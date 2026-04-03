CREATE INDEX IF NOT EXISTS idx_batch_summary_status ON batch_summary (status);
CREATE INDEX IF NOT EXISTS idx_batch_summary_created_by ON batch_summary (created_by);
CREATE INDEX IF NOT EXISTS idx_batch_summary_updated_by ON batch_summary (updated_by);