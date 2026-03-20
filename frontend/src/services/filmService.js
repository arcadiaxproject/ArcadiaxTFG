import api from "../config/api";

const filmService = {
  getAll: ()       => api.get("/films"),
  create: (data)   => api.post("/films", data),
  delete: (id)     => api.delete(`/films/${id}`),
};

export default filmService;
