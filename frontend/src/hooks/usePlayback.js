import { useState, useCallback } from "react";
import playbackService from "../services/playbackService";

export function usePlayback() {
  const [current, setCurrent] = useState({ type: "none", data: null });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchCurrent = useCallback(async () => {
    try {
      const res = await playbackService.getCurrent();
      setCurrent(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Error al obtener estado");
    }
  }, []);

  const playGame = useCallback(async (nombre, consola) => {
    try {
      setLoading(true);
      setError(null);
      await playbackService.playGame(nombre, consola);
      await fetchCurrent();
    } catch (err) {
      setError(err.response?.data?.detail || "Error al iniciar juego");
    } finally {
      setLoading(false);
    }
  }, [fetchCurrent]);

  const playFilm = useCallback(async (nombre) => {
    try {
      setLoading(true);
      setError(null);
      await playbackService.playFilm(nombre);
      await fetchCurrent();
    } catch (err) {
      setError(err.response?.data?.detail || "Error al iniciar pelicula");
    } finally {
      setLoading(false);
    }
  }, [fetchCurrent]);

  const stop = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      await playbackService.stop();
      setCurrent({ type: "none", data: null });
    } catch (err) {
      setError(err.response?.data?.detail || "Error al parar");
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    current, loading, error,
    playGame, playFilm, stop, fetchCurrent,
    clearError: () => setError(null),
  };
}
