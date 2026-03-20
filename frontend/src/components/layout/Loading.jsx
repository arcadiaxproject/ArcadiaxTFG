import React from "react";

export default function Loading({ text = "CARGANDO..." }) {
  const containerStyle = {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    padding: "60px 20px",
    width: "100%",
  };

  const textStyle = {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "14px",
    color: "#FFE600",
    letterSpacing: "3px",
    animation: "neonPulse 1.4s ease-in-out infinite",
  };

  return (
    <div style={containerStyle}>
      <span style={textStyle}>{text.toUpperCase()}</span>
    </div>
  );
}
