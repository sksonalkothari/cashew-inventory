from pydantic import BaseModel, field_validator
from typing import Optional
from app.validators.common_validators import not_empty, remap_date_field, valid_date, positive_float, positive_int


class ProductionCreateRequest(BaseModel):
    production_date: str
    _map_date = remap_date_field("production_date")
    grade_id: Optional[int]
    batch_number: Optional[str]
    shape: Optional[str]
    processing: Optional[str]
    packaging: Optional[str]
    quantity_in_tin: Optional[float]

    @field_validator("batch_number")
    @classmethod
    def validate_batch_number(cls, value: str, info):
        return not_empty(value, info.field_name)

    @field_validator("production_date")
    @classmethod
    def validate_production_date(cls, value: str, info):
        return valid_date(value, info.field_name)


class ProductionUpdateRequest(BaseModel):
    id: int
    production_date: Optional[str]
    _map_date = remap_date_field("production_date")
    grade_id: Optional[int]
    batch_number: Optional[str]
    shape: Optional[str]
    processing: Optional[str]
    packaging: Optional[str]
    quantity_in_tin: Optional[float]
    
    @field_validator("id")
    @classmethod
    def validate_id(cls, value: int, info):
        return positive_int(value, info.field_name)

    @field_validator("production_date")
    @classmethod
    def validate_production_date(cls, value: str, info):
        return valid_date(value, info.field_name)


class ProductionDeleteRequest(BaseModel):
    id: int

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: int, info):
        return positive_int(value, info.field_name)


class ProductionFetchByBatchNumberRequest(BaseModel):
    batch_number: str

    @field_validator("batch_number")
    @classmethod
    def validate_batch_number(cls, value: str, info):
        return not_empty(value, info.field_name)


class ProductionResponse(BaseModel):
    id: int
    production_date: str
    grade_id: Optional[int]
    batch_number: Optional[str]
    shape: Optional[str]
    processing: Optional[str]
    packaging: Optional[str]
    quantity_in_tin: Optional[int]
    created_by: Optional[str]
    updated_by: Optional[str]
    is_deleted: Optional[bool] = False
    created_at: Optional[str]
    updated_at: Optional[str]
