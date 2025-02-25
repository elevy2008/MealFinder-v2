from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from ..schemas.user import UserCreate, UserLogin, Token, EmailOnlyRegister
from ..core.limiter import limiter, rate_limit_exceeded_handler
from ..services.auth import create_access_token, get_password_hash, verify_password, get_current_user
from datetime import timedelta
import uuid
import logging
import json
from typing import Dict, Optional

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

# In-memory user storage
users: Dict[str, dict] = {}

@router.post("/register")
async def register(request: Request, user: UserCreate):
    try:
        logger.info(f"Registration attempt for email: {user.email}")
        
        # Check if email exists
        if user.email in [u["email"] for u in users.values()]:
            logger.warning(f"Registration failed - email already exists: {user.email}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Email already registered"}
            )
        
        # Create user
        user_id = str(uuid.uuid4())
        user_data = {
            "id": user_id,
            "email": user.email,
            "hashed_password": get_password_hash(user.password) if user.password else None,
            "is_premium": False
        }
        users[user_id] = user_data
        logger.info(f"User created with ID: {user_id}")
        
        # Generate token
        access_token = create_access_token(
            data={"sub": user_id},
            expires_delta=timedelta(days=7)
        )
        logger.info(f"Access token generated for user: {user_id}")
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"access_token": access_token, "token_type": "bearer"}
        )
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Registration failed"}
        )

@router.post("/login")
async def login(request: Request, user: UserLogin):
    try:
        logger.info(f"Login attempt for email: {user.email}")
        
        # Find user
        user_data = next(
            (u for u in users.values() if u["email"] == user.email),
            None
        )
        
        # Validate credentials
        if not user_data or not user_data["hashed_password"]:
            logger.warning(f"Login failed - user not found: {user.email}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid credentials"}
            )
            
        if not verify_password(user.password, user_data["hashed_password"]):
            logger.warning(f"Login failed - invalid password: {user.email}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid credentials"}
            )
        
        # Generate token
        access_token = create_access_token(
            data={"sub": user_data["id"]},
            expires_delta=timedelta(days=7)
        )
        logger.info(f"Login successful for user: {user_data['id']}")
        
        return JSONResponse(
            content={"access_token": access_token, "token_type": "bearer"}
        )
    except Exception as e:
        logger.error(f"Login failed for {user.email}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.post("/email-only")
async def register_email_only(user: EmailOnlyRegister):
    if user.email in [u["email"] for u in users.values()]:
        return {"message": "Email already registered"}
    
    user_id = str(uuid.uuid4())
    user_data = {
        "id": user_id,
        "email": user.email,
        "hashed_password": None,
        "is_premium": False
    }
    users[user_id] = user_data
    return {"message": "Email registered successfully"}

@router.post("/upgrade-premium")
async def upgrade_to_premium(user_id: str = Depends(get_current_user)):
    if not user_id or user_id not in users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    users[user_id]["is_premium"] = True
    return {"message": "Upgraded to premium successfully"}
