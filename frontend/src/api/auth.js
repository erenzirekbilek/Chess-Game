import api from "./axios";

export const register = async (username, email, password) => {
  const response = await api.post("/api/auth/register/", {
    username,
    email,
    password,
  });
  return response.data;
};

export const login = async (username, password) => {
  const response = await api.post("/api/auth/login/", {
    username,
    password,
  });
  const { access, refresh } = response.data;
  localStorage.setItem("access_token", access);
  localStorage.setItem("refresh_token", refresh);
  return response.data;
};

export const logout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
};

export const getCurrentUser = async () => {
  const response = await api.get("/api/auth/me/");
  return response.data;
};

export const refreshToken = async () => {
  const refresh = localStorage.getItem("refresh_token");
  if (!refresh) return null;

  try {
    const response = await api.post("/api/auth/refresh/", { refresh });
    const { access } = response.data;
    localStorage.setItem("access_token", access);
    return access;
  } catch (error) {
    logout();
    return null;
  }
};

export const isAuthenticated = () => {
  return !!localStorage.getItem("access_token");
};