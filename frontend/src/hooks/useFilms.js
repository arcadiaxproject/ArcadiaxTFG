import { useState, useEffect, useCallback } from "react";
import filmService from "../services/filmService";

export function useFilms() {
  const [films, setFilms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetch = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await filmService.getAll();
      setFilms(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Error al cargar peliculas");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetch(); }, [fetch]);

  return { films, loading, error, refresh: fetch };
}
