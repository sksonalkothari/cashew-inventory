from fastapi import APIRouter
from app.models.auth_models import SignupRequest, LoginRequest
from app.services import auth_service
from app.utils.logger import logger


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", summary="User Signup", description="Creates a new user account")
async def signup(data: SignupRequest):
    logger.info(f"Received signup request for {data.email}")
    user = await auth_service.signup_user(data)
    return user


@router.post("/login", summary="User Login", description="Authenticates a user and returns a JWT token")
async def login(data: LoginRequest):
    logger.info(f"Received login request for {data.email}")
    token = await auth_service.login_user(data)
    return token
