CREATE INDEX IF NOT EXISTS idx_drying_batch_number ON drying (batch_number);
CREATE INDEX IF NOT EXISTS idx_drying_created_by ON drying (created_by);
CREATE INDEX IF NOT EXISTS idx_drying_updated_by ON drying (updated_by);