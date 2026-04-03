import axiosInstance from "./axiosInstance";
import { API } from "../constants/apiRoutes";

export const insertHumidifying = async (rows: any[]) => {
  console.log("Inserting Humidifying with rows:", rows);
  const response = await axiosInstance.post(API.HUMIDIFYING, rows);
  return response.data;
};

export const updateHumidifying = async (rows: any[]) => {
  console.log("Updating Humidifying with rows:", rows);
  const response = await axiosInstance.patch(API.HUMIDIFYING, rows);
  console.log("Response from updating Humidifying:", response.data);
  return response.data;
};

export const deleteHumidifying = async (ids: string[]) => {
  console.log("Deleting Humidifying with ids:", ids);
  const payload = ids.map((id) => ({ id: parseInt(id) }));
  const response = await axiosInstance.delete(API.HUMIDIFYING, {
    data: payload,
  });
  return response.data;
};

export const getHumidifyingByDate = async (date: string) => {
  console.log("Fetching Humidifying records for date:", date);
  const response = await axiosInstance.get(
    `${API.HUMIDIFYING_BY_DATE}?date=${date}`
  );
  return response.data;
};
