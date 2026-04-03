CREATE INDEX IF NOT EXISTS idx_boiling_batch_number ON boiling (batch_number);
CREATE INDEX IF NOT EXISTS idx_boiling_created_by ON boiling (created_by);
CREATE INDEX IF NOT EXISTS idx_boiling_updated_by ON boiling (updated_by);