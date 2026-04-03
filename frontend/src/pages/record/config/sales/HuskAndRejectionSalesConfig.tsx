import type { FormField } from "../../../../types/FormField";
import { Sell } from "@mui/icons-material";

export const fields: FormField[] = [
  { name: "date", label: "Date", type: "date", required: true },
  { name: "bill_number", label: "Bill No.", type: "text", required: true },
  { name: "customer_name", label: "Name", type: "text", required: true },
  { name: "batch_number", label: "Batch No", type: "text", required: true },
  {
    name: "item_type",
    label: "Item",
    type: "select",
    required: true,
    options: [
      { label: "Husk", value: "Husk" },
      { label: "Rejection", value: "Rejection" },
    ],
  },
  {
    name: "quantity_kg",
    label: "Quantity (Kg)",
    type: "number",
    required: true,
    step: 0, // only integers allowed
  },
  {
    name: "price_per_kg",
    label: "Price (₹/Kg)",
    type: "number",
    required: true,
    step: 0.01, // allow decimal numbers
  },
  {
    name: "total_amount",
    label: "Total",
    type: "number",
    required: true,
    step: 0.01,
    compute: (values) => {
      const q = parseFloat(values.quantity_kg) || 0;
      const p = parseFloat(values.price_per_kg) || 0;
      return +(q * p).toFixed(2);
    },
  },
];

export const huskAndRejectionSalesPageMeta = {
  title: "Husk & Rejection Sales",
  subtitle: "Add daily husk & rejection sales records",
  icon: <Sell fontSize="medium" sx={{ color: "#cc6600" }} />,
};
