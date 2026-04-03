from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from app.validators.common_validators import not_empty, positive_int

class GradeCreateRequest(BaseModel):
    grade_name: str

    @field_validator("grade_name")
    @classmethod
    def validate_grade_name(cls, value: str, info):
        return not_empty(value, info.field_name)

class GradeUpdateRequest(BaseModel):
    id: int
    grade_name: str

    @field_validator("grade_name")
    @classmethod
    def validate_grade_name(cls, value: str, info):
        return not_empty(value, info.field_name)

class GradeDeleteRequest(BaseModel):
    id: int

    @field_validator("id")
    @classmethod
    def validate_positive_int(cls, value: int, info):
        return positive_int(value, info.field_name)

class GradeMetadata(BaseModel):
    id: int
    grade_name: str
    created_by: Optional[str]
    updated_by: Optional[str]
    is_deleted: Optional[bool] = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]