const VERSION = import.meta.env.VITE_API_VERSION;
export const BASE_URL = `${import.meta.env.VITE_API_BASE}/${VERSION}`;

console.log("ENV BASE:", import.meta.env.VITE_API_BASE);
console.log("ENV VERSION:", import.meta.env.VITE_API_VERSION);
console.log("BASE_URL:", BASE_URL);

export const API = {
  LOGIN: `/auth/login`,
  SIGNUP: `/auth/signup`,
  ME: `/user/me`,
  USERS: `/users`,
  GRADES: `/grades`,
  GRADES_BY_DATE: `/grades/by-date`,
  RCN_PURCHASE: `/purchase/`,
  RCN_PURCHASE_BY_DATE: `/purchase/by-date`,
  BOILING: `/boiling/`,
  BOILING_BY_DATE: `/boiling/by-date`,
  DRYING: `/drying/`,
  DRYING_BY_DATE: `/drying/by-date`,
  HUMIDIFYING: `/humidifying/`,
  HUMIDIFYING_BY_DATE: `/humidifying/by-date`,
  PEELING_BEFORE_DRYING: `/peeling_before_drying/`,
  PEELING_BEFORE_DRYING_BY_DATE: `/peeling_before_drying/by-date`,
  PEELING_AFTER_DRYING: `/peeling_after_drying/`,
  PEELING_AFTER_DRYING_BY_DATE: `/peeling_after_drying/by-date`,
  PRODUCTION: `/production/`,
  PRODUCTION_BY_DATE: `/production/by-date`,
  RCN_SALES: `/rcn_sales/`,
  RCN_SALES_BY_DATE: `/rcn_sales/by-date`,
  CASHEW_KERNEL_SALES: `/cashew_kernel_sales/`,
  CASHEW_KERNEL_SALES_BY_DATE: `/cashew_kernel_sales/by-date`,
  CASHEW_SHELL_SALES: `/cashew_shell_sales/`,
  CASHEW_SHELL_SALES_BY_DATE: `/cashew_shell_sales/by-date`,
  HUSK_REJECTION_SALES: `/husk_rejection_sales/`,
  HUSK_REJECTION_SALES_BY_DATE: `/husk_rejection_sales/by-date`,
  HUSK_RETURN: `/husk_return/`,
  HUSK_RETURN_BY_DATE: `/husk_return/by-date`,
  BATCH: `/batch/`,
  BATCH_ALL: `/batch/all`,
  BATCH_INPROGRESS: `/batch/inprogress`,
};
