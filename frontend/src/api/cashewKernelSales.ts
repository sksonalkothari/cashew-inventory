import axiosInstance from "./axiosInstance";
import { API } from "../constants/apiRoutes";

export const insertCashewKernelSales = async (rows: any[]) => {
  const response = await axiosInstance.post(API.CASHEW_KERNEL_SALES, rows);
  return response.data;
};

export const updateCashewKernelSales = async (rows: any[]) => {
  console.log("Updating CashewKernelSales with rows:", rows);
  const response = await axiosInstance.patch(API.CASHEW_KERNEL_SALES, rows);
  console.log("Response from updating CashewKernelSales:", response.data);
  return response.data;
};

export const deleteCashewKernelSales = async (ids: string[]) => {
  console.log("Deleting CashewKernelSales with ids:", ids);
  const payload = ids.map((id) => ({ id: parseInt(id) }));
  const response = await axiosInstance.delete(API.CASHEW_KERNEL_SALES, {
    data: payload,
  });
  return response.data;
};

export const getCashewKernelSalesByDate = async (date: string) => {
  const response = await axiosInstance.get(
    `${API.CASHEW_KERNEL_SALES_BY_DATE}?date=${date}`
  );
  return response.data;
};
