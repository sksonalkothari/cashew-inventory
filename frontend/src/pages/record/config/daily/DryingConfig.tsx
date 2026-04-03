import { WbSunny } from "@mui/icons-material";
import type { FormField } from "../../../../types/FormField";

export const fields: FormField[] = [
  { name: "date", label: "Date", type: "date", required: true },
  {
    name: "batch_number",
    label: "Batch No",
    type: "batch_select",
    required: true,
    stage: "nw_drying",
  },
  {
    name: "nw_wholes_in_kg",
    label: "IN (kg)",
    type: "number",
    required: true,
    step: 0.01,
    group: "NW Wholes",
  },
  {
    name: "nw_wholes_out_kg",
    label: "OUT (kg)",
    type: "number",
    required: true,
    step: 0.01,
    group: "NW Wholes",
  },
  {
    name: "nw_pieces_in_kg",
    label: "IN (kg)",
    type: "number",
    required: true,
    step: 0.01,
    group: "NW Pieces",
  },
  {
    name: "nw_pieces_out_kg",
    label: "OUT (kg)",
    type: "number",
    required: true,
    step: 0.01,
    group: "NW Pieces",
  },
  {
    name: "nw_rejection_in_kg",
    label: "IN (kg)",
    type: "number",
    required: true,
    step: 0.01,
    group: "NW Rejection",
  },
  {
    name: "nw_rejection_out_kg",
    label: "OUT (kg)",
    type: "number",
    required: true,
    step: 0.01,
    group: "NW Rejection",
  },
  {
    name: "moisture_loss",
    label: "Moisture Loss",
    type: "number",
    required: true,
    step: 0.01,
  },
];

export const dryingPageMeta = {
  title: "Drying Process",
  subtitle: "Add daily drying records",
  icon: <WbSunny fontSize="medium" sx={{ color: "#cc6600" }} />,
};
