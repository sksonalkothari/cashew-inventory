import axiosInstance from "./axiosInstance";
import { API } from "../constants/apiRoutes";

export const insertCashewShellSales = async (rows: any[]) => {
  const response = await axiosInstance.post(API.CASHEW_SHELL_SALES, rows);
  return response.data;
};

export const updateCashewShellSales = async (rows: any[]) => {
  console.log("Updating CashewShellSales with rows:", rows);
  const response = await axiosInstance.patch(API.CASHEW_SHELL_SALES, rows);
  console.log("Response from updating CashewShellSales:", response.data);
  return response.data;
};

export const deleteCashewShellSales = async (ids: string[]) => {
  console.log("Deleting CashewShellSales with ids:", ids);
  const payload = ids.map((id) => ({ id: parseInt(id) }));
  const response = await axiosInstance.delete(API.CASHEW_SHELL_SALES, {
    data: payload,
  });
  return response.data;
};

export const getCashewShellSalesByDate = async (date: string) => {
  const response = await axiosInstance.get(
    `${API.CASHEW_SHELL_SALES_BY_DATE}?date=${date}`
  );
  return response.data;
};
