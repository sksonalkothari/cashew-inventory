type UserAction = "INSERT" | "UPDATE" | "DELETE" | null | undefined;
type SystemStatus = "PENDING" | "SUBMITTED" | null | undefined;

export const getUserActionColor = (action: UserAction): string => {
  switch (action) {
    case "INSERT":
      return "green";
    case "UPDATE":
      return "orange";
    case "DELETE":
      return "red";
    default:
      return "#666";
  }
};

export const getSystemStatusColor = (status: SystemStatus): string => {
  switch (status) {
    case "PENDING":
      return "orange";
    case "SUBMITTED":
      return "green";
    default:
      return "#666";
  }
};
