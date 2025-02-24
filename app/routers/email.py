from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from ..services.auth import get_current_user
from ..services.email import send_daily_summary
from typing import Dict, List, Optional

router = APIRouter(prefix="/email", tags=["email"])

# In-memory email preferences storage
email_preferences: Dict[str, dict] = {}

@router.post("/preferences")
async def set_email_preferences(
    frequency: str,
    user_id: Optional[str] = Depends(get_current_user)
):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    if frequency not in ["daily", "weekly", "none"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid frequency. Choose 'daily', 'weekly', or 'none'"
        )
    
    email_preferences[user_id] = {"frequency": frequency}
    return {"message": "Email preferences updated successfully"}

@router.post("/send-summary")
async def trigger_email_summary(
    background_tasks: BackgroundTasks,
    user_id: Optional[str] = Depends(get_current_user)
):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    from .portfolio import portfolios  # Local import to avoid circular dependency
    holdings = portfolios.get(user_id, [])
    
    if not holdings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No holdings found in portfolio"
        )
    
    background_tasks.add_task(send_daily_summary, user_id, holdings)
    return {"message": "Email summary triggered successfully"}
