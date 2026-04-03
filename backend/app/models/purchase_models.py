from pydantic import BaseModel, Field, field_validator, root_validator
from typing import Optional
from app.validators.common_validators import not_empty, remap_date_field, valid_date, positive_float, positive_int

class PurchaseCreateRequest(BaseModel):
    purchase_date: str = Field(..., description="Date in YYYY-MM-DD format")
    supplier_name: str
    bill_number: str
    batch_number: str
    quantity_kg: float
    price_per_kg: float
    total_amount: Optional[float] = Field(None, description="Auto-calculated as quantity_kg * price_per_kg")
    _map_date = remap_date_field("purchase_date")

    @field_validator("purchase_date", "supplier_name", "bill_number", "batch_number")
    @classmethod
    def validate_fields(cls, value: str, info):
        return not_empty(value, info.field_name)
    
    @field_validator("quantity_kg", "price_per_kg")
    @classmethod
    def validate_positive_numbers(cls, value: float, info):
        return positive_float(value, info.field_name)
    
    @field_validator("purchase_date")
    @classmethod
    def validate_purchase_date(cls, value: str, info):
        return valid_date(value, info.field_name)
   
class PurchaseUpdateRequest(BaseModel):
    id: int
    purchase_date: Optional[str]
    supplier_name: Optional[str]
    bill_number: Optional[str]
    batch_number: Optional[str]
    quantity_kg: Optional[float]
    price_per_kg: Optional[float]

    @field_validator("purchase_date", "supplier_name", "bill_number", "batch_number")
    @classmethod
    def validate_fields(cls, value: str, info):
        return not_empty(value, info.field_name)
    
    @field_validator("quantity_kg", "price_per_kg")
    @classmethod
    def validate_positive_float(cls, value: float, info):
        return positive_float(value, info.field_name)
    
    @field_validator("purchase_date")
    @classmethod
    def validate_purchase_date(cls, value: str, info):
        return valid_date(value, info.field_name)
    
    @field_validator("id")
    @classmethod
    def validate_positive_int(cls, value: int, info):
        return positive_int(value, info.field_name)


class PurchaseDeleteRequest(BaseModel):
    id: int

    @field_validator("id")
    @classmethod
    def validate_positive_int(cls, value: int, info):
        return positive_int(value, info.field_name)