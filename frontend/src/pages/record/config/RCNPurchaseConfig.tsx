import type { FormField } from "../../../types/FormField";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";

export const rcnPurchaseFields: FormField[] = [
  { name: "date", label: "Date", type: "date", required: true },
  { name: "supplier_name", label: "Name", type: "text", required: true },
  { name: "bill_number", label: "Bill No", type: "text", required: true },
  {
    name: "batch_number",
    label: "Batch No",
    type: "batch_select",
    required: true,
    stage: "purchase",
  },
  {
    name: "quantity_kg",
    label: "Quantity (kg)",
    type: "number",
    required: true,
    step: 0,
  },
  {
    name: "price_per_kg",
    label: "Price (₹/Kg)",
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
      const q = parseFloat(values.quantity_kg) || 0;
      const p = parseFloat(values.price_per_kg) || 0;
      return +(q * p).toFixed(2);
    },
  },
];

export const rcnPurchasePageMeta = {
  title: "RCN Purchase",
  subtitle: "Add RCN purchase records",
  icon: <ShoppingCartIcon fontSize="medium" sx={{ color: "#cc6600" }} />,
};
