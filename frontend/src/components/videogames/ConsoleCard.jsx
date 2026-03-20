import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

// Colores por consola
const CONSOLE_THEMES = {
  nes:      { color: "#FFE600", glow: "rgba(255,230,0,0.5)",    label: "NES",       year: "1983" },
  snes:     { color: "#9B59B6", glow: "rgba(155,89,182,0.5)",   label: "SNES",      year: "1990" },
  n64:      { color: "#00FF41", glow: "rgba(0,255,65,0.5)",     label: "N64",       year: "1996" },
  gba:      { color: "#00F5FF", glow: "rgba(0,245,255,0.5)",    label: "GBA",       year: "2001" },
  psp:      { color: "#FF6B00", glow: "rgba(255,107,0,0.5)",    label: "PSP",       year: "2005" },
  ps1:      { color: "#0080FF", glow: "rgba(0,128,255,0.5)",    label: "PS1",       year: "1994" },
  megadrive:{ color: "#FF006E", glow: "rgba(255,0,110,0.5)",    label: "MEGA DRIVE",year: "1988" },
};

const DEFAULT_THEME = { color: "#FFE600", glow: "rgba(255,230,0,0.5)", label: "CONSOLE", year: "???" };

export default function ConsoleCard({ consola }) {
  const navigate = useNavigate();
  const [hovered, setHovered] = useState(false);
  const theme = CONSOLE_THEMES[consola?.toLowerCase()] || DEFAULT_THEME;

  const cardStyle = {
    background: "linear-gradient(145deg, #141420, #0d0d18)",
    border: `2px solid ${hovered ? theme.color : theme.color + "80"}`,
    boxShadow: hovered
      ? `0 0 20px ${theme.glow}, 0 0 50px ${theme.color}30, 0 12px 40px rgba(0,0,0,0.8)`
      : `0 0 8px ${theme.color}40, 0 4px 20px rgba(0,0,0,0.6)`,
    borderRadius: "10px",
    padding: "24px 20px 20px",
    cursor: "pointer",
    transform: hovered ? "translateY(-10px) scale(1.04)" : "translateY(0) scale(1)",
    transition: "all 0.3s ease",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "16px",
    width: "200px",
    userSelect: "none",
    position: "relative",
    overflow: "hidden",
  };

  // Scanlines en la card
  const cardScanlinesStyle = {
    position: "absolute",
    inset: 0,
    backgroundImage: "repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,0.08) 3px, rgba(0,0,0,0.08) 4px)",
    pointerEvents: "none",
    opacity: 0.5,
    borderRadius: "10px",
  };

  /* ── NES CSS art ── */
  const nesBodyStyle = {
    width: "150px",
    height: "96px",
    background: "linear-gradient(180deg, #3d3d3d 0%, #2a2a2a 60%, #222 100%)",
    borderRadius: "6px 6px 12px 12px",
    position: "relative",
    border: "2px solid #1a1a1a",
    boxShadow: "inset 0 2px 4px rgba(255,255,255,0.08), inset 0 -3px 6px rgba(0,0,0,0.5)",
    flexShrink: 0,
  };

  const cartridgeSlotStyle = {
    position: "absolute",
    top: "8px",
    left: "50%",
    transform: "translateX(-50%)",
    width: "56px",
    height: "16px",
    background: "#080808",
    borderRadius: "2px 2px 4px 4px",
    border: "1px solid #111",
    boxShadow: "inset 0 3px 6px rgba(0,0,0,0.9)",
  };

  const frontLabelStyle = {
    position: "absolute",
    top: "30px",
    left: "50%",
    transform: "translateX(-50%)",
    width: "108px",
    height: "40px",
    background: `linear-gradient(135deg, #0d0d20, #1a0a30)`,
    borderRadius: "3px",
    border: `1px solid ${theme.color}60`,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    boxShadow: `inset 0 1px 3px rgba(0,0,0,0.6), 0 0 6px ${theme.color}30`,
  };

  const nesTextStyle = {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "9px",
    color: theme.color,
    textShadow: `0 0 6px ${theme.color}`,
    letterSpacing: "1px",
  };

  const bottomRowStyle = {
    position: "absolute",
    bottom: "12px",
    left: 0,
    right: 0,
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 16px",
  };

  const portStyle = {
    width: "16px",
    height: "16px",
    borderRadius: "50%",
    background: "radial-gradient(circle at 40% 35%, #2a2a2a, #111)",
    border: "2px solid #0d0d0d",
    boxShadow: "inset 0 1px 3px rgba(0,0,0,0.9), 0 1px 1px rgba(255,255,255,0.04)",
  };

  const powerLedStyle = {
    width: "8px",
    height: "8px",
    borderRadius: "50%",
    background: hovered ? theme.color : "#440000",
    boxShadow: hovered
      ? `0 0 6px ${theme.color}, 0 0 14px ${theme.glow}`
      : "0 0 2px #440000",
    transition: "all 0.3s ease",
  };

  const consoleLabelStyle = {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "9px",
    color: theme.color,
    textShadow: `0 0 6px ${theme.color}, 0 0 14px ${theme.glow}`,
    letterSpacing: "2px",
    textAlign: "center",
    textTransform: "uppercase",
  };

  const yearBadgeStyle = {
    fontFamily: "'Orbitron', sans-serif",
    fontSize: "9px",
    color: "rgba(255,255,255,0.4)",
    letterSpacing: "2px",
  };

  const insertStyle = {
    fontFamily: "'Orbitron', sans-serif",
    fontSize: "7px",
    color: hovered ? theme.color : "rgba(255,255,255,0.2)",
    letterSpacing: "2px",
    textShadow: hovered ? `0 0 6px ${theme.color}` : "none",
    transition: "all 0.3s ease",
    marginTop: "-8px",
  };

  return (
    <div
      style={cardStyle}
      onClick={() => navigate(`/juegos/${consola.toLowerCase()}`)}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === "Enter" && navigate(`/juegos/${consola.toLowerCase()}`)}
    >
      <div style={cardScanlinesStyle} />

      {/* NES CSS Art */}
      <div style={nesBodyStyle}>
        <div style={cartridgeSlotStyle} />
        <div style={frontLabelStyle}>
          <span style={nesTextStyle}>{theme.label}</span>
        </div>
        <div style={bottomRowStyle}>
          <div style={portStyle} />
          <div style={powerLedStyle} />
          <div style={portStyle} />
        </div>
      </div>

      <span style={consoleLabelStyle}>{consola.toUpperCase()}</span>
      <span style={yearBadgeStyle}>{theme.year}</span>
      <span style={insertStyle}>▶ INSERT COIN</span>
    </div>
  );
}
