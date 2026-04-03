import React, { useState } from "react";
import { Box, Typography, Button, Paper } from "@mui/material";
import { StageIconBar } from "./StageIconBar";
import { type BatchStageMap } from "../pages/batch/status/types";
import { UpdateStatusDrawer } from "./UpdateStatusDrawer";
import { updateBatch } from "../api/batch";

export const BatchCardRow: React.FC<{
  batchNumber: string;
  origin: string;
  intake_date: string;
  stages: BatchStageMap;
  onUpdated?: () => void;
}> = ({ batchNumber, origin, intake_date, stages, onUpdated }) => {
  const completedCount = Object.values(stages).filter(
    (s) => s.status === "Completed"
  ).length;

  const [drawerOpen, setDrawerOpen] = useState(false);

  const handleSubmit = async (updated: BatchStageMap) => {
    try {
      const payload = {
        batch_number: batchNumber,
        ...Object.fromEntries(
          Object.entries(updated).map(([stage, { status }]) => [
            `${stage}_status`,
            status,
          ])
        ),
      };

      await updateBatch(payload);
      console.log("Batch updated successfully:", payload);
      onUpdated?.();
    } catch (err) {
      console.error("Failed to update batch:", err);
    }
  };

  return (
    <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
      <Box
        display="grid"
        gridTemplateColumns="1fr 1.25fr auto" // 👈 3 fixed columns
        alignItems="center"
        gap={2}
      >
        {/* Column 1: Batch info */}
        <Box>
          <Typography variant="subtitle2" fontWeight={600}>
            {batchNumber}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            {origin} — Intake: {intake_date}
          </Typography>
        </Box>

        {/* Column 2: Stage icons */}
        <StageIconBar stages={stages} />

        {/* Column 3: Progress + Update button */}
        <Box display="flex" alignItems="center" gap={2}>
          <Typography variant="body2" color="warning.main" fontWeight={600}>
            {completedCount}/8 Completed
          </Typography>
          <Button
            variant="outlined"
            size="small"
            onClick={() => setDrawerOpen(true)}
          >
            Update Status
          </Button>
        </Box>
      </Box>

      <UpdateStatusDrawer
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        batchNumber={batchNumber}
        initialStages={stages}
        onSubmit={handleSubmit}
      />
    </Paper>
  );
};
