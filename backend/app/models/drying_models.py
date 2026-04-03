from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.validators.common_validators import not_empty, remap_date_field, valid_date, positive_float, positive_int

class DryingCreateRequest(BaseModel):
    drying_date: str = Field(..., description="Date in YYYY-MM-DD format")
    batch_number: str
    nw_wholes_in_kg:  Optional[float]
    nw_wholes_out_kg: Optional[float]
    nw_pieces_in_kg: Optional[float]
    nw_pieces_out_kg: Optional[float]
    nw_rejection_in_kg: Optional[float]
    nw_rejection_out_kg: Optional[float]
    moisture_loss: Optional[float]
    _map_date = remap_date_field("drying_date")

    @field_validator("batch_number")
    @classmethod
    def validate_fields(cls, value: str, info):
        return not_empty(value, info.field_name)

    @field_validator("drying_date")
    @classmethod
    def validate_drying_date(cls, value: str, info):
        return valid_date(value, info.field_name)

class DryingUpdateRequest(BaseModel):
    id: int
    drying_date: Optional[str]
    batch_number: Optional[str]
    nw_wholes_in_kg: Optional[float]
    nw_pieces_in_kg: Optional[float]
    nw_rejection_in_kg: Optional[float]
    nw_wholes_out_kg: Optional[float]
    nw_pieces_out_kg: Optional[float]
    nw_rejection_out_kg: Optional[float]
    moisture_loss: Optional[float]
    _map_date = remap_date_field("drying_date")

    @field_validator("batch_number")
    @classmethod
    def validate_fields(cls, value: str, info):
        return not_empty(value, info.field_name)

    @field_validator("drying_date")
    @classmethod
    def validate_drying_date(cls, value: str, info):
        return valid_date(value, info.field_name)
    
    @field_validator("id")
    @classmethod
    def validate_positive_int(cls, value: int, info):
        return positive_int(value, info.field_name)


class DryingDeleteRequest(BaseModel):
    id: int

    @field_validator("id")
    @classmethod
    def validate_positive_int(cls, value: int, info):
        return positive_int(value, info.field_name)
    
class DryingFetchByBatchNumberRequest(BaseModel):
    batch_number: str

    @field_validator("batch_number")
    @classmethod
    def validate_batch_number(cls, value: str, info):
        return not_empty(value, info.field_name)