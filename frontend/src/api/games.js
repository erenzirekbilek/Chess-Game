import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const createGame = async (gameType = "vs_ai", aiDifficulty = "medium", aiColor = "black") => {
  const response = await api.post("/api/games/", {
    game_type: gameType,
    ai_difficulty: aiDifficulty,
    ai_color: aiColor,
  });
  return response.data;
};

export const getGame = async (gameId) => {
  const response = await api.get(`/api/games/${gameId}/`);
  return response.data;
};

export const makeMove = async (gameId, uci) => {
  const response = await api.post(`/api/games/${gameId}/make_move/`, {
    uci,
  });
  return response.data;
};

export const resignGame = async (gameId) => {
  const response = await api.post(`/api/games/${gameId}/resign/`);
  return response.data;
};

export const getMyGames = async () => {
  const response = await api.get("/api/games/my_games/");
  return response.data;
};

export const getActiveGames = async () => {
  const response = await api.get("/api/games/active/");
  return response.data;
};

export default api;