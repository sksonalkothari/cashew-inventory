CREATE TABLE IF NOT EXISTS purchases (
  id SERIAL PRIMARY KEY,
  purchase_date DATE NOT NULL,
  supplier_name TEXT NOT NULL,
  bill_number TEXT NOT NULL,
  origin TEXT,
  batch_number TEXT REFERENCES batch_summary(batch_number),
  quantity_kg NUMERIC(10,2) NOT NULL,
  price_per_kg NUMERIC(10,2) NOT NULL,
  total_amount numeric(12, 2) null,
  created_by UUID REFERENCES users(id),
  updated_by UUID REFERENCES users(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP
);