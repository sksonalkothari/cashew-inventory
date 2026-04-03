import React, { useEffect, useState } from "react";
import { TextField, MenuItem, CircularProgress } from "@mui/material";
import {
  fetchInProgressBatchesByStage,
  type BatchListItem,
} from "../api/batch";

interface BatchSelectProps {
  value: string;
  onChange: (value: string) => void;
  stage: string;
  label?: string;
  required?: boolean;
  disabled?: boolean;
  sx?: any;
}

const BatchSelect: React.FC<BatchSelectProps> = ({
  value,
  onChange,
  stage,
  label = "Batch Number",
  required = false,
  disabled = false,
  sx = {},
}) => {
  const [batches, setBatches] = useState<BatchListItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetchInProgressBatchesByStage(stage)
      .then((data) => {
        setBatches(data);
        setLoading(false);
      })
      .catch(() => {
        setBatches([]);
        setLoading(false);
      });
  }, [stage]);

  return loading ? (
    <CircularProgress size={24} sx={{ mt: 1, mb: 1 }} />
  ) : (
    <TextField
      select
      label={label}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      fullWidth
      required={required}
      disabled={disabled}
      variant="outlined"
      size="small"
      sx={{ minWidth: 180, ...sx }}
      slotProps={{ inputLabel: { shrink: true } }}
    >
      {batches.map((batch) => (
        <MenuItem
          key={batch.batchNumber}
          value={batch.batchNumber}
          sx={{ fontSize: 14 }}
        >
          {batch.batchNumber}
        </MenuItem>
      ))}
    </TextField>
  );
};

export default BatchSelect;
