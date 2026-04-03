// src/pages/batch/status/mockData.ts
import { type BatchStageMap } from "./types";

export const mockBatchStages: BatchStageMap = {
  purchase: {
    status: "Completed",
    updated_at: "2025-11-25T10:15:00Z",
    updated_by_name: "Alice",
  },
  boiling: {
    status: "In_Progress",
    updated_at: "2025-11-26T08:30:00Z",
    updated_by_name: "Bob",
  },
  nw_drying: {
    status: "Not_Started",
    updated_at: null,
    updated_by_name: null,
  },
  nw_humidification: {
    status: "Not_Started",
    updated_at: null,
    updated_by_name: null,
  },
  peeling_before_drying: {
    status: "Completed",
    updated_at: "2025-11-27T09:45:00Z",
    updated_by_name: "Charlie",
  },
  peeling_after_drying: {
    status: "In_Progress",
    updated_at: "2025-11-27T14:20:00Z",
    updated_by_name: "Dana",
  },
  production: {
    status: "Not_Started",
    updated_at: null,
    updated_by_name: null,
  },
  cashew_kernel_sales: {
    status: "Completed",
    updated_at: "2025-11-28T11:00:00Z",
    updated_by_name: "Eve",
  },
};
