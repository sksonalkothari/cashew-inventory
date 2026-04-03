// src/pages/batch/BatchListTest.tsx
import React from "react";
import { Box, Typography, Divider } from "@mui/material";
import { SegmentedStatusBar } from "./status/SegmentedStatusBar";
import { mockBatchList } from "./status/mockListData";

const BatchListTest: React.FC = () => {
  return (
    <Box p={2}>
      <Typography variant="h5" gutterBottom>
        Mock Batch List
      </Typography>
      {mockBatchList.map((batch) => (
        <Box key={batch.batchNumber} mb={3}>
          <Typography variant="subtitle1">
            {batch.batchNumber} — {batch.origin} (Intake: {batch.intake_date})
          </Typography>
          <SegmentedStatusBar
            value={batch.stages}
            onChange={(next) =>
              console.log("Changed:", batch.batchNumber, next)
            }
          />
          <Divider sx={{ mt: 2 }} />
        </Box>
      ))}
    </Box>
  );
};

export default BatchListTest;
