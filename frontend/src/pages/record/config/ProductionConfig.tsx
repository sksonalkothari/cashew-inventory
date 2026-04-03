import type { FormField } from "../../../types/FormField";
import { Factory } from "@mui/icons-material";

export const fields: FormField[] = [
  { name: "date", label: "Date", type: "date", required: true },
  {
    name: "grade_id",
    label: "Grade",
    type: "select",
    required: true,
  },
  {
    name: "batch_number",
    label: "Batch No",
    type: "batch_select",
    required: true,
    stage: "production",
  },
  {
    name: "shape",
    label: "Shape",
    type: "select",
    required: true,
    options: [
      { label: "Wholes", value: "Wholes" },
      { label: "Pieces", value: "Pieces" },
    ],
  },
  {
    name: "processing",
    label: "Processing",
    type: "select",
    required: true,
    options: [
      { label: "Normal", value: "Normal" },
      { label: "Dysing", value: "Dysing" },
      { label: "Hand Peeled", value: "Hand Peeled" },
    ],
  },
  {
    name: "packaging",
    label: "Packaging",
    type: "select",
    required: true,
    options: [
      { label: "13 inch Tin", value: "13 inch Tin" },
      { label: "14 inch Tin", value: "14 inch Tin" },
      { label: "Corrugated Box", value: "Corrugated Box" },
    ],
  },
  {
    name: "quantity_in_tin",
    label: "Quantity (Tin)",
    type: "number",
    required: true,
    step: 0,
  },
];

export const productionPageMeta = {
  title: "Production",
  subtitle: "Add production records",
  icon: <Factory fontSize="medium" sx={{ color: "#cc6600" }} />,
};
