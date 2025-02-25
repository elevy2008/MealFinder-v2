from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class EmailOnlyRegister(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr

class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    password: Optional[str] = None  # Optional for email-only users

class UserLogin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    password: str

class PortfolioAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    ticker: str = Field(..., min_length=1, max_length=10, description="Stock ticker symbol")
    amount: float = Field(..., gt=0, description="Number of shares")

class Token(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    token_type: str = "bearer"
