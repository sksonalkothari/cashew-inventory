CREATE INDEX IF NOT EXISTS idx_husk_rejection_sales_batch_number ON husk_rejection_sales (batch_number);
CREATE INDEX IF NOT EXISTS idx_husk_rejection_sales_created_by ON husk_rejection_sales (created_by);
CREATE INDEX IF NOT EXISTS idx_husk_rejection_sales_updated_by ON husk_rejection_sales (updated_by);