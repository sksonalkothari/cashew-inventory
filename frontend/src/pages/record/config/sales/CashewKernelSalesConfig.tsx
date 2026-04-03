import type { FormField } from "../../../../types/FormField";
import { Sell } from "@mui/icons-material";

export const fields: FormField[] = [
  { name: "date", label: "Date", type: "date", required: true },
  { name: "bill_number", label: "Bill No.", type: "text", required: true },
  { name: "customer_name", label: "Name", type: "text", required: true },
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
    stage: "cashew_kernel_sales",
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
    name: "quantity_in_tin",
    label: "Quantity (Tin)",
    type: "number",
    required: true,
    step: 0,
  },
  {
    name: "price_per_tin",
    label: "Price (₹/Tin)",
    type: "number",
    required: true,
    step: 0.01,
  },
  {
    name: "total_amount",
    label: "Total",
    type: "number",
    required: true,
    step: 0.01,
    compute: (values) => {
      const q = parseFloat(values.quantity_in_tin) || 0;
      const p = parseFloat(values.price_per_tin) || 0;
      return +(q * p).toFixed(2);
    },
  },
];

export const cashewKernelSalesPageMeta = {
  title: "Cashew Kernel Sales",
  subtitle: "Add daily cashew kernel sales records",
  icon: <Sell fontSize="medium" sx={{ color: "#cc6600" }} />,
};
