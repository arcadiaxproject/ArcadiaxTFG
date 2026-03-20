import React from "react";
import Navbar from "../components/layout/Navbar";
import Loading from "../components/layout/Loading";
import ErrorMessage from "../components/layout/ErrorMessage";
import ConsoleCard from "../components/videogames/ConsoleCard";
import { useConsoles } from "../hooks/useVideogames";

export default function Consoles() {
  const { consoles, loading, error } = useConsoles();

  const pageStyle = {
    minHeight: "100vh",
    backgroundColor: "#0a0a0f",
    backgroundImage: `
      linear-gradient(rgba(255, 230, 0, 0.035) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 230, 0, 0.035) 1px, transparent 1px)
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
  };

  const headerStyle = {
    textAlign: "center",
    marginBottom: "3rem",
  };

  const titleStyle = {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "clamp(16px, 3.5vw, 36px)",
    color: "#FFE600",
    textShadow:
      "0 0 10px #FFE600, 0 0 30px rgba(255, 230, 0, 0.6), 0 0 60px rgba(255, 230, 0, 0.3)",
    letterSpacing: "6px",
    marginBottom: "0.8rem",
    display: "block",
  };

  const subtitleStyle = {
    fontFamily: "'Orbitron', sans-serif",
    fontSize: "11px",
    color: "#00F5FF",
    letterSpacing: "4px",
    textShadow: "0 0 6px #00F5FF",
    border: "1px solid rgba(0,245,255,0.4)",
    display: "inline-block",
    padding: "4px 14px",
    borderRadius: "2px",
    marginTop: "0.5rem",
  };

  const dividerStyle = {
    width: "200px",
    height: "2px",
    background: "linear-gradient(90deg, transparent, #FFE600, transparent)",
    margin: "1.5rem auto",
    boxShadow: "0 0 8px #FFE600",
  };

  const gridStyle = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
    gap: "28px",
    maxWidth: "1100px",
    margin: "0 auto",
    justifyItems: "center",
  };

  const emptyStyle = {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "12px",
    color: "rgba(255, 230, 0, 0.5)",
    textAlign: "center",
    padding: "60px 0",
    letterSpacing: "2px",
    gridColumn: "1 / -1",
  };

  return (
    <div style={pageStyle}>
      <Navbar />
      <div style={scanlinesStyle} />
      <div style={contentStyle}>
        <div style={headerStyle}>
          <span style={titleStyle}>ARCADE</span>
          <div>
            <span style={subtitleStyle}>▶ SELECCIONA TU CONSOLA</span>
          </div>
          <div style={dividerStyle} />
        </div>

        {loading && <Loading />}
        {error && <ErrorMessage message={error} />}

        {!loading && !error && (
          <div style={gridStyle}>
            {consoles.length > 0
              ? consoles.map((c) => <ConsoleCard key={c} consola={c} />)
              : <p style={emptyStyle}>NO HAY CONSOLAS DISPONIBLES</p>
            }
          </div>
        )}
      </div>
    </div>
  );
}
