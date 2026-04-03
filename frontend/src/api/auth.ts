export const getToken = (): string | null => {
  try {
    return localStorage.getItem("token");
  } catch {
    return null;
  }
};

export const setToken = (token: string) => {
  try {
    localStorage.setItem("token", token);
  } catch {}
};

export const clearToken = () => {
  try {
    localStorage.removeItem("token");
  } catch {}
};

export const isAuthenticated = (): boolean => {
  const t = getToken();
  return !!t;
};
