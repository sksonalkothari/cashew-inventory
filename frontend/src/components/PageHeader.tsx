// src/components/PageHeader.tsx
import { Box, Typography } from "@mui/material";
import { type ReactNode } from "react";

interface PageHeaderProps {
  title?: string;
  subtitle?: string;
  icon?: ReactNode;
  color?: string; // optional custom color
}

const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  subtitle,
  icon,
  color,
}) => {
  return (
    <Box sx={{ mb: 2 }}>
      <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
        {icon}
        <Typography
          variant="h6"
          fontWeight={600}
          lineHeight={1.3}
          sx={{ color: color || "#cc6600" }} // default to brownish-orange
        >
          {title}
        </Typography>
      </Box>
      {subtitle && (
        <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
          {subtitle}
        </Typography>
      )}
    </Box>
  );
};

export default PageHeader;
