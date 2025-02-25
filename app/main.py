from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routers import auth, portfolio, email
import os
import sys
import asyncio
from dotenv import load_dotenv
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from datetime import datetime
import logging
from .core.limiter import limiter, rate_limit_exceeded_handler
import uvicorn

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Return - Stock Portfolio API",
    description="API for managing stock portfolios and sending email summaries",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS first (before any other middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"]
)

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    try:
        logger.info("Starting Return API server")
        logger.info(f"Environment: {os.getenv('ENV', 'development')}")
        
        # Initialize routers
        app.include_router(auth.router)
        app.include_router(portfolio.router)
        app.include_router(email.router)
        logger.info("Routers initialized")
        
        logger.info("Server startup complete")
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    try:
        logger.info("Shutting down Return API server")
        # Close any open connections
        logger.info("Server shutdown complete")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}", exc_info=True)
        raise

# Configure middleware and rate limiter
try:
    # Configure rate limiter first
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)
    
    # Add CORS after rate limiter
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )
    
    logger.info("Rate limiter and middleware configured successfully")
except Exception as e:
    logger.error(f"Failed to configure middleware: {e}", exc_info=True)
    raise

# Include routers
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    """Global error handling and request logging middleware"""
    start_time = datetime.now()
    request_id = os.urandom(8).hex()
    
    try:
        logger.info(
            "Request started",
            extra={
                "request_id": request_id,
                "path": request.url.path,
                "method": request.method,
                "client_host": request.client.host if request.client else "unknown",
                "user_agent": request.headers.get("user-agent", "unknown")
            }
        )
        
        try:
            response = await call_next(request)
            process_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(
                "Request completed",
                extra={
                    "request_id": request_id,
                    "path": request.url.path,
                    "method": request.method,
                    "status_code": response.status_code,
                    "process_time": process_time
                }
            )
            
            response.headers["X-Request-ID"] = request_id
            return response
            
        except RateLimitExceeded:
            logger.warning(
                "Rate limit exceeded",
                extra={
                    "request_id": request_id,
                    "path": request.url.path,
                    "method": request.method
                }
            )
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests",
                    "request_id": request_id
                },
                headers={"X-Request-ID": request_id}
            )
        
    except Exception as e:
        logger.error(
            "Request failed",
            extra={
                "request_id": request_id,
                "path": request.url.path,
                "method": request.method,
                "error": str(e),
                "error_type": type(e).__name__
            },
            exc_info=True
        )
        
        if isinstance(e, RateLimitExceeded):
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests",
                    "request_id": request_id
                },
                headers={"X-Request-ID": request_id}
            )
        elif isinstance(e, asyncio.TimeoutError):
            return JSONResponse(
                status_code=504,
                content={
                    "detail": "Request timed out",
                    "request_id": request_id
                },
                headers={"X-Request-ID": request_id}
            )
        else:
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "request_id": request_id
                },
                headers={"X-Request-ID": request_id}
            )

app.include_router(auth.router)
app.include_router(portfolio.router)
app.include_router(email.router)

@app.get("/healthz")
@limiter.limit("5/minute")
async def healthz(request: Request):
    """Health check endpoint with rate limiting"""
    request_id = os.urandom(8).hex()
    try:
        logger.info(
            "Health check request received",
            extra={
                "request_id": request_id,
                "client_host": request.client.host if request.client else "unknown"
            }
        )
        
        # Basic health checks
        checks = {
            "api": True,
            "rate_limiter": bool(app.state.limiter),
            "cors": True
        }
        
        response = JSONResponse(
            content={
                "status": "ok",
                "timestamp": datetime.now().isoformat(),
                "checks": checks,
                "request_id": request_id
            },
            headers={"X-Request-ID": request_id}
        )
        
        logger.info(
            "Health check completed",
            extra={
                "request_id": request_id,
                "checks": checks
            }
        )
        
        return response
    except Exception as e:
        logger.error(
            "Health check failed",
            extra={
                "request_id": request_id,
                "error": str(e)
            },
            exc_info=True
        )
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "detail": str(e),
                "request_id": request_id
            },
            headers={"X-Request-ID": request_id}
        )
