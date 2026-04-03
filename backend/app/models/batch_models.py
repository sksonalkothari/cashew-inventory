from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.validators.common_validators import not_empty, valid_date

class BatchCreateModel(BaseModel):
    batch_number: str = Field(..., description="Batch number")
    origin: Optional[str] = Field(None, description="Origin")
    batch_entry_date: str = Field(..., description="Date in YYYY-MM-DD format")

    @field_validator("batch_number")
    @classmethod
    def validate_batch_number(cls, value: str, info):
        return not_empty(value, info.field_name)

    @field_validator("batch_entry_date")
    @classmethod
    def validate_batch_entry_date(cls, value: str, info):
        return valid_date(value, info.field_name)
    
class BatchUpdateModel(BaseModel):
    batch_number: str = Field(..., description="Batch number")
    purchase_status: Optional[str] = Field(None, description="Purchase stage status")
    boiling_status: Optional[str] = Field(None, description="Boiling stage status")
    nw_drying_status: Optional[str] = Field(None, description="NW Drying stage status")
    nw_humidification_status: Optional[str] = Field(None, description="NW Humidification stage status")
    peeling_before_drying_status: Optional[str] = Field(None, description="Peeling Before Drying stage status")
    peeling_after_drying_status: Optional[str] = Field(None, description="Peeling After Drying stage status")
    production_status: Optional[str] = Field(None, description="Production stage status")
    cashew_kernel_sales_status: Optional[str] = Field(None, description="Cashew Kernel Sales stage status")
    rcn_sales_status: Optional[str] = Field(None, description="RCN Sales stage status")

    @field_validator("batch_number")
    @classmethod
    def validate_batch_number(cls, value: str, info):
        return not_empty(value, info.field_name)
    
class InProgressBatchQueryModel(BaseModel):
    stage: str = Field(..., description="Stage name, e.g. 'purchase', 'boiling', etc.")
    
    @field_validator("stage")
    @classmethod    
    def validate_stage(cls, value: str, info):
        return not_empty(value, info.field_name)
    