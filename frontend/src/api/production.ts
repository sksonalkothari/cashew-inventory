import axiosInstance from "./axiosInstance";
import { API } from "../constants/apiRoutes";

export const insertProduction = async (rows: any[]) => {
  console.log("Inserting Production with rows:", rows);
  const response = await axiosInstance.post(API.PRODUCTION, rows);
  return response.data;
};

export const updateProduction = async (rows: any[]) => {
  console.log("Updating Production with rows:", rows);
  const response = await axiosInstance.patch(API.PRODUCTION, rows);
  console.log("Response from updating Production:", response.data);
  return response.data;
};

export const deleteProduction = async (ids: string[]) => {
  console.log("Deleting Production with ids:", ids);
  const payload = ids.map((id) => ({ id: parseInt(id) }));
  const response = await axiosInstance.delete(API.PRODUCTION, {
    data: payload,
  });
  return response.data;
};

export const getProductionByDate = async (date: string) => {
  console.log("Fetching Production records for date:", date);
  const response = await axiosInstance.get(
    `${API.PRODUCTION_BY_DATE}?date=${date}`
  );
  return response.data;
};
