CREATE TABLE IF NOT EXISTS boiling (
  id SERIAL PRIMARY KEY,
  boiling_date DATE NOT NULL,
  batch_number TEXT REFERENCES batch_summary(batch_number),
  quantity_kg NUMERIC(10,2) NOT NULL,
  created_by UUID REFERENCES users(id),
  updated_by UUID REFERENCES users(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP
);