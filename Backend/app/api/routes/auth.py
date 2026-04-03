from datetime import timedelta
from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.jwt_handler import create_access_token, TOKEN_EXPIRATION_HOURS

router = APIRouter(prefix="/auth", tags=["auth"])

USERS_DB = {
    "user1": "password123",
    "demo": "demo123",
}


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest) -> TokenResponse:
    """
    Authenticate user and return JWT token.
    
    Args:
        request: LoginRequest containing username and password
        
    Returns:
        TokenResponse with access token
        
    Raises:
        HTTPException: If credentials are invalid
    """
    if request.username not in USERS_DB or USERS_DB[request.username] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    token = create_access_token(
        data={"sub": request.username, "user_id": request.username}
    )
    
    expires_in = TOKEN_EXPIRATION_HOURS * 3600
    
    return TokenResponse(
        access_token=token,
        token_type="Bearer",
        expires_in=expires_in
    )
