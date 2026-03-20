import React, { useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { usePlayback } from "../../hooks/usePlayback";

const navLinks = [
  { to: "/", label: "INICIO" },
  { to: "/consolas", label: "ARCADES" },
  { to: "/peliculas", label: "HOMEFLIX" },
];

export default function Navbar() {
  const location = useLocation();
  const { current, stop, fetchCurrent } = usePlayback();
  useEffect(() => { fetchCurrent(); }, [fetchCurrent]);

  const navStyle = {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100%",
    zIndex: 1000,
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "1rem 2rem",
    background: "rgba(10, 10, 15, 0.85)",
    backdropFilter: "blur(12px)",
    WebkitBackdropFilter: "blur(12px)",
    borderBottom: "1px solid rgba(255, 230, 0, 0.3)",
    boxSizing: "border-box",
  };

  const logoStyle = {
    fontFamily: "'Press Start 2P', monospace",
    fontSize: "14px",
    letterSpacing: "2px",
    textDecoration: "none",
    userSelect: "none",
  };

  const logoArcadiaStyle = {
    color: "#ffffff",
  };

  const logoXStyle = {
    color: "#FFE600",
    textShadow: "0 0 6px #FFE600, 0 0 18px #FFE600, 0 0 32px rgba(255, 230, 0, 0.6)",
  };

  const linksContainerStyle = {
    display: "flex",
    gap: "2rem",
    alignItems: "center",
  };

  const getLinkStyle = (to) => {
    const isActive = location.pathname === to;
    return {
      fontFamily: "'Orbitron', sans-serif",
      fontWeight: 600,
      fontSize: "13px",
      letterSpacing: "1.5px",
      color: isActive ? "#FFE600" : "#ffffff",
      textDecoration: "none",
      textShadow: isActive
        ? "0 0 6px #FFE600, 0 0 14px rgba(255, 230, 0, 0.6)"
        : "none",
      borderBottom: isActive ? "2px solid #FFE600" : "2px solid transparent",
      paddingBottom: "2px",
      transition: "color 0.2s, text-shadow 0.2s, border-bottom-color 0.2s",
    };
  };

  const handleLinkMouseEnter = (e) => {
    e.currentTarget.style.color = "#FFE600";
    e.currentTarget.style.textShadow = "0 0 6px #FFE600, 0 0 14px rgba(255, 230, 0, 0.6)";
  };

  const handleLinkMouseLeave = (e, to) => {
    const isActive = location.pathname === to;
    if (!isActive) {
      e.currentTarget.style.color = "#ffffff";
      e.currentTarget.style.textShadow = "none";
    }
  };

  return (
    <nav style={navStyle}>
      <Link to="/" style={{ textDecoration: "none" }}>
        <span style={logoStyle}>
          <span style={logoArcadiaStyle}>ARCADIA</span>
          <span style={logoXStyle}>X</span>
        </span>
      </Link>

      <div style={linksContainerStyle}>
        {navLinks.map(({ to, label }) => (
          <Link
            key={to}
            to={to}
            style={getLinkStyle(to)}
            onMouseEnter={handleLinkMouseEnter}
            onMouseLeave={(e) => handleLinkMouseLeave(e, to)}
          >
            {label}
          </Link>
        ))}

        {current.type !== "none" && current.data?.nombre && (
          <div style={{
            display: "flex",
            alignItems: "center",
            gap: "10px",
            background: "rgba(0,255,65,0.08)",
            border: "1px solid rgba(0,255,65,0.4)",
            borderRadius: "4px",
            padding: "6px 12px",
            boxShadow: "0 0 8px rgba(0,255,65,0.2)",
          }}>
            <span style={{
              fontFamily: "'Orbitron', sans-serif",
              fontSize: "10px",
              color: "#00FF41",
              textShadow: "0 0 6px #00FF41",
              letterSpacing: "1px",
              maxWidth: "150px",
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
            }}>
              ▶ {current.data.nombre}
            </span>
            <button
              onClick={async () => { await stop(); window.location.reload(); }}
              style={{
                fontFamily: "'Press Start 2P', monospace",
                fontSize: "7px",
                background: "transparent",
                border: "1px solid rgba(255,0,0,0.6)",
                color: "#FF3333",
                borderRadius: "2px",
                padding: "4px 8px",
                cursor: "pointer",
                letterSpacing: "1px",
                boxShadow: "0 0 6px rgba(255,0,0,0.3)",
                flexShrink: 0,
              }}
            >
              ■ STOP
            </button>
          </div>
        )}
      </div>
    </nav>
  );
}
