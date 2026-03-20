import React, { useState } from "react";

export default function GameCard({ game, onPlay, onStop, isPlaying }) {
  const [hovered, setHovered] = useState(false);

  const cardStyle = {
    background: "linear-gradient(145deg, #141420, #0d0d18)",
    border: isPlaying
      ? "2px solid #00FF41"
      : hovered
        ? "2px solid #00F5FF"
        : "2px solid rgba(0,245,255,0.35)",
    boxShadow: isPlaying
      ? "0 0 16px #00FF41, 0 0 40px rgba(0, 255, 65, 0.35), 0 8px 30px rgba(0,0,0,0.7)"
      : hovered
        ? "0 0 14px #00F5FF, 0 0 40px rgba(0,245,255,0.3), 0 12px 40px rgba(0,0,0,0.7)"
        : "0 4px 20px rgba(0,0,0,0.6)",
    borderRadius: "8px",
    padding: "0",
    overflow: "hidden",
    display: "flex",
    flexDirection: "column",
    transform: hovered && !isPlaying ? "translateY(-6px)" : "translateY(0)",
    transition: "all 0.3s ease",
    position: "relative",
  };

  // Cartucho CSS en la parte superior de la card
  const cartridgeStyle = {
    background: isPlaying
      ? "linear-gradient(135deg, #001a00, #003300)"
      : "linear-gradient(135deg, #0a0020, #150030)",
    borderBottom: `2px solid ${isPlaying ? "#00FF41" : "#00F5FF"}40`,
    padding: "18px 16px 12px",
    display: "flex",
    alignItems: "center",
    gap: "12px",
    position: "relative",
    overflow: "hidden",
  };

  // Scanlines dentro del cartucho
  const cartScanlinesStyle = {
    position: "absolute",
    inset: 0,
    backgroundImage: "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 3px)",
    pointerEvents: "none",
  };

  // Cartucho icono
  const cartIconStyle = {
    width: "40px",
    height: "50px",
    background: isPlaying
      ? "linear-gradient(180deg, #003300 0%, #001a00 100%)"
      : "linear-gradient(180deg, #1a0035 0%, #0d0020 100%)",
    border: `2px solid ${isPlaying ? "#00FF41" : "#00F5FF"}60`,
    borderRadius: "3px 3px 6px 6px",
    position: "relative",
    flexShrink: 0,
    boxShadow: isPlaying
      ? "0 0 8px rgba(0,255,65,0.4)"
      : "0 0 6px rgba(0,245,255,0.3)",
  };

  const cartConnectorStyle = {
    position: "absolute",
    bottom: 0,
    left: "6px",
    right: "6px",
    height: "8px",
    background: "#1a1a1a",
    borderRadius: "0 0 2px 2px",
    display: "flex",
    gap: "2px",
    padding: "0 2px",
    alignItems: "center",
  };

  const connectorPinStyle = (i) => ({
    flex: 1,
    height: "5px",
    background: i % 2 === 0 ? "#888" : "#666",
    borderRadius: "1px",
  });

  const cartLabelStyle = {
    position: "absolute",
    top: "6px",
    left: "4px",
    right: "4px",
    height: "24px",
    background: isPlaying
      ? "rgba(0,255,65,0.15)"
      : "rgba(0,245,255,0.12)",
    borderRadius: "2px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  };

  const cartLabelTextStyle = {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "4px",
    color: isPlaying ? "#00FF41" : "#00F5FF",
    textShadow: isPlaying ? "0 0 4px #00FF41" : "0 0 4px #00F5FF",
    letterSpacing: "0.5px",
    textAlign: "center",
    lineHeight: 1.2,
    padding: "0 2px",
  };

  const gameInfoStyle = {
    flex: 1,
  };

  const gameNameStyle = {
    fontFamily: "'Orbitron', sans-serif",
    fontWeight: 700,
    fontSize: "13px",
    color: "#ffffff",
    letterSpacing: "0.5px",
    lineHeight: 1.4,
    margin: "0 0 6px 0",
    textShadow: isPlaying ? "0 0 8px #00FF41" : "none",
  };

  const consoleBadgeStyle = {
    display: "inline-block",
    fontFamily: "'Orbitron', sans-serif",
    fontWeight: 600,
    fontSize: "9px",
    color: "#FFE600",
    textShadow: "0 0 4px rgba(255, 230, 0, 0.5)",
    border: "1px solid rgba(255, 230, 0, 0.4)",
    borderRadius: "2px",
    padding: "1px 6px",
    letterSpacing: "1px",
  };

  // Área inferior con botón
  const bottomStyle = {
    padding: "12px 16px 14px",
    background: "rgba(0,0,0,0.3)",
    borderTop: "1px solid rgba(255,255,255,0.05)",
  };

  const playButtonStyle = {
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
          background: "#00FF41",
          color: "#000000",
          boxShadow: "0 0 10px #00FF41, 0 0 24px rgba(0,255,65,0.5)",
        }
      : {
          background: "rgba(255,0,0,0.15)",
          color: "#FF3333",
          border: "1px solid rgba(255,0,0,0.6)",
          boxShadow: "0 0 8px rgba(255,0,0,0.3)",
        }),
  };

  return (
    <div
      style={cardStyle}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      {/* Cartucho + info */}
      <div style={cartridgeStyle}>
        <div style={cartScanlinesStyle} />
        {/* Icono cartucho */}
        <div style={cartIconStyle}>
          <div style={cartLabelStyle}>
            <span style={cartLabelTextStyle}>
              {game.nombre?.substring(0, 8).toUpperCase()}
            </span>
          </div>
          <div style={cartConnectorStyle}>
            {[0,1,2,3,4].map(i => <div key={i} style={connectorPinStyle(i)} />)}
          </div>
        </div>

        {/* Info */}
        <div style={gameInfoStyle}>
          <p style={gameNameStyle}>{game.nombre}</p>
          <span style={consoleBadgeStyle}>{game.consola?.toUpperCase()}</span>
        </div>
      </div>

      {/* Botón jugar */}
      <div style={bottomStyle}>
        <button
          style={playButtonStyle}
          onClick={isPlaying ? onStop : () => onPlay(game.nombre, game.consola)}
        >
          {isPlaying ? "■ STOP" : "▶ JUGAR"}
        </button>
      </div>
    </div>
  );
}
