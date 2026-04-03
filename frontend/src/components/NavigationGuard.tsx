import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
} from "@mui/material";
import { useNavigationGuard } from "../hooks/useNavigationGuard";

interface NavigationGuardProps {
  shouldBlock: boolean;
}

const NavigationGuard: React.FC<NavigationGuardProps> = ({ shouldBlock }) => {
  const { showDialog, confirmNavigation, cancelNavigation } =
    useNavigationGuard(shouldBlock);

  return (
    <Dialog open={showDialog}>
      <DialogTitle
        sx={{
          bgcolor: "#fff3e0", // soft amber
          color: "#e65100", // deep orange
          fontWeight: 600,
          fontSize: "1.1rem",
        }}
      >
        Unsaved Changes
      </DialogTitle>

      <DialogContent
        sx={{
          bgcolor: "#fff8e1", // lighter amber
          color: "#5d4037", // muted brown
          fontSize: "0.95rem",
        }}
      >
        <Typography>
          You have pending records. They will be lost if not submitted.
        </Typography>
      </DialogContent>

      <DialogActions
        sx={{
          bgcolor: "#fff3e0",
          padding: "12px 24px",
        }}
      >
        <Button
          onClick={cancelNavigation}
          variant="outlined"
          color="inherit"
          sx={{
            borderColor: "#e65100",
            color: "#e65100",
            "&:hover": {
              backgroundColor: "#ffe0b2",
            },
          }}
        >
          No, Stay Here
        </Button>

        <Button
          onClick={confirmNavigation}
          variant="contained"
          sx={{
            backgroundColor: "#e65100",
            color: "#fff",
            "&:hover": {
              backgroundColor: "#d84315",
            },
          }}
          autoFocus
        >
          Yes, Leave Page
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default NavigationGuard;
