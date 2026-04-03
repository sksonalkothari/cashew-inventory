import axiosInstance from "./axiosInstance";
import { API } from "../constants/apiRoutes";

export const insertRCNSales = async (rows: any[]) => {
  const response = await axiosInstance.post(API.RCN_SALES, rows);
  return response.data;
};

export const updateRCNSales = async (rows: any[]) => {
  console.log("Updating RCNSales with rows:", rows);
  const response = await axiosInstance.patch(API.RCN_SALES, rows);
  console.log("Response from updating RCNSales:", response.data);
  return response.data;
};

export const deleteRCNSales = async (ids: string[]) => {
  console.log("Deleting RCNSales with ids:", ids);
  const payload = ids.map((id) => ({ id: parseInt(id) }));
  const response = await axiosInstance.delete(API.RCN_SALES, { data: payload });
  return response.data;
};

export const getRCNSalesByDate = async (date: string) => {
  const response = await axiosInstance.get(
    `${API.RCN_SALES_BY_DATE}?date=${date}`
  );
  return response.data;
};
