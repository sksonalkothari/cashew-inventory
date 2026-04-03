from fastapi import APIRouter, Depends, Request
from app.config import get_user_headers
from app.decorators.inject_headers import inject_headers
from app.utils.response_wrapper import wrap_response
from app.dependencies.auth_dependency import get_current_user
from app.models.user_models import StatusUpdateRequest, RoleUpdateRequest, UserMetadata
from app.services import user_service
from app.utils.logger import logger
from app.dependencies.role_dependency import require_roles

router = APIRouter(prefix="/user", tags=["Users"])

@router.get("/me", summary="User Metdata", description="Get Logged in user Metdata")
async def get_my_metadata(
    current_user: dict = Depends(get_current_user)
):
    logger.info(f"Received get user metdata for logged in user")
    user_id = current_user["id"]
    headers = current_user["headers"]
    logger.debug(f"Fetching metadata of user {user_id}")
    metadata = await user_service.get_user_metadata(user_id, headers)
    return metadata


@router.patch("/status", summary="Update User Status", description="Admin-only: updates status and deletion flag")
async def update_status(
    data: StatusUpdateRequest, 
    current_user: dict = Depends(require_roles("admin"))
):
    logger.info(f"Received status update for user ID {data.user_id}")
    headers = current_user["headers"]
    result = await user_service.update_user_status(data, headers)
    return wrap_response(result)


@router.patch("/roles", summary="Update User Roles", description="Admin-only: assign or remove roles for a user")
async def update_roles(
    data: RoleUpdateRequest,
    current_user: dict = Depends(require_roles(["admin"]))
):
    enriched_data = data.model_dump()
    enriched_data["updated_by"] = current_user["id"]
    headers = current_user["headers"]
    result = await user_service.update_user_roles(enriched_data, headers)
    return wrap_response(result)
