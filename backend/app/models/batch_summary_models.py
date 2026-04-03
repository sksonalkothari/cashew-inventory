from pydantic import BaseModel
from typing import Optional

class BatchSummaryMetadata(BaseModel):
    batch_number: str
    purchase_quantity: float
    boiling_quantity: float
    drying_quantity: float
    humidifying_quantity: float
    peeling_before_drying_qty: float
    peeling_after_drying_qty: float
    husk_return_quantity: float
    packaged_quantity: float
    sales_quantity: float
    status: Optional[str]
    origin: Optional[str]
    created_by: Optional[str]
    updated_by: Optional[str]
    is_deleted: Optional[bool] = False
    created_at: Optional[str]
    updated_at: Optional[str]

class UnsoldBatchesResponse(BaseModel):
    batch_number: str
    status: Optional[str]
    origin: Optional[str]