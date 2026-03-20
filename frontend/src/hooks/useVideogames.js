import { useState, useEffect, useCallback } from "react";
import videogameService from "../services/videogameService";

export function useVideogames(consola) {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetch = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const res = consola
        ? await videogameService.getByConsole(consola)
        : await videogameService.getAll();
      setGames(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Error al cargar videojuegos");
    } finally {
      setLoading(false);
    }
  }, [consola]);

  useEffect(() => { fetch(); }, [fetch]);

  return { games, loading, error, refresh: fetch };
}

export function useConsoles() {
  const [consoles, setConsoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetch = async () => {
      try {
        setLoading(true);
        const res = await videogameService.getConsoles();
        setConsoles(res.data);
      } catch (err) {
        setError(err.response?.data?.detail || "Error al cargar consolas");
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, []);

  return { consoles, loading, error };
}
