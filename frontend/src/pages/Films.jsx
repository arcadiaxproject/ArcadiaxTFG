import React, { useEffect } from "react";
import Layout from "../components/layout/Layout";
import Loading from "../components/layout/Loading";
import ErrorMessage from "../components/layout/ErrorMessage";
import FilmCard from "../components/films/FilmCard";
import { useFilms } from "../hooks/useFilms";
import { usePlayback } from "../hooks/usePlayback";

export default function Films() {
  const { films, loading, error, refresh } = useFilms();
  const { current, playFilm, stop, fetchCurrent, error: playbackError, clearError } = usePlayback();

  useEffect(() => { fetchCurrent(); }, [fetchCurrent]);

  const handlePlay = async (nombre) => {
    await playFilm(nombre);
    refresh();
  };

  const handleStop = async () => {
    await stop();
    refresh();
  };

  return (
    <Layout>
      <h2>Homeflix</h2>
      {playbackError && (
        <p style={{ color: "#f55" }}>{playbackError} <button onClick={clearError}>x</button></p>
      )}
      {loading && <Loading text="Cargando peliculas..." />}
      {error && <ErrorMessage message={error} onRetry={refresh} />}
      {!loading && !error && (
        <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
          {films.length > 0
            ? films.map((film) => (
                <FilmCard
                  key={film._id}
                  film={film}
                  onPlay={handlePlay}
                  onStop={handleStop}
                  isPlaying={current.type === "film" && current.data?._id === film._id}
                />
              ))
            : <p>No hay peliculas disponibles.</p>
          }
        </div>
      )}
    </Layout>
  );
}
