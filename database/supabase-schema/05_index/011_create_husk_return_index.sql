CREATE INDEX IF NOT EXISTS idx_husk_return_batch_number ON husk_return (batch_number);
CREATE INDEX IF NOT EXISTS idx_husk_return_created_by ON husk_return (created_by);
CREATE INDEX IF NOT EXISTS idx_husk_return_updated_by ON husk_return (updated_by);