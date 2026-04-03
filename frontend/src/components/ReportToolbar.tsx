// src/components/ReportToolbar.tsx
import React, { useEffect, useRef } from "react";
import { Box, IconButton, TextField, Tooltip } from "@mui/material";
import { Download, Search, DateRange } from "@mui/icons-material";
import PageHeader from "./PageHeader";

type Props = {
  title?: string;
  subtitle?: string;
  icon?: React.ReactNode;
  color?: string;
  globalSearch: string;
  onGlobalSearch: (value: string) => void;
  onExport: () => void;
  showTimeWindow: boolean;
  onToggleTimeWindow: () => void;
  showSearch: boolean;
  setShowSearch: (open: boolean) => void;
};

export const ReportToolbar: React.FC<Props> = ({
  title,
  subtitle,
  icon,
  color,
  globalSearch,
  onGlobalSearch,
  onExport,
  showTimeWindow,
  onToggleTimeWindow,
  showSearch,
  setShowSearch,
}) => {
  const hasSearch = globalSearch.length > 0;
  const searchRef = useRef<HTMLDivElement>(null);

  // Collapse when clicking outside if empty
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        searchRef.current &&
        !searchRef.current.contains(event.target as Node) &&
        !hasSearch
      ) {
        setShowSearch(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [hasSearch, setShowSearch]);

  const containedIconStyle = {
    backgroundColor: "primary.main",
    color: "white",
    "&:hover": { backgroundColor: "primary.dark" },
  };

  return (
    <Box
      sx={{
        mb: 1,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        margin: 0,
      }}
    >
      <PageHeader title={title} subtitle={subtitle} icon={icon} color={color} />

      <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
        <Box ref={searchRef}>
          {showSearch || hasSearch ? (
            <TextField
              size="small"
              placeholder="Search..."
              value={globalSearch}
              onChange={(e) => onGlobalSearch(e.target.value)}
              sx={{ width: 200 }}
            />
          ) : (
            <Tooltip title="Search">
              <IconButton
                onClick={() => setShowSearch(true)}
                sx={{ color: "primary.main" }}
              >
                <Search />
              </IconButton>
            </Tooltip>
          )}
        </Box>

        <Tooltip title="Export CSV">
          <IconButton onClick={onExport} sx={{ color: "primary.main" }}>
            <Download />
          </IconButton>
        </Tooltip>

        <Tooltip title="Select time range">
          <IconButton
            onClick={onToggleTimeWindow}
            sx={showTimeWindow ? containedIconStyle : { color: "primary.main" }}
          >
            <DateRange />
          </IconButton>
        </Tooltip>
      </Box>
    </Box>
  );
};
