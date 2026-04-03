from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional, List
from datetime import datetime
from app.enum.user_status import UserStatus
from app.validators.common_validators import not_empty, must_be_in

STATUS_VALUES = {UserStatus.PENDING, UserStatus.ACTIVE, UserStatus.DISABLED}

class StatusUpdateRequest(BaseModel):
    user_id: str
    status: str
    is_deleted: Optional[bool] = False

    @field_validator("user_id", "status")
    @classmethod
    def validate_fields(cls, value: str, info):
        return not_empty(value, info.field_name)

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str, info):
        return must_be_in(value, STATUS_VALUES, info.field_name)

    @model_validator(mode="after")
    def check_status_and_deletion(cls, values):
        if values.status == "active" and values.is_deleted:
            raise ValueError("Active users cannot be marked as deleted")
        return values

class UserMetadata(BaseModel):
    id: str
    name: str
    email: EmailStr
    status: str
    is_deleted: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("id", "name", "status")
    @classmethod
    def validate_fields(cls, value: str, info):
        return not_empty(value, info.field_name)

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str, info):
        return must_be_in(value, STATUS_VALUES, info.field_name)
    
class RoleUpdateRequest(BaseModel):
    user_id: str
    roles_to_add: List[str] = []
    roles_to_remove: List[str] = []
    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, value: str):
        return not_empty(value, "user_id")
    @model_validator(mode="after")
    def check_roles(cls, values):
        if not values.roles_to_add and not values.roles_to_remove:
            raise ValueError("At least one of roles_to_add or roles_to_remove must be provided")
        return values       
    