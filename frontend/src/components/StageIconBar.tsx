import React from "react";
import { Tooltip, Box } from "@mui/material";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import LocalFireDepartmentIcon from "@mui/icons-material/LocalFireDepartment";
import WaterDropIcon from "@mui/icons-material/WaterDrop";
import FactoryIcon from "@mui/icons-material/Factory";
import { type BatchStageMap, type Stage } from "../pages/batch/status/types";
import { ContentCut, Layers, Sell, WbSunny } from "@mui/icons-material";

const stageIcons: Record<Stage, React.ReactNode> = {
  purchase: <ShoppingCartIcon fontSize="small" />,
  boiling: <LocalFireDepartmentIcon fontSize="small" />,
  nw_drying: <WbSunny fontSize="small" />,
  nw_humidification: <WaterDropIcon fontSize="small" />,
  peeling_before_drying: <ContentCut fontSize="small" />,
  peeling_after_drying: <Layers fontSize="small" />,
  production: <FactoryIcon fontSize="small" />,
  cashew_kernel_sales: <Sell fontSize="small" />,
};

const statusColors: Record<string, string> = {
  Not_Started: "#ccc",
  In_Progress: "#f2c94c",
  Completed: "#27ae60",
};

export const StageIconBar: React.FC<{ stages: BatchStageMap }> = ({
  stages,
}) => {
  return (
    <Box display="flex" gap={1}>
      {Object.entries(stages).map(
        ([key, { status, updated_at, updated_by_name }]) => {
          const stage = key as Stage;
          const icon = stageIcons[stage];
          const color = statusColors[status];

          const tooltip = `${stage}: ${status.replace("_", " ")}${
            updated_at
              ? `\nUpdated: ${new Date(updated_at).toLocaleString()}`
              : ""
          }${updated_by_name ? `\nBy: ${updated_by_name}` : ""}`;

          return (
            <Tooltip key={stage} title={tooltip} arrow>
              <Box
                sx={{
                  backgroundColor: color,
                  borderRadius: "50%",
                  padding: 0.5,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  width: 28,
                  height: 28,
                }}
              >
                {icon}
              </Box>
            </Tooltip>
          );
        }
      )}
    </Box>
  );
};
