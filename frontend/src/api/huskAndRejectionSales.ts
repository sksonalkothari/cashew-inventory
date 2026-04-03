import axiosInstance from "./axiosInstance";
import { API } from "../constants/apiRoutes";

export const insertHuskAndRejectionSales = async (rows: any[]) => {
  const response = await axiosInstance.post(API.HUSK_REJECTION_SALES, rows);
  return response.data;
};

export const updateHuskAndRejectionSales = async (rows: any[]) => {
  console.log("Updating HuskAndRejectionSales with rows:", rows);
  const response = await axiosInstance.patch(API.HUSK_REJECTION_SALES, rows);
  console.log("Response from updating HuskAndRejectionSales:", response.data);
  return response.data;
};

export const deleteHuskAndRejectionSales = async (ids: string[]) => {
  console.log("Deleting HuskAndRejectionSales with ids:", ids);
  const payload = ids.map((id) => ({ id: parseInt(id) }));
  const response = await axiosInstance.delete(API.HUSK_REJECTION_SALES, {
    data: payload,
  });
  return response.data;
};

export const getHuskAndRejectionSalesByDate = async (date: string) => {
  const response = await axiosInstance.get(
    `${API.HUSK_REJECTION_SALES_BY_DATE}?date=${date}`
  );
  return response.data;
};
