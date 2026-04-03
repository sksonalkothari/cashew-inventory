CREATE TABLE IF NOT EXISTS peeling_after_drying (
  id SERIAL PRIMARY KEY,
  peeling_date DATE NOT NULL,
  batch_number TEXT REFERENCES batch_summary(batch_number),

  wholes_kg NUMERIC(10,2) DEFAULT 0,
  pieces_kg NUMERIC(10,2) DEFAULT 0,
  unpeeled_kg NUMERIC(10,2) DEFAULT 0,
  swp_kg NUMERIC(10,2) DEFAULT 0,
  bb_kg NUMERIC(10,2) DEFAULT 0,
  rejection_kg NUMERIC(10,2) DEFAULT 0,
  cutting_pieces_kg NUMERIC(10,2) DEFAULT 0,

  total_quantity_kg NUMERIC(10,2) GENERATED ALWAYS AS (
    wholes_kg + pieces_kg + unpeeled_kg + swp_kg + bb_kg +
    rejection_kg + cutting_pieces_kg
  ) STORED,

  decrease_kg NUMERIC(10,2),
  decrease_percent NUMERIC(5,2),

  created_by UUID REFERENCES users(id),
  updated_by UUID REFERENCES users(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP
);