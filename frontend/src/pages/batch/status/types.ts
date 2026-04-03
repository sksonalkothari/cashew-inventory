// src/pages/batch/status/types.ts
export type Stage =
  | "purchase"
  | "boiling"
  | "nw_drying"
  | "nw_humidification"
  | "peeling_before_drying"
  | "peeling_after_drying"
  | "production"
  | "cashew_kernel_sales";

export type Status = "Not_Started" | "In_Progress" | "Completed";

export const stageLabels: Record<Stage, string> = {
  purchase: "Purchase",
  boiling: "Boiling",
  nw_drying: "NW Drying",
  nw_humidification: "Humidification",
  peeling_before_drying: "Peeling Before Drying",
  peeling_after_drying: "Peeling After Dryinh",
  production: "Production",
  cashew_kernel_sales: "Cashew Kernel Sales",
};

export const statusColors: Record<Status, string> = {
  Not_Started: "#d3d3d3",
  In_Progress: "#f2c94c",
  Completed: "#27ae60",
};

export type StageState = {
  status: Status;
  updated_at?: string | null;
  updated_by_name?: string | null; // optional: resolve user id -> name in API
};

export type BatchStageMap = Record<Stage, StageState>;
