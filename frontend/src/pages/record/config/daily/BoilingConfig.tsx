import LocalFireDepartmentIcon from "@mui/icons-material/LocalFireDepartment";
import type { FormField } from "../../../../types/FormField";

export const fields: FormField[] = [
  { name: "date", label: "Date", type: "date", required: true },
  {
    name: "batch_number",
    label: "Batch No",
    type: "batch_select",
    required: true,
    stage: "boiling",
  },
  {
    name: "quantity_kg",
    label: "Quantity (kg)",
    type: "number",
    required: true,
    step: 0, // default value, only integers allowed
  },
];

export const boilingPageMeta = {
  title: "Boiling Process",
  subtitle: "Add daily boiling records",
  icon: <LocalFireDepartmentIcon fontSize="medium" sx={{ color: "#cc6600" }} />,
};
