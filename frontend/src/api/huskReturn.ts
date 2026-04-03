import axiosInstance from "./axiosInstance";
import { API } from "../constants/apiRoutes";

export const insertHuskReturn = async (rows: any[]) => {
  const response = await axiosInstance.post(API.HUSK_RETURN, rows);
  return response.data;
};

export const updateHuskReturn = async (rows: any[]) => {
  console.log("Updating Husk Return with rows:", rows);
  const response = await axiosInstance.patch(API.HUSK_RETURN, rows);
  console.log("Response from updating Husk Return:", response.data);
  return response.data;
};

export const deleteHuskReturn = async (ids: string[]) => {
  console.log("Deleting Husk Return with ids:", ids);
  const payload = ids.map((id) => ({ id: parseInt(id) }));
  const response = await axiosInstance.delete(API.HUSK_RETURN, {
    data: payload,
  });
  return response.data;
};

export const getHuskReturnByDate = async (date: string) => {
  const response = await axiosInstance.get(
    `${API.HUSK_RETURN_BY_DATE}?date=${date}`
  );
  return response.data;
};
