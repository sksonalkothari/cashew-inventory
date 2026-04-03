CREATE INDEX IF NOT EXISTS idx_production_grade_id ON production (grade_id);
CREATE INDEX IF NOT EXISTS idx_production_batch_number ON production (batch_number);
CREATE INDEX IF NOT EXISTS idx_production_created_by ON production (created_by);
CREATE INDEX IF NOT EXISTS idx_production_updated_by ON production (updated_by);