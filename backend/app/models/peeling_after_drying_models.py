from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.validators.common_validators import not_empty, remap_date_field, valid_date, positive_float, positive_int

class PeelingAfterDryingCreateRequest(BaseModel):
    peeling_date: str = Field(..., description="Date in YYYY-MM-DD format")
    batch_number: str
    wholes_kg: Optional[float]
    pieces_kg: Optional[float]
    unpeeled_kg: Optional[float]
    swp_kg: Optional[float]
    bb_kg: Optional[float]
    rejection_kg: Optional[float]
    cutting_pieces_kg: Optional[float]
    total_quantity_kg: Optional[float]
    decrease: Optional[float]
    _map_date = remap_date_field("peeling_date")

    @field_validator("batch_number")
    @classmethod
    def validate_fields(cls, value: str, info):
        return not_empty(value, info.field_name)
    
    @field_validator("peeling_date")
    @classmethod
    def validate_peeling_date(cls, value: str, info):
        return valid_date(value, info.field_name)


class PeelingAfterDryingUpdateRequest(BaseModel):
    id: int
    peeling_date: Optional[str]
    batch_number: Optional[str]
    wholes_kg: Optional[float]
    pieces_kg: Optional[float]
    unpeeled_kg: Optional[float]
    swp_kg: Optional[float]
    bb_kg: Optional[float]
    rejection_kg: Optional[float]
    cutting_pieces_kg: Optional[float]
    total_quantity_kg: Optional[float]
    decrease: Optional[float]
    _map_date = remap_date_field("peeling_date")
    
    @field_validator("batch_number")
    @classmethod
    def validate_fields(cls, value: str, info):
        return not_empty(value, info.field_name)

    @field_validator("peeling_date")
    @classmethod
    def validate_peeling_date(cls, value: str, info):
        return valid_date(value, info.field_name)
    
    @field_validator("id")
    @classmethod
    def validate_positive_int(cls, value: int, info):
        return positive_int(value, info.field_name)


class PeelingAfterDryingDeleteRequest(BaseModel):
    id: int

    @field_validator("id")
    @classmethod
    def validate_positive_int(cls, value: int, info):
        return positive_int(value, info.field_name)


class PeelingAfterDryingFetchByBatchNumberRequest(BaseModel):
    batch_number: str

    @field_validator("batch_number")
    @classmethod
    def validate_batch_number(cls, value: str, info):
        return not_empty(value, info.field_name)


class PeelingAfterDryingResponse(BaseModel):
    id: int
    peeling_date: str
    batch_number: str
    wholes_kg: Optional[float]
    pieces_kg: Optional[float]
    unpeeled_kg: Optional[float]
    swp_kg: Optional[float]
    bb_kg: Optional[float]
    rejection_kg: Optional[float]
    cutting_pieces_kg: Optional[float]
    total_quantity_kg: Optional[float]
    decrease: Optional[float]
    created_by: Optional[str]
    updated_by: Optional[str]
    is_deleted: Optional[bool] = False
    created_at: Optional[str]
    updated_at: Optional[str]
