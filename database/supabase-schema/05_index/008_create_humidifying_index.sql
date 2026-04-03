CREATE INDEX IF NOT EXISTS idx_humidifying_batch_number ON humidifying (batch_number);
CREATE INDEX IF NOT EXISTS idx_humidifying_created_by ON humidifying (created_by);
CREATE INDEX IF NOT EXISTS idx_humidifying_updated_by ON humidifying (updated_by);