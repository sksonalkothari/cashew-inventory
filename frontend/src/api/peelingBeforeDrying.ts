import axiosInstance from "./axiosInstance";
import { API } from "../constants/apiRoutes";

export const insertPeelingBeforeDrying = async (rows: any[]) => {
  console.log("Inserting Peeling Before Drying with rows:", rows);
  const response = await axiosInstance.post(API.PEELING_BEFORE_DRYING, rows);
  return response.data;
};

export const updatePeelingBeforeDrying = async (rows: any[]) => {
  console.log("Updating Peeling Before Drying with rows:", rows);
  const response = await axiosInstance.patch(API.PEELING_BEFORE_DRYING, rows);
  console.log("Response from updating Peeling Before Drying:", response.data);
  return response.data;
};

export const deletePeelingBeforeDrying = async (ids: string[]) => {
  console.log("Deleting Peeling Before Drying with ids:", ids);
  const payload = ids.map((id) => ({ id: parseInt(id) }));
  const response = await axiosInstance.delete(API.PEELING_BEFORE_DRYING, {
    data: payload,
  });
  return response.data;
};

export const getPeelingBeforeDryingByDate = async (date: string) => {
  console.log("Fetching PeelingBeforeDrying records for date:", date);
  const response = await axiosInstance.get(
    `${API.PEELING_BEFORE_DRYING_BY_DATE}?date=${date}`
  );
  return response.data;
};
