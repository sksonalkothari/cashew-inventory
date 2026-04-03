// src/api/reportClient.ts
import { type TableQuery, type TableResult } from "../types/reportingTypes";
import axiosInstance from "./axiosInstance";

export async function fetchDefinedReport<T>(
  endpoint: string,
  query: TableQuery
): Promise<TableResult<T>> {
  const params = new URLSearchParams({
    page: String(query.page),
    pageSize: String(query.pageSize),
  });
  if (query.sortBy)
    params.set("sort", `${query.sortBy}:${query.sortDir ?? "asc"}`);
  if (query.globalSearch) params.set("search", query.globalSearch);
  if (query.dateFrom) params.set("dateFrom", query.dateFrom);
  if (query.dateTo) params.set("dateTo", query.dateTo);
  Object.entries(query.columnFilters ?? {}).forEach(([k, v]) => {
    if (v) params.append(`filter_${k}`, v);
  });

  const res = await axiosInstance.get(`${endpoint}?${params.toString()}`);
  return res.data;
}
