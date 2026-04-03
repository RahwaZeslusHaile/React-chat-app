from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int  # Token expiration time in seconds


class UserInfo(BaseModel):
    """User information schema"""
    username: str
    user_id: Optional[str] = None
