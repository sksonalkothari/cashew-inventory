import React, { useState } from "react";
import { Drawer, Box, Divider, Button, IconButton } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { StageStatusEditor } from "./StageStatusEditor";
import {
  type BatchStageMap,
  type Stage,
  type Status,
} from "../pages/batch/status/types";
import PageHeader from "./PageHeader";

export const UpdateStatusDrawer: React.FC<{
  open: boolean;
  onClose: () => void;
  batchNumber: string;
  initialStages: BatchStageMap;
  onSubmit: (updated: BatchStageMap) => void;
}> = ({ open, onClose, batchNumber, initialStages, onSubmit }) => {
  const [stages, setStages] = useState<BatchStageMap>(initialStages);

  const handleChange = (stage: Stage, next: Status) => {
    setStages((prev) => ({
      ...prev,
      [stage]: {
        ...prev[stage],
        status: next,
      },
    }));
  };

  const handleSubmit = () => {
    onSubmit(stages);
    onClose();
  };

  const handleCancel = () => {
    setStages(initialStages);
    onClose();
  };

  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={onClose}
      PaperProps={{
        sx: { mt: "50px", height: "calc(100% - 50px)" },
      }}
    >
      <Box width={360} p={2}>
        <Box
          display="flex"
          justifyContent="space-between"
          alignItems="center"
          mb={2}
        >
          <PageHeader title="Update Status" subtitle={batchNumber} />
          <IconButton onClick={onClose}>
            <CloseIcon />
          </IconButton>
        </Box>

        <Divider sx={{ mb: 2 }} />

        {Object.entries(stages).map(([key, value]) => (
          <StageStatusEditor
            key={key}
            stage={key as Stage}
            status={value.status}
            updated_at={value.updated_at}
            updated_by_name={value.updated_by_name}
            onChange={(next) => handleChange(key as Stage, next)}
          />
        ))}

        <Divider sx={{ mt: 2, mb: 2 }} />

        <Box display="flex" justifyContent="space-between">
          <Button variant="outlined" onClick={handleCancel}>
            Cancel
          </Button>
          <Button variant="contained" onClick={handleSubmit}>
            Submit
          </Button>
        </Box>
      </Box>
    </Drawer>
  );
};
