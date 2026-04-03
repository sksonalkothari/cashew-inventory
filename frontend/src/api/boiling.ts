import axiosInstance from "./axiosInstance";
import { API } from "../constants/apiRoutes";

export const insertBoiling = async (rows: any[]) => {
  const response = await axiosInstance.post(API.BOILING, rows);
  return response.data;
};

export const updateBoiling = async (rows: any[]) => {
  console.log("Updating Boiling with rows:", rows);
  const response = await axiosInstance.patch(API.BOILING, rows);
  console.log("Response from updating Boiling:", response.data);
  return response.data;
};

export const deleteBoiling = async (ids: string[]) => {
  console.log("Deleting Boiling with ids:", ids);

  const payload = ids.map((id) => ({ id: parseInt(id) }));

  const response = await axiosInstance.delete(API.BOILING, { data: payload });

  return response.data;
};

export const getBoilingByDate = async (date: string) => {
  const response = await axiosInstance.get(
    `${API.BOILING_BY_DATE}?date=${date}`
  );
  return response.data;
};
