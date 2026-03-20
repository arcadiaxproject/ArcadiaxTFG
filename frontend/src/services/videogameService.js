import api from "../config/api";

const videogameService = {
  getAll:       ()             => api.get("/videogames"),
  getById:      (id)           => api.get(`/videogames/${id}`),
  getConsoles:  ()             => api.get("/videogames/consoles"),
  getByConsole: (consola)      => api.get(`/videogames/console/${consola}`),
  create:       (data)         => api.post("/videogames", data),
  update:       (id, data)     => api.put(`/videogames/${id}`, data),
  delete:       (id)           => api.delete(`/videogames/${id}`),
};

export default videogameService;
