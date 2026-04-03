// src/pages/batch/status/mockListData.ts
import { type BatchStageMap } from "./types";

export const mockBatchList: {
  batchNumber: string;
  origin: string;
  intake_date: string;
  stages: BatchStageMap;
}[] = [
  {
    batchNumber: "BATCH-001",
    origin: "Nigeria",
    intake_date: "2025-11-20",
    stages: {
      purchase: {
        status: "Completed",
        updated_at: "2025-11-20T09:00:00Z",
        updated_by_name: "Alice",
      },
      boiling: {
        status: "In_Progress",
        updated_at: "2025-11-21T10:30:00Z",
        updated_by_name: "Bob",
      },
      nw_drying: { status: "Not_Started" },
      nw_humidification: { status: "Not_Started" },
      peeling_before_drying: { status: "Not_Started" },
      peeling_after_drying: { status: "Not_Started" },
      production: { status: "Not_Started" },
      cashew_kernel_sales: { status: "Not_Started" },
    },
  },
  {
    batchNumber: "BATCH-002",
    origin: "Ghana",
    intake_date: "2025-11-22",
    stages: {
      purchase: {
        status: "Completed",
        updated_at: "2025-11-22T08:00:00Z",
        updated_by_name: "Charlie",
      },
      boiling: {
        status: "Completed",
        updated_at: "2025-11-23T11:15:00Z",
        updated_by_name: "Dana",
      },
      nw_drying: {
        status: "In_Progress",
        updated_at: "2025-11-24T14:00:00Z",
        updated_by_name: "Eve",
      },
      nw_humidification: { status: "Not_Started" },
      peeling_before_drying: { status: "Not_Started" },
      peeling_after_drying: { status: "Not_Started" },
      production: { status: "Not_Started" },
      cashew_kernel_sales: { status: "Not_Started" },
    },
  },
  {
    batchNumber: "BATCH-003",
    origin: "India",
    intake_date: "2025-11-25",
    stages: {
      purchase: {
        status: "Completed",
        updated_at: "2025-11-25T07:45:00Z",
        updated_by_name: "Frank",
      },
      boiling: {
        status: "Completed",
        updated_at: "2025-11-26T09:20:00Z",
        updated_by_name: "Grace",
      },
      nw_drying: {
        status: "Completed",
        updated_at: "2025-11-27T12:00:00Z",
        updated_by_name: "Hannah",
      },
      nw_humidification: {
        status: "Completed",
        updated_at: "2025-11-27T15:30:00Z",
        updated_by_name: "Ivan",
      },
      peeling_before_drying: {
        status: "In_Progress",
        updated_at: "2025-11-28T10:00:00Z",
        updated_by_name: "Jack",
      },
      peeling_after_drying: { status: "Not_Started" },
      production: { status: "Not_Started" },
      cashew_kernel_sales: { status: "Not_Started" },
    },
  },
];
