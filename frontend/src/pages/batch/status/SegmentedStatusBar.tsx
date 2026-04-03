// src/pages/batch/status/SegmentedStatusBar.tsx
import React, { useState } from "react";
import {
  Box,
  Tooltip,
  IconButton,
  Popover,
  MenuItem,
  Chip,
} from "@mui/material";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import {
  stageLabels,
  statusColors,
  type BatchStageMap,
  type Stage,
  type Status,
} from "./types";

export function SegmentedStatusBar({
  value,
  onChange,
  readOnly = false,
}: {
  value: BatchStageMap;
  onChange: (next: BatchStageMap) => void;
  readOnly?: boolean;
}) {
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);
  const [activeStage, setActiveStage] = useState<Stage | null>(null);

  const handleOpen = (e: React.MouseEvent<HTMLElement>, stage: Stage) => {
    if (readOnly) return;
    setAnchorEl(e.currentTarget);
    setActiveStage(stage);
  };

  const handleClose = () => {
    setAnchorEl(null);
    setActiveStage(null);
  };

  const setStatus = (s: Status) => {
    if (!activeStage) return;
    const next = {
      ...value,
      [activeStage]: { ...value[activeStage], status: s },
    };
    onChange(next);
    handleClose();
  };

  return (
    <Box display="flex" gap={1} alignItems="center">
      <Box display="flex" gap={6} flex={1}>
        {Object.keys(stageLabels).map((k) => {
          const stage = k as Stage;
          const { status, updated_at, updated_by_name } = value[stage];
          const label = stageLabels[stage];
          const color = statusColors[status];

          return (
            <Box key={stage} width="100%">
              <Tooltip
                title={
                  <Box>
                    <Box fontWeight={600}>{label}</Box>
                    <Box>Status: {status}</Box>
                    {updated_at && (
                      <Box>
                        Last updated: {new Date(updated_at).toLocaleString()}
                      </Box>
                    )}
                    {updated_by_name && <Box>By: {updated_by_name}</Box>}
                  </Box>
                }
                arrow
              >
                <Box
                  role="button"
                  aria-label={`${label} status: ${status}`}
                  onClick={(e) => handleOpen(e as any, stage)}
                  sx={{
                    height: 24,
                    borderRadius: 6,
                    backgroundColor: color,
                    cursor: readOnly ? "default" : "pointer",
                    boxShadow: "inset 0 0 0 1px rgba(0,0,0,0.08)",
                  }}
                />
              </Tooltip>

              <Box mt={0.5} display="flex" alignItems="center" gap={0.5}>
                <Chip size="small" label={label} />
                {!readOnly && (
                  <IconButton
                    aria-label={`Change ${label} status`}
                    size="small"
                    onClick={(e) => handleOpen(e, stage)}
                  >
                    <ArrowDropDownIcon fontSize="small" />
                  </IconButton>
                )}
                {updated_at && (
                  <Tooltip
                    title={`Last: ${new Date(updated_at).toLocaleString()}`}
                  >
                    <InfoOutlinedIcon sx={{ fontSize: 16, opacity: 0.7 }} />
                  </Tooltip>
                )}
              </Box>
            </Box>
          );
        })}
      </Box>

      <Popover
        open={Boolean(anchorEl)}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "left" }}
      >
        <Box p={1}>
          {(["Not_Started", "In_Progress", "Completed"] as Status[]).map(
            (s) => (
              <MenuItem key={s} onClick={() => setStatus(s)}>
                <Box
                  width={12}
                  height={12}
                  borderRadius="50%"
                  mr={1}
                  sx={{ backgroundColor: statusColors[s] }}
                />
                {s.replace("_", " ")}
              </MenuItem>
            )
          )}
        </Box>
      </Popover>
    </Box>
  );
}
