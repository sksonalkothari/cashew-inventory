from pydantic import BaseModel, EmailStr, field_validator
from app.validators.common_validators import not_empty

STATUS_VALUES = {"pending", "active", "disabled"}

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

    @field_validator("name", "password")
    @classmethod
    def validate_fields(cls, value: str, info):
        return not_empty(value, info.field_name)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        return not_empty(value, "password")