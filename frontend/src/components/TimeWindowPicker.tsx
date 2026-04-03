// src/components/TimeWindowPicker.tsx
import React from "react";
import { Box, Button, TextField } from "@mui/material";

type Props = {
  dateFrom?: string;
  dateTo?: string;
  onChange: (next: { dateFrom?: string; dateTo?: string }) => void;
};

function isoDate(d: Date) {
  return d.toISOString().slice(0, 10);
}

export const TimeWindowPicker: React.FC<Props> = ({
  dateFrom,
  dateTo,
  onChange,
}) => {
  const today = new Date();
  const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
  const startOfYear = new Date(today.getFullYear(), 0, 1);
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);
  const last7 = new Date(today);
  last7.setDate(today.getDate() - 6);
  const last30 = new Date(today);
  last30.setDate(today.getDate() - 29);

  return (
    <Box sx={{ display: "flex", gap: 2, alignItems: "center" }}>
      <TextField
        label="From"
        type="date"
        size="small"
        value={dateFrom ?? ""}
        onChange={(e) => onChange({ dateFrom: e.target.value, dateTo })}
        InputLabelProps={{ shrink: true }}
      />
      <TextField
        label="To"
        type="date"
        size="small"
        value={dateTo ?? ""}
        onChange={(e) => onChange({ dateFrom, dateTo: e.target.value })}
        InputLabelProps={{ shrink: true }}
      />
      <Box sx={{ display: "flex", gap: 1 }}>
        <Button
          variant="outlined"
          size="small"
          onClick={() =>
            onChange({ dateFrom: isoDate(last7), dateTo: isoDate(today) })
          }
        >
          Last 7 days
        </Button>
        <Button
          variant="outlined"
          size="small"
          onClick={() =>
            onChange({ dateFrom: isoDate(last30), dateTo: isoDate(today) })
          }
        >
          Last 30 days
        </Button>
        <Button
          variant="outlined"
          size="small"
          onClick={() =>
            onChange({
              dateFrom: isoDate(startOfMonth),
              dateTo: isoDate(today),
            })
          }
        >
          This month
        </Button>
        <Button
          variant="outlined"
          size="small"
          onClick={() =>
            onChange({ dateFrom: isoDate(startOfYear), dateTo: isoDate(today) })
          }
        >
          This year
        </Button>
        <Button
          variant="text"
          size="small"
          onClick={() => onChange({ dateFrom: undefined, dateTo: undefined })}
        >
          Clear
        </Button>
      </Box>
    </Box>
  );
};
