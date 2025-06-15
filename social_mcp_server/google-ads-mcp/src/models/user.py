"""User models."""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    """Base user model."""
    username: str = Field(..., min_length=3, max_length=50, regex="^[a-zA-Z0-9_-]+$")
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(UserBase):
    """User model for database storage."""
    hashed_password: str

class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """User update model."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    """User response model."""
    class Config:
        orm_mode = True

class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str
    user: User

class TokenData(BaseModel):
    """Token data model."""
    username: Optional[str] = None
