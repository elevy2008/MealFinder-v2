from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class EmailOnlyRegister(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: Optional[str] = None  # Optional for email-only users

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PortfolioAdd(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10, description="Stock ticker symbol")
    amount: float = Field(..., gt=0, description="Number of shares")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
