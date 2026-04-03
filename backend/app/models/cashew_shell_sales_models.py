from pydantic import BaseModel, field_validator
from typing import Optional
from app.validators.common_validators import not_empty, remap_date_field, valid_date, positive_int


class CashewShellSalesCreateRequest(BaseModel):
    sale_date: str
    _map_date = remap_date_field("sale_date")
    bill_number: str
    customer_name: str
    batch_number: Optional[str]
    quantity_kg: Optional[float] = 0.0
    price_per_kg: Optional[float] = 0.0

    @field_validator("bill_number")
    @classmethod
    def validate_bill_number(cls, value: str, info):
        return not_empty(value, info.field_name)

    @field_validator("customer_name")
    @classmethod
    def validate_customer_name(cls, value: str, info):
        return not_empty(value, info.field_name)

    @field_validator("sale_date")
    @classmethod
    def validate_sale_date(cls, value: str, info):
        return valid_date(value, info.field_name)


class CashewShellSalesUpdateRequest(BaseModel):
    id: int
    sale_date: Optional[str]
    _map_date = remap_date_field("sale_date")
    bill_number: Optional[str]
    customer_name: Optional[str]
    batch_number: Optional[str]
    quantity_kg: Optional[float]
    price_per_kg: Optional[float]

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: int, info):
        return positive_int(value, info.field_name)

    @field_validator("sale_date")
    @classmethod
    def validate_sale_date(cls, value: str, info):
        return valid_date(value, info.field_name)


class CashewShellSalesDeleteRequest(BaseModel):
    id: int

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: int, info):
        return positive_int(value, info.field_name)


class CashewShellSalesFetchByBatchNumberRequest(BaseModel):
    batch_number: str

    @field_validator("batch_number")
    @classmethod
    def validate_batch_number(cls, value: str, info):
        return not_empty(value, info.field_name)


class CashewShellSalesResponse(BaseModel):
    id: int
    sale_date: str
    bill_number: str
    customer_name: str
    batch_number: Optional[str]
    quantity_kg: Optional[float]
    price_per_kg: Optional[float]
    total_amount: Optional[float]
    created_by: Optional[str]
    updated_by: Optional[str]
    is_deleted: Optional[bool] = False
    created_at: Optional[str]
    updated_at: Optional[str]
