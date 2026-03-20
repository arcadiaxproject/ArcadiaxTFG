import React, { useState } from "react";

export default function FilmCard({ film, onPlay, onStop, isPlaying }) {
  const [hovered, setHovered] = useState(false);

  const cardStyle = {
    position: "relative",
    width: "220px",
    height: "330px",
    borderRadius: "8px",
    overflow: "hidden",
    border: isPlaying
      ? "2px solid #FF006E"
      : hovered
        ? "2px solid rgba(255,0,110,0.8)"
        : "2px solid rgba(255,0,110,0.25)",
    boxShadow: isPlaying
      ? "0 0 20px #FF006E, 0 0 50px rgba(255,0,110,0.4)"
      : hovered
        ? "0 0 16px rgba(255,0,110,0.5), 0 12px 40px rgba(0,0,0,0.8)"
        : "0 4px 20px rgba(0,0,0,0.6)",
    transform: hovered ? "translateY(-8px) scale(1.03)" : "translateY(0) scale(1)",
    transition: "all 0.3s ease",
    cursor: "pointer",
    background: "#111",
  };

  const imageStyle = {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    display: "block",
  };

  const overlayStyle = {
    position: "absolute",
    inset: 0,
    background: isPlaying
      ? "linear-gradient(transparent 30%, rgba(180,0,80,0.5) 70%, rgba(0,0,0,0.95) 100%)"
      : "linear-gradient(transparent 40%, rgba(0,0,0,0.7) 70%, rgba(0,0,0,0.97) 100%)",
    transition: "background 0.3s ease",
  };

  // Efecto scanlines VHS
  const scanlinesStyle = {
    position: "absolute",
    inset: 0,
    backgroundImage: "repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,0.1) 3px, rgba(0,0,0,0.1) 4px)",
    pointerEvents: "none",
    opacity: hovered ? 0.3 : 0.6,
    transition: "opacity 0.3s ease",
  };

  const contentStyle = {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    padding: "16px",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  };

  const vhsBadgeStyle = {
    display: "inline-block",
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "7px",
    color: "#00F5FF",
    letterSpacing: "2px",
    textShadow: "0 0 6px #00F5FF",
    opacity: 0.8,
  };

  const titleStyle = {
    fontFamily: "'Orbitron', sans-serif",
    fontWeight: 900,
    fontSize: "15px",
    color: "#ffffff",
    letterSpacing: "1px",
    lineHeight: 1.3,
    textShadow: isPlaying
      ? "0 0 10px #FF006E, 0 2px 8px rgba(0,0,0,0.8)"
      : "0 2px 8px rgba(0,0,0,0.8)",
    margin: 0,
  };

  const buttonStyle = {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "8px",
    letterSpacing: "1px",
    border: "none",
    borderRadius: "3px",
    padding: "10px",
    cursor: "pointer",
    width: "100%",
    transition: "all 0.3s ease",
    ...(isPlaying
      ? {
          background: "#FF006E",
          color: "#ffffff",
          boxShadow: "0 0 12px #FF006E, 0 0 28px rgba(255,0,110,0.5)",
        }
      : {
          background: "rgba(255,0,110,0.15)",
          color: "#FF006E",
          border: "1px solid rgba(255,0,110,0.6)",
          boxShadow: "0 0 8px rgba(255,0,110,0.3)",
        }),
  };

  // Badge "reproduciendo" en la esquina superior
  const playingBadgeStyle = {
    position: "absolute",
    top: "12px",
    right: "12px",
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "7px",
    color: "#FF006E",
    background: "rgba(0,0,0,0.8)",
    border: "1px solid #FF006E",
    borderRadius: "3px",
    padding: "4px 8px",
    textShadow: "0 0 6px #FF006E",
    boxShadow: "0 0 8px rgba(255,0,110,0.4)",
  };

  // Placeholder si no hay imagen
  const placeholderStyle = {
    width: "100%",
    height: "100%",
    background: "linear-gradient(135deg, #1a0010, #0a0a1f)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "48px",
  };

  return (
    <div
      style={cardStyle}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      {film.imagen
        ? <img src={film.imagen} alt={film.nombre} style={imageStyle} />
        : <div style={placeholderStyle}>🎬</div>
      }

      <div style={overlayStyle} />
      <div style={scanlinesStyle} />

      {isPlaying && <div style={playingBadgeStyle}>▶ PLAY</div>}

      <div style={contentStyle}>
        <span style={vhsBadgeStyle}>▶ VHS</span>
        <p style={titleStyle}>{film.nombre}</p>
        <button
          style={buttonStyle}
          onClick={isPlaying ? onStop : () => onPlay(film.nombre)}
        >
          {isPlaying ? "■ STOP" : "▶ VER"}
        </button>
      </div>
    </div>
  );
}
