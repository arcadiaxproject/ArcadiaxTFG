import React from "react";
import { useParams } from "react-router-dom";
import Layout from "../components/layout/Layout";
import Loading from "../components/layout/Loading";
import ErrorMessage from "../components/layout/ErrorMessage";
import GameCard from "../components/videogames/GameCard";
import { useVideogames } from "../hooks/useVideogames";
import { usePlayback } from "../hooks/usePlayback";

export default function Games() {
  const { consolaNombre } = useParams();
  const { games, loading, error, refresh } = useVideogames(consolaNombre);
  const { current, playGame, stop, error: playbackError, clearError } = usePlayback();

  const handlePlay = async (nombre, consola) => {
    await playGame(nombre, consola);
    refresh();
  };

  const handleStop = async () => {
    await stop();
    refresh();
  };

  return (
    <Layout>
      <h2>{consolaNombre?.toUpperCase()}</h2>
      {playbackError && (
        <p style={{ color: "#f55" }}>{playbackError} <button onClick={clearError}>x</button></p>
      )}
      {loading && <Loading text="Cargando juegos..." />}
      {error && <ErrorMessage message={error} onRetry={refresh} />}
      {!loading && !error && (
        <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
          {games.length > 0
            ? games.map((game) => (
                <GameCard
                  key={game._id}
                  game={game}
                  onPlay={handlePlay}
                  onStop={handleStop}
                  isPlaying={current.type === "game" && current.data?._id === game._id}
                />
              ))
            : <p>No hay juegos para esta consola.</p>
          }
        </div>
      )}
    </Layout>
  );
}
