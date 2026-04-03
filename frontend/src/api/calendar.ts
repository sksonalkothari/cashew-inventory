import axiosInstance from "./axiosInstance";

export const getDatesWithEntries = async (): Promise<string[]> => {
  const res = await axiosInstance.get("/api/entries/dates-with-data");
  return res.data;
};

export const getEntriesByDate = async (
  date: string
): Promise<Record<string, any[]>> => {
  const res = await axiosInstance.get(`/api/entries/by-date?date=${date}`);
  return res.data.modules;
};
