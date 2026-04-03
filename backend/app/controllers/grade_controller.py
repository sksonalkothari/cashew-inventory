from typing import Union, List
from fastapi import APIRouter, Depends
from app.models.grade_models import GradeCreateRequest, GradeUpdateRequest, GradeDeleteRequest, GradeMetadata
from app.services import grade_service
from app.dependencies.role_dependency import require_roles
from app.utils.logger import logger

router = APIRouter(prefix="/grades", tags=["Grades"])

@router.post("/", summary="Create Grade", description="Create a new grade (admin or entry_operator)")
async def create_grade(
    data: Union[GradeCreateRequest, List[GradeCreateRequest]],
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info("Creating a new grade")
    records = data if isinstance(data, list) else [data]
    enriched = [{**rec.model_dump(), "created_by": current_user["id"]} for rec in records]
    # pass list or single depending on caller preference
    payload = enriched if len(enriched) > 1 else enriched[0]
    result = await grade_service.insert_or_reactivate_grade(payload, current_user["headers"])
    return result


@router.patch("/", summary="Update Grade", description="Update an existing grade (admin or entry_operator)")
async def update_grade(
    data: Union[GradeUpdateRequest, List[GradeUpdateRequest]],
    current_user: dict = Depends(require_roles(["admin", "entry_operator"]))
):
    logger.info(f"Updating grade ID {data.id}")
    records = data if isinstance(data, list) else [data]
    enriched = [{**rec.model_dump(), "updated_by": current_user["id"]} for rec in records]
    result = await grade_service.update_grade(enriched, current_user["headers"])
    return result


@router.delete("/", summary="Delete Grade", description="Soft-delete a grade (admin only)")
async def delete_grade(
    data: Union[GradeDeleteRequest, List[GradeDeleteRequest]],
    current_user: dict = Depends(require_roles(["admin"]))
):
    logger.info(f"Soft-deleting grade ID {data.id}")
    records = data if isinstance(data, list) else [data]
    enriched = [{**rec.model_dump(), "updated_by": current_user["id"]} for rec in records]
    for rec in enriched:
        rec["is_deleted"] = True
    result = await grade_service.delete_grade(enriched, current_user["headers"])
    return result


@router.get("/", summary="Fetch Grades", description="Fetch all active grades")
async def get_grades(
    current_user: dict = Depends(require_roles(["admin", "entry_operator", "viewer"]))
):
    logger.info("Fetching all grades")
    result = await grade_service.fetch_grades(current_user["headers"])
    return result