from typing import Optional
from pydantic import BaseModel, field_validator  
from app.validators.common_validators import not_empty, remap_date_field, valid_date, positive_float, positive_int

class BoilingCreateRequest(BaseModel):
    boiling_date: str
    _map_date = remap_date_field("boiling_date")
    batch_number: str
    quantity_kg: float
   
    @field_validator("boiling_date", "batch_number")
    @classmethod
    def validate_fields(cls, value: str, info):
        return not_empty(value, info.field_name)
    
    @field_validator("quantity_kg")
    @classmethod    
    def validate_positive_numbers(cls, value: float, info):
        return positive_float(value, info.field_name)
    
    @field_validator("boiling_date")
    @classmethod
    def validate_boiling_date(cls, value: str, info):
        return valid_date(value, info.field_name)

class BoilingUpdateRequest(BaseModel):
    id: int
    boiling_date: str
    batch_number: str
    quantity_kg: float
    _map_date = remap_date_field("boiling_date")

    @field_validator("batch_number")
    @classmethod    
    def validate_fields(cls, value: str, info):
        return not_empty(value, info.field_name)
    
    @field_validator("quantity_kg")
    @classmethod
    def validate_positive_float(cls, value: float, info):
        return positive_float(value, info.field_name)
    
    @field_validator("boiling_date")
    @classmethod
    def validate_boiling_date(cls, value: str, info):
        return valid_date(value, info.field_name)
    
    @field_validator("id")
    @classmethod    
    def validate_positive_int(cls, value: int, info):
        return positive_int(value, info.field_name)  

class BoilingDeleteRequest(BaseModel):
    id: int

    @field_validator("id")
    @classmethod
    def validate_positive_int(cls, value: int, info):
        return positive_int(value, info.field_name)