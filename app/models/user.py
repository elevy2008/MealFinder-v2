from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    id: str
    email: EmailStr
    hashed_password: Optional[str] = None  # Optional for email-only users
    is_premium: bool = False
    created_at: datetime
    last_login: Optional[datetime] = None

class Portfolio(BaseModel):
    user_id: str
    ticker: str
    amount: float
    added_at: datetime
