import axiosInstance from "./axiosInstance";
import { API } from "../constants/apiRoutes";

export const insertDrying = async (rows: any[]) => {
  console.log("Inserting Drying with rows:", rows);
  const response = await axiosInstance.post(API.DRYING, rows);
  return response.data;
};

export const updateDrying = async (rows: any[]) => {
  console.log("Updating Drying with rows:", rows);
  const response = await axiosInstance.patch(API.DRYING, rows);
  console.log("Response from updating Drying:", response.data);
  return response.data;
};

export const deleteDrying = async (ids: string[]) => {
  console.log("Deleting Drying with ids:", ids);
  const payload = ids.map((id) => ({ id: parseInt(id) }));
  const response = await axiosInstance.delete(API.DRYING, { data: payload });
  return response.data;
};

export const getDryingByDate = async (date: string) => {
  console.log("Fetching Drying records for date:", date);
  const response = await axiosInstance.get(
    `${API.DRYING_BY_DATE}?date=${date}`
  );
  return response.data;
};
