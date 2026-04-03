CREATE INDEX IF NOT EXISTS idx_purchases_batch_number ON purchases (batch_number);
CREATE INDEX IF NOT EXISTS idx_purchases_created_by ON purchases (created_by);
CREATE INDEX IF NOT EXISTS idx_purchases_updated_by ON purchases (updated_by);