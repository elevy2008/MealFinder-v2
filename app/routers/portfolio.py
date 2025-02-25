from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from ..schemas.user import PortfolioAdd
from ..services.auth import get_current_user
from ..services.stock import get_stock_data, get_stock_history
from ..services.news import get_stock_news
from typing import Dict, List, Optional
import uuid
import logging
import json
import asyncio
from datetime import datetime, timedelta
from ..core.limiter import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

logger = logging.getLogger(__name__)

# In-memory portfolio storage
router = APIRouter(prefix="/portfolio", tags=["portfolio"])
portfolios: Dict[str, List[dict]] = {}

@router.post("/holdings")
async def add_holding(
    request: Request,
    holding: PortfolioAdd,
    user_id: str = Depends(get_current_user)
):
    try:
        logger.info(f"Adding holding for user {user_id}: {holding.ticker}")
        
        # Get stock data
        stock_data = await get_stock_data(request, holding.ticker)
        if not stock_data:
            logger.error(f"Invalid stock ticker: {holding.ticker}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": f"Invalid stock ticker: {holding.ticker}"}
            )
        
        # Initialize user portfolio if needed
        if user_id not in portfolios:
            portfolios[user_id] = []
            logger.info(f"Created new portfolio for user {user_id}")
        
        # Create new holding
        new_holding = {
            "id": str(uuid.uuid4()),
            "ticker": holding.ticker.upper(),
            "amount": holding.amount,
            "current_data": stock_data
        }
        portfolios[user_id].append(new_holding)
        logger.info(f"Successfully added holding: {new_holding}")
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Holding added successfully", "data": new_holding}
        )
    except Exception as e:
        logger.error(f"Error adding holding: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(e)}
        )

@router.get("/holdings")
async def get_holdings(
    request: Request,
    user_id: str = Depends(get_current_user)
) -> List[Dict]:
    try:
        start_time = datetime.now()
        logger.info(
            "Getting holdings",
            extra={
                "user_id": user_id,
                "path": request.url.path,
                "method": request.method
            }
        )
        
        # Initialize portfolio if needed
        if user_id not in portfolios:
            portfolios[user_id] = []
            
        holdings = portfolios.get(user_id, [])
        logger.info(f"Found {len(holdings)} holdings for user {user_id}")
        
        # Return holdings with current data
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=holdings
        )
    except Exception as e:
        logger.error(f"Error getting holdings: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(e)}
        )

@router.delete("/holdings/{holding_id}")
async def remove_holding(
    request: Request,
    holding_id: str,
    user_id: str = Depends(get_current_user)
):
    start_time = datetime.now()
    logger.info(
        "Removing holding",
        extra={
            "user_id": user_id,
            "holding_id": holding_id,
            "path": request.url.path,
            "method": request.method,
            "process_time": (datetime.now() - start_time).total_seconds()
        }
    )
    
    if user_id not in portfolios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Holding not found"
        )
    
    portfolios[user_id] = [
        h for h in portfolios[user_id]
        if h["id"] != holding_id
    ]
    
    return {"message": "Holding removed successfully"}

@router.get("/analysis")
@limiter.limit("5/minute")
async def get_portfolio_analysis(
    request: Request,
    user_id: str = Depends(get_current_user)
):
    """Get portfolio analysis with rate limiting"""
    try:
        logger.info(f"Getting portfolio analysis for user {user_id}")
        holdings = portfolios.get(user_id, [])
        
        if not holdings:
            logger.info(f"No holdings found for user {user_id}")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=[]
            )
            
        analysis = []
        for holding in holdings:
            try:
                # Use existing stock data from holdings
                stock_data = holding.get("current_data", {})
                
                # Get historical data (mock data if needed)
                history = await get_stock_history(holding["ticker"])
                if history is None:
                    history = [
                        {
                            "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
                            "close": 150 + (i % 5),
                            "volume": 1000000 - (i * 10000)
                        }
                        for i in range(30)
                    ]
                    logger.warning(f"Using mock history data for {holding['ticker']}")
                
                # Get news data (mock data if needed)
                news = await get_stock_news(request, stock_data.get("company_name", ""), holding["ticker"])
                if news is None:
                    news = [
                        {
                            "title": f"{holding['ticker']} Market Update",
                            "description": "Latest market analysis...",
                            "url": "https://example.com/news/1",
                            "published_at": datetime.now().isoformat(),
                            "source": "Market News"
                        }
                    ]
                    logger.warning(f"Using mock news data for {holding['ticker']}")
                
                analysis.append({
                    "ticker": holding["ticker"],
                    "amount": holding["amount"],
                    "current_data": stock_data,
                    "history": history,
                    "news": news
                })
                logger.info(f"Successfully analyzed {holding['ticker']}")
            except Exception as e:
                logger.error(f"Error analyzing {holding['ticker']}: {e}", exc_info=True)
                continue
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=analysis
        )
    except RateLimitExceeded as e:
        logger.warning(f"Rate limit exceeded: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Too many requests"},
            headers={"Retry-After": str(e.retry_after)}
        )
    except Exception as e:
        logger.error(f"Error getting portfolio analysis: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(e)}
        )
