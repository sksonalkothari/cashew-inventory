// src/components/ErrorFallback.tsx
import { useRouteError } from "react-router-dom";
import { Box, Typography, Button } from "@mui/material";

export default function ErrorFallback() {
  const error = useRouteError();
  console.error("Route error:", error);

  return (
    <Box p={4} textAlign="center">
      <Typography variant="h5" color="error" gutterBottom>
        Something went wrong.
      </Typography>
      <Typography variant="body2" color="text.secondary" mb={2}>
        We couldn’t load this page. Please try again or contact support.
      </Typography>
      <Button variant="contained" onClick={() => window.location.reload()}>
        Reload Page
      </Button>
    </Box>
  );
}
