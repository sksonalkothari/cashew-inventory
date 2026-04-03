CREATE TABLE IF NOT EXISTS production (
  id SERIAL PRIMARY KEY,
  production_date DATE NOT NULL,
  grade_id INTEGER REFERENCES grades(id),
  batch_number TEXT REFERENCES batch_summary(batch_number),

  shape TEXT CHECK (shape IN ('Wholes', 'Pieces')),
  processing TEXT CHECK (processing IN ('Normal', 'Dysing', 'Hand Peeled')),
  packaging TEXT CHECK (packaging IN ('13 inch Tin', '14 inch Tin', 'Corrugated Box')),

  quantity_in_tin NUMERIC(10,2) DEFAULT 0,

  created_by UUID REFERENCES public.users(id),
  updated_by UUID REFERENCES public.users(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP
);