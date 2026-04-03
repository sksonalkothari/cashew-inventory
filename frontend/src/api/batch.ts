// src/api/batch.ts
import type { BatchStageMap } from "../pages/batch/status/types";
import axiosInstance from "./axiosInstance";
import { API } from "../constants/apiRoutes";

export type BatchListItem = {
  batchNumber: string;
  origin: string;
  intake_date: string;
  stages: BatchStageMap;
};

export async function fetchBatchList(): Promise<BatchListItem[]> {
  const res = await axiosInstance.get(API.BATCH_ALL);
  return res.data;
}

export async function insertBatch(data: any) {
  const res = await axiosInstance.post(API.BATCH, data);
  return res.data;
}

export const updateBatch = async (data: any) => {
  console.log("Updating batch:", data);
  const res = await axiosInstance.patch(API.BATCH, data);
  console.log("Response from updating batch:", res.data);
  return res.data;
};

export async function fetchInProgressBatchesByStage(
  stage: string
): Promise<BatchListItem[]> {
  const res = await axiosInstance.post(API.BATCH_INPROGRESS, { stage });
  return res.data;
}
