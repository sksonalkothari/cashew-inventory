import axiosInstance from "./axiosInstance";
import { API } from "../constants/apiRoutes";

export const insertGrade = async (rows: any[]) => {
  console.log("Inserting Grade with rows:", rows);
  const response = await axiosInstance.post(API.GRADES, rows);
  return response.data;
};

export const updateGrade = async (rows: any[]) => {
  console.log("Updating Grade with rows:", rows);
  const response = await axiosInstance.patch(API.GRADES, rows);
  console.log("Response from updating Grade:", response.data);
  return response.data;
};

export const deleteGrade = async (ids: string[]) => {
  console.log("Deleting Grade with ids:", ids);
  const payload = ids.map((id) => ({ id: parseInt(id) }));
  const response = await axiosInstance.delete(API.GRADES, { data: payload });
  return response.data;
};

export const getAllGrades = async () => {
  const response = await axiosInstance.get(`${API.GRADES}`);
  return response.data;
};
