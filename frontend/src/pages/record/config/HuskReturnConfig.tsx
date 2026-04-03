import type { FormField } from "../../../types/FormField";
import { Sell } from "@mui/icons-material";

export const fields: FormField[] = [
  { name: "date", label: "Date", type: "date", required: true },
  { name: "batch_number", label: "Batch No", type: "text", required: true },
  {
    name: "wholes_kg",
    label: "Wholes (kg)",
    type: "number",
    required: true,
    step: 0.01,
  },
  {
    name: "pieces_kg",
    label: "Pieces (kg)",
    type: "number",
    required: true,
    step: 0.01,
  },
  {
    name: "unpeeled_kg",
    label: "Unpeeled (kg)",
    type: "number",
    required: true,
    step: 0.01,
  },
  {
    name: "swp_kg",
    label: "SWP (kg)",
    type: "number",
    required: true,
    step: 0.01,
  },
  {
    name: "bb_kg",
    label: "BB (kg)",
    type: "number",
    required: true,
    step: 0.01,
  },
  {
    name: "rejection_kg",
    label: "Rejection (kg)",
    type: "number",
    required: true,
    step: 0.01,
  },
  {
    name: "cutting_pieces_kg",
    label: "Cutting Pieces (kg)",
    type: "number",
    required: true,
    step: 0.01,
  },
  {
    name: "total_quantity_kg",
    label: "Total (kg)",
    type: "number",
    required: true,
    step: 0.01,
    compute: (values) => {
      const q = parseFloat(values.wholes_kg) || 0;
      const p = parseFloat(values.pieces_kg) || 0;
      const r = parseFloat(values.unpeeled_kg) || 0;
      const s = parseFloat(values.swp_kg) || 0;
      const t = parseFloat(values.bb_kg) || 0;
      const u = parseFloat(values.rejection_kg) || 0;
      const v = parseFloat(values.cutting_pieces_kg) || 0;
      return +(q + p + r + s + t + u + v).toFixed(2);
    },
  },
];

export const huskReturnPageMeta = {
  title: "Husk Return",
  subtitle: "Add Husk return records",
  icon: <Sell fontSize="medium" sx={{ color: "#cc6600" }} />,
};
