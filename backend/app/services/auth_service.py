from app.dao import auth_dao, user_dao
from app.enum.user_status import UserStatus
from app.exceptions.exceptions import AuthError
from app.models.auth_models import SignupRequest, LoginRequest
from app.services import user_service
from app.utils.logger import logger
from app.config import get_user_headers

async def signup_user(data: SignupRequest):
    logger.info(f"Signup initiated for {data.email}")

    user = await auth_dao.signup_user(data.email, data.password)
    
    uid = user["user"]["id"]

    await user_dao.insert_user_metadata({
        "id": uid,
        "name": data.name,
        "email": data.email,
        "status": "pending",
        "is_deleted": False
    })

    logger.info(f"Signup completed for {data.email}")
    return "Signup completed successfully. Contact your system Administrator to activate your account."

async def login_user(data: LoginRequest):
    logger.info(f"Login attempt for {data.email}")
    token_data = await auth_dao.login_user(data.email, data.password)
    user_id = token_data["user"]["id"]

    headers = get_user_headers(token_data["access_token"])

    user = await user_service.get_user_metadata_by_email(data.email, headers)
    logger.debug(f"Logged in User's status: {user['status']}")
    if user["status"] == UserStatus.ACTIVE and user["status"] != UserStatus.DISABLED:
        roles = await user_service.get_user_roles(user_id, headers)
        token_data["user"]["roles"] = roles
    else:
        raise AuthError(f"{data.email} cannot login. Activation is pending. Contact your administrator.")    
    return token_data