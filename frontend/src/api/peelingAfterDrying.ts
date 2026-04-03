import axiosInstance from "./axiosInstance";
import { API } from "../constants/apiRoutes";

export const insertPeelingAfterDrying = async (rows: any[]) => {
  console.log("Inserting Peeling After Drying with rows:", rows);
  const response = await axiosInstance.post(API.PEELING_AFTER_DRYING, rows);
  return response.data;
};

export const updatePeelingAfterDrying = async (rows: any[]) => {
  console.log("Updating Peeling After Drying with rows:", rows);
  const response = await axiosInstance.patch(API.PEELING_AFTER_DRYING, rows);
  console.log("Response from updating Peeling After Drying:", response.data);
  return response.data;
};

export const deletePeelingAfterDrying = async (ids: string[]) => {
  console.log("Deleting Peeling After Drying with ids:", ids);
  const payload = ids.map((id) => ({ id: parseInt(id) }));
  const response = await axiosInstance.delete(API.PEELING_AFTER_DRYING, {
    data: payload,
  });
  return response.data;
};

export const getPeelingAfterDryingByDate = async (date: string) => {
  console.log("Fetching PeelingAfterDrying records for date:", date);
  const response = await axiosInstance.get(
    `${API.PEELING_AFTER_DRYING_BY_DATE}?date=${date}`
  );
  return response.data;
};
