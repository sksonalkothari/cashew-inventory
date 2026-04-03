from app.models.grade_models import GradeCreateRequest, GradeUpdateRequest, GradeDeleteRequest
from app.dao import grade_dao
from app.utils.logger import logger

async def insert_or_reactivate_grade(data: dict, headers: dict):
    return await grade_dao.insert_or_reactivate_grade(data, headers)

async def update_grade(data: dict, headers: dict):
    return await grade_dao.update_grade(data, headers)

async def delete_grade(data: dict, headers: dict):
    return await grade_dao.soft_delete_grade(data, headers)

async def fetch_grades(headers: dict):
    return await grade_dao.fetch_active_grades(headers)