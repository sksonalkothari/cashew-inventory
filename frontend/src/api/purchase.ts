import axiosInstance from "./axiosInstance";
import { API } from "../constants/apiRoutes";

export const insertRCNPurchase = async (rows: any[]) => {
  const response = await axiosInstance.post(API.RCN_PURCHASE, rows);
  return response.data;
};

export const updateRCNPurchase = async (rows: any[]) => {
  console.log("Updating RCN Purchase with rows:", rows);
  const response = await axiosInstance.patch(API.RCN_PURCHASE, rows);
  console.log("Response from updating RCN Purchase:", response.data);
  return response.data;
};

export const deleteRCNPurchase = async (ids: string[]) => {
  console.log("Deleting RCN Purchase with ids:", ids);

  const payload = ids.map((id) => ({ id: parseInt(id) }));

  const response = await axiosInstance.delete(API.RCN_PURCHASE, {
    data: payload,
  });

  return response.data;
};

export const getRCNPurchaseByDate = async (date: string) => {
  const response = await axiosInstance.get(
    `${API.RCN_PURCHASE_BY_DATE}?date=${date}`
  );
  return response.data;
};
