import React from "react";
import {
  Box,
  Typography,
  Select,
  MenuItem,
  Tooltip,
  FormControl,
} from "@mui/material";
import {
  stageLabels,
  statusColors,
  type Stage,
  type Status,
} from "../pages/batch/status/types";

export const StageStatusEditor: React.FC<{
  stage: Stage;
  status: Status;
  updated_at?: string | null;
  updated_by_name?: string | null;
  onChange: (next: Status) => void;
}> = ({ stage, status, updated_at, updated_by_name, onChange }) => {
  const label = stageLabels[stage];
  const tooltip = `${label}: ${status.replace("_", " ")}${
    updated_at ? `\nUpdated: ${new Date(updated_at).toLocaleString()}` : ""
  }${updated_by_name ? `\nBy: ${updated_by_name}` : ""}`;

  return (
    <Box
      display="flex"
      alignItems="center"
      justifyContent="space-between"
      mb={2}
    >
      <Tooltip title={tooltip} arrow>
        <Typography fontWeight={600}>{label}</Typography>
      </Tooltip>

      <FormControl size="small" sx={{ minWidth: 140 }}>
        <Select
          value={status}
          label="Status"
          onChange={(e) => onChange(e.target.value as Status)}
          sx={{ backgroundColor: statusColors[status], color: "#fff" }}
        >
          <MenuItem value="Not_Started">Not Started</MenuItem>
          <MenuItem value="In_Progress">In Progress</MenuItem>
          <MenuItem value="Completed">Completed</MenuItem>
        </Select>
      </FormControl>
    </Box>
  );
};
