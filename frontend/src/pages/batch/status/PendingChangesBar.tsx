// src/pages/batch/status/PendingChangesBar.tsx
import { Box, Button } from "@mui/material";

export function PendingChangesBar({
  dirtyCount,
  onSubmit,
  onDiscard,
  disabled,
}: {
  dirtyCount: number;
  onSubmit: () => void;
  onDiscard: () => void;
  disabled?: boolean;
}) {
  if (dirtyCount === 0) return null;

  return (
    <Box
      position="sticky"
      bottom={0}
      zIndex={10}
      bgcolor="#fff"
      borderTop="1px solid #eee"
      p={1.5}
      display="flex"
      justifyContent="space-between"
      alignItems="center"
    >
      <Box fontWeight={600}>{dirtyCount} change(s) pending</Box>
      <Box display="flex" gap={1}>
        <Button variant="outlined" onClick={onDiscard}>
          Discard
        </Button>
        <Button variant="contained" onClick={onSubmit} disabled={disabled}>
          Submit
        </Button>
      </Box>
    </Box>
  );
}
