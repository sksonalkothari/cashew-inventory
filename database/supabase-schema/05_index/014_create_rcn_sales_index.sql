CREATE INDEX IF NOT EXISTS idx_rcn_sales_batch_number ON rcn_sales (batch_number);
CREATE INDEX IF NOT EXISTS idx_rcn_sales_created_by ON rcn_sales (created_by);
CREATE INDEX IF NOT EXISTS idx_rcn_sales_updated_by ON rcn_sales (updated_by);