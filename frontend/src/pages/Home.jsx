import React, { useEffect } from "react";
import Navbar from "../components/layout/Navbar";
import { usePlayback } from "../hooks/usePlayback";

// La imagen se carga desde public/assets/ para evitar errores si no existe aún
const arcadeBg = process.env.PUBLIC_URL + '/assets/arcade-bg.jpg';

export default function Home() {
  const { current, fetchCurrent } = usePlayback();

  useEffect(() => { fetchCurrent(); }, [fetchCurrent]);

  const heroStyle = {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100vw",
    height: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backgroundImage: arcadeBg ? `url('${arcadeBg}')` : "none",
    backgroundSize: "cover",
    backgroundPosition: "center",
    backgroundRepeat: "no-repeat",
    backgroundColor: "#0a0a0f",
  };

  const overlayStyle = {
    position: "absolute",
    inset: 0,
    background: "rgba(0, 0, 0, 0.6)",
    zIndex: 0,
  };

  const contentStyle = {
    position: "relative",
    zIndex: 1,
    border: "2px solid #FFE600",
    boxShadow: "0 0 12px #FFE600, 0 0 40px rgba(255, 230, 0, 0.35), inset 0 0 30px rgba(255, 230, 0, 0.05)",
    background: "rgba(0, 0, 0, 0.7)",
    padding: "2.5rem",
    maxWidth: "600px",
    width: "90%",
    borderRadius: "4px",
    textAlign: "center",
  };

  const titleStyle = {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "clamp(20px, 4vw, 36px)",
    color: "#FFE600",
    textShadow: "0 0 8px #FFE600, 0 0 24px #FFE600, 0 0 48px rgba(255, 230, 0, 0.5)",
    marginBottom: "1.2rem",
    letterSpacing: "3px",
  };

  const subtitleStyle = {
    fontFamily: "'Orbitron', sans-serif",
    fontWeight: 600,
    fontSize: "clamp(13px, 2vw, 18px)",
    color: "#ffffff",
    letterSpacing: "2px",
    marginBottom: "1.5rem",
    opacity: 0.85,
  };

  const descriptionStyle = {
    fontFamily: "'Orbitron', sans-serif",
    fontWeight: 400,
    fontSize: "13px",
    color: "#cccccc",
    lineHeight: 1.8,
    marginBottom: current.type !== "none" ? "1.5rem" : 0,
  };

  const playingBadgeStyle = {
    display: "inline-block",
    fontFamily: "'Orbitron', sans-serif",
    fontWeight: 700,
    fontSize: "12px",
    color: "#00FF41",
    textShadow: "0 0 6px #00FF41, 0 0 14px rgba(0, 255, 65, 0.6)",
    border: "1px solid #00FF41",
    boxShadow: "0 0 8px rgba(0, 255, 65, 0.4)",
    borderRadius: "4px",
    padding: "6px 14px",
    marginTop: "0.5rem",
    letterSpacing: "1px",
  };

  return (
    <div style={heroStyle} className="scanlines">
      <Navbar />
      <div style={overlayStyle} />
      <div style={contentStyle}>
        <h1 style={titleStyle}>ARCADIAX</h1>
        <p style={subtitleStyle}>Tu Arcade en Casa</p>
        <p style={descriptionStyle}>
          ArcadiaX es una plataforma arcade retro que te permite jugar a tus videojuegos clásicos favoritos
          y disfrutar de tus películas desde un único lugar. Selecciona tu consola, elige tu juego y comienza a jugar.
        </p>
        {current.type !== "none" && current.data?.nombre && (
          <div>
            <span style={playingBadgeStyle}>
              &#9658; Reproduciendo: {current.data.nombre}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
