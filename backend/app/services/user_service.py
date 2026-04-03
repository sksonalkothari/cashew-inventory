import asyncio
from app.dao import user_dao
from app.models.user_models import RoleUpdateRequest
from app.utils.logger import logger
from app.exceptions.exceptions import UserError

async def get_user_metadata(user_id: str, headers: dict):
    logger.info(f"Fetching metadata for user ID {user_id}")
    metadata = await user_dao.get_user_metadata(user_id, headers)
    if len(metadata) == 0:
        raise UserError(f"User metadata for user ID {user_id} not found")
    return metadata[0] if isinstance(metadata, list) else metadata

async def get_user_metadata_by_email(email: str, headers: dict):
    logger.info(f"Fetching metadata for user {email}")
    metadata = await user_dao.get_user_metadata_by_email(email, headers)
    if len(metadata) == 0:
        raise UserError(f"User metadata for user {email} not found")
    return metadata[0] if isinstance(metadata, list) else metadata

async def update_user_status(data: RoleUpdateRequest, headers: dict):
    logger.info(f"Updating status for user ID {data.user_id}")
    await get_user_metadata(data.user_id, headers)  # Ensure user exists
    return await user_dao.update_user_status(
        user_id=data.user_id,
        status=data.status,
        is_deleted=data.is_deleted or False,
        headers=headers
    )

async def update_user_roles(data: dict, headers: dict):
    logger.info(f"Updating roles for user ID {data['user_id']}")

    # Prepare insert and delete tasks
    insert_tasks = [
        user_dao.insert_or_reactivate_user_role(data['user_id'], role, data["updated_by"], headers)
        for role in data["roles_to_add"]
    ]

    delete_tasks = [
        user_dao.delete_user_role(data["user_id"], role, data["updated_by"], headers)
        for role in data["roles_to_remove"]
    ]

    # Run all tasks concurrently
    results = await asyncio.gather(*insert_tasks, *delete_tasks, return_exceptions=True)

    # Track failed actions
    failed_actions = []

    # Log individual failures
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            action = "insert" if i < len(insert_tasks) else "delete"
            role = data["roles_to_add"][i] if action == "insert" else data["roles_to_remove"][i - len(insert_tasks)]
            logger.error(f"Failed to {action} role '{role}' for user {data['user_id']}: {result}")
            failed_actions.append(f"{action} '{role}'")

    # Raise consolidated error if any failed
    if failed_actions:
        error_message = (
            f"Role update failed for user {data['user_id']}. "
            f"Failed actions: {', '.join(failed_actions)}"
        )
        raise UserError(error_message, status_code=400)

    return {
        "user_id": data["user_id"],
        "roles_added": data["roles_to_add"],
        "roles_removed": data["roles_to_remove"]
    }

async def get_user_roles(user_id: str, headers: dict):
    logger.info(f"Fetching metadata for logged in user")
    user_roles = await user_dao.get_user_roles(user_id, headers)
    if len(user_roles) == 0:
        raise UserError(f"User roles are not assigned. Contact your System Administrator.")
    return user_roles