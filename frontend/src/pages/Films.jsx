import React, { useEffect } from "react";
import Navbar from "../components/layout/Navbar";
import Loading from "../components/layout/Loading";
import ErrorMessage from "../components/layout/ErrorMessage";
import FilmCard from "../components/films/FilmCard";
import { useFilms } from "../hooks/useFilms";
import { usePlayback } from "../hooks/usePlayback";

const tvBg = process.env.PUBLIC_URL + '/assets/tv.jpg';

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

  const pageStyle = {
    minHeight: "100vh",
    backgroundImage: `url('${tvBg}')`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    backgroundAttachment: "fixed",
    backgroundColor: "#0a0a0f",
    position: "relative",
  };

  const overlayStyle = {
    position: "absolute",
    inset: 0,
    background: "rgba(10, 5, 20, 0.82)",
    zIndex: 0,
  };

  // Efecto scanlines años 80
  const scanlinesStyle = {
    position: "absolute",
    inset: 0,
    backgroundImage: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.18) 2px, rgba(0,0,0,0.18) 4px)",
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
  };

  const headerStyle = {
    textAlign: "center",
    marginBottom: "2.5rem",
  };

  const titleStyle = {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "clamp(18px, 4vw, 40px)",
    color: "#FF006E",
    textShadow: "0 0 10px #FF006E, 0 0 30px rgba(255,0,110,0.6), 0 0 60px rgba(255,0,110,0.3)",
    letterSpacing: "6px",
    marginBottom: "0.8rem",
    display: "block",
  };

  // Estética VHS años 80
  const vhsBadgeStyle = {
    display: "inline-block",
    fontFamily: "'Orbitron', sans-serif",
    fontSize: "11px",
    color: "#00F5FF",
    letterSpacing: "4px",
    textShadow: "0 0 6px #00F5FF",
    border: "1px solid rgba(0,245,255,0.4)",
    padding: "4px 14px",
    borderRadius: "2px",
    marginTop: "0.5rem",
  };

  const dividerStyle = {
    width: "200px",
    height: "2px",
    background: "linear-gradient(90deg, transparent, #FF006E, transparent)",
    margin: "1.5rem auto",
    boxShadow: "0 0 8px #FF006E",
  };

  const playbackErrorStyle = {
    fontFamily: "'Orbitron', sans-serif",
    fontSize: "12px",
    color: "#FF006E",
    background: "rgba(255,0,110,0.1)",
    border: "1px solid rgba(255,0,110,0.4)",
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
    border: "1px solid rgba(255,0,110,0.5)",
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
    maxWidth: "1200px",
    margin: "0 auto",
  };

  const emptyStyle = {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "12px",
    color: "rgba(255,0,110,0.5)",
    textAlign: "center",
    padding: "60px 0",
    letterSpacing: "2px",
  };

  return (
    <div style={pageStyle}>
      <Navbar />
      <div style={overlayStyle} />
      <div style={scanlinesStyle} />
      <div style={contentStyle}>
        <div style={headerStyle}>
          <span style={titleStyle}>HOMEFLIX</span>
          <div>
            <span style={vhsBadgeStyle}>▶ VHS · BETA · 1980s</span>
          </div>
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
              : <p style={emptyStyle}>NO HAY PELICULAS DISPONIBLES</p>
            }
          </div>
        )}
      </div>
    </div>
  );
}
