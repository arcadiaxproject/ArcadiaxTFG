import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import Navbar from "../components/layout/Navbar";
import Loading from "../components/layout/Loading";
import ErrorMessage from "../components/layout/ErrorMessage";
import GameCard from "../components/videogames/GameCard";
import { useVideogames } from "../hooks/useVideogames";
import { usePlayback } from "../hooks/usePlayback";

export default function Games() {
  const { consolaNombre } = useParams();
  const navigate = useNavigate();
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

  const pageStyle = {
    minHeight: "100vh",
    backgroundColor: "#0a0a0f",
    backgroundImage: `
      linear-gradient(rgba(0, 245, 255, 0.025) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0, 245, 255, 0.025) 1px, transparent 1px)
    `,
    backgroundSize: "48px 48px",
    position: "relative",
  };

  const scanlinesStyle = {
    position: "fixed",
    inset: 0,
    backgroundImage:
      "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.12) 2px, rgba(0,0,0,0.12) 4px)",
    zIndex: 1,
    pointerEvents: "none",
  };

  const contentStyle = {
    position: "relative",
    zIndex: 2,
    paddingTop: "100px",
    paddingBottom: "3rem",
    paddingLeft: "2rem",
    paddingRight: "2rem",
    maxWidth: "1200px",
    margin: "0 auto",
  };

  const headerStyle = {
    textAlign: "center",
    marginBottom: "2.5rem",
  };

  const titleStyle = {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "clamp(14px, 3vw, 30px)",
    color: "#00F5FF",
    textShadow:
      "0 0 10px #00F5FF, 0 0 30px rgba(0, 245, 255, 0.6), 0 0 60px rgba(0, 245, 255, 0.3)",
    letterSpacing: "4px",
    marginBottom: "0.8rem",
    display: "block",
  };

  const dividerStyle = {
    width: "200px",
    height: "2px",
    background: "linear-gradient(90deg, transparent, #00F5FF, transparent)",
    margin: "1.2rem auto",
    boxShadow: "0 0 8px #00F5FF",
  };

  const backButtonStyle = {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "8px",
    letterSpacing: "1px",
    color: "#FFE600",
    background: "transparent",
    border: "1px solid rgba(255, 230, 0, 0.5)",
    borderRadius: "3px",
    padding: "10px 16px",
    cursor: "pointer",
    marginBottom: "2rem",
    display: "inline-block",
    transition: "box-shadow 0.2s, border-color 0.2s",
    textShadow: "0 0 6px rgba(255,230,0,0.5)",
  };

  const playbackErrorStyle = {
    fontFamily: "'Orbitron', sans-serif",
    fontSize: "12px",
    color: "#FF006E",
    background: "rgba(255, 0, 110, 0.1)",
    border: "1px solid rgba(255, 0, 110, 0.4)",
    borderRadius: "4px",
    padding: "10px 16px",
    marginBottom: "1.5rem",
    display: "flex",
    alignItems: "center",
    gap: "12px",
    maxWidth: "600px",
    margin: "0 auto 1.5rem",
  };

  const clearBtnStyle = {
    background: "transparent",
    border: "1px solid rgba(255, 0, 110, 0.5)",
    color: "#FF006E",
    borderRadius: "3px",
    padding: "2px 8px",
    cursor: "pointer",
    fontSize: "11px",
    fontFamily: "'Orbitron', sans-serif",
  };

  const gridStyle = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
    gap: "24px",
  };

  const emptyStyle = {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "12px",
    color: "rgba(0, 245, 255, 0.5)",
    textAlign: "center",
    padding: "60px 0",
    letterSpacing: "2px",
  };

  return (
    <div style={pageStyle}>
      <Navbar />
      <div style={scanlinesStyle} />
      <div style={contentStyle}>
        <button
          style={backButtonStyle}
          onClick={() => navigate("/consolas")}
          onMouseEnter={(e) => {
            e.currentTarget.style.boxShadow = "0 0 8px #FFE600, 0 0 20px rgba(255,230,0,0.3)";
            e.currentTarget.style.borderColor = "#FFE600";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.boxShadow = "none";
            e.currentTarget.style.borderColor = "rgba(255, 230, 0, 0.5)";
          }}
        >
          ← VOLVER
        </button>

        <div style={headerStyle}>
          <span style={titleStyle}>{consolaNombre?.toUpperCase()}</span>
          <div style={dividerStyle} />
        </div>

        {playbackError && (
          <div style={playbackErrorStyle}>
            <span>{playbackError}</span>
            <button style={clearBtnStyle} onClick={clearError}>✕</button>
          </div>
        )}

        {loading && <Loading />}
        {error && <ErrorMessage message={error} onRetry={refresh} />}

        {!loading && !error && (
          <div style={gridStyle}>
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
              : <p style={emptyStyle}>NO HAY JUEGOS DISPONIBLES</p>
            }
          </div>
        )}
      </div>
    </div>
  );
}
