import api from "../config/api";

const playbackService = {
  playGame:        (nombre, consola) => api.post(`/playback/game/${nombre}/${consola}`),
  playFilm:        (nombre)          => api.post(`/playback/film/${nombre}`),
  stop:            ()                => api.post("/playback/stop"),
  getCurrent:      ()                => api.get("/playback/current"),
  getRandomTrailer:()                => api.get("/playback/trailer"),
};

export default playbackService;
