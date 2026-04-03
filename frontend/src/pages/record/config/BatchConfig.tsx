import type { FormField } from "../../../types/FormField";

// pages/batch/config/BatchConfig.ts
export const batchFields: FormField[] = [
  { name: "date", label: "Date", type: "date" },
  { name: "batch_number", label: "Batch Number", type: "text" },
  { name: "origin", label: "Origin", type: "text" },
  {
    name: "purchase_status",
    label: "Purchase Status",
    type: "select",
    options: [
      { label: "In_Progress", value: "In_Progress" },
      { label: "Completed", value: "Completed" },
    ],
  },
  {
    name: "boiling_status",
    label: "Boiling Status",
    type: "select",
    options: [
      { label: "In_Progress", value: "In_Progress" },
      { label: "Completed", value: "Completed" },
    ],
  },
  {
    name: "nw_drying_status",
    label: "New Drying Status",
    type: "select",
    options: [
      { label: "In_Progress", value: "In_Progress" },
      { label: "Completed", value: "Completed" },
    ],
  },
  {
    name: "nw_humidification_status",
    label: "New Humidification Status",
    type: "select",
    options: [
      { label: "In_Progress", value: "In_Progress" },
      { label: "Completed", value: "Completed" },
    ],
  },
  {
    name: "peeling_before_drying_status",
    label: "Peeling Before Drying",
    type: "select",
    options: [
      { label: "In_Progress", value: "In_Progress" },
      { label: "Completed", value: "Completed" },
    ],
  },
  {
    name: "peeling_after_drying_status",
    label: "Peeling After Drying",
    type: "select",
    options: [
      { label: "In_Progress", value: "In_Progress" },
      { label: "Completed", value: "Completed" },
    ],
  },
  {
    name: "production_status",
    label: "Production Status",
    type: "select",
    options: [
      { label: "In_Progress", value: "In_Progress" },
      { label: "Completed", value: "Completed" },
    ],
  },
  {
    name: "cashew_kernel_sales_status",
    label: "Cashew Kernel Sales Status",
    type: "select",
    options: [
      { label: "In_Progress", value: "In_Progress" },
      { label: "Completed", value: "Completed" },
    ],
  },
];

export const batchPageMeta = {
  title: "Batch Entry",
  description: "Manage batch lifecycle entries across modules",
};
