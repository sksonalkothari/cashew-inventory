CREATE INDEX IF NOT EXISTS idx_cashew_kernel_sales_grade_id ON cashew_kernel_sales (grade_id);
CREATE INDEX IF NOT EXISTS idx_cashew_kernel_sales_batch_number ON cashew_kernel_sales (batch_number);
CREATE INDEX IF NOT EXISTS idx_cashew_kernel_sales_created_by ON cashew_kernel_sales (created_by);
CREATE INDEX IF NOT EXISTS idx_cashew_kernel_sales_updated_by ON cashew_kernel_sales (updated_by);