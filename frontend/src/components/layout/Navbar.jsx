import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav style={{ background: "#222", padding: "12px 24px", display: "flex", gap: "20px", alignItems: "center" }}>
      <span style={{ color: "#fff", fontWeight: "bold", fontSize: "18px" }}>ArcadiaX</span>
      <Link to="/" style={{ color: "#aaa", textDecoration: "none" }}>Inicio</Link>
      <Link to="/consolas" style={{ color: "#aaa", textDecoration: "none" }}>Arcades</Link>
      <Link to="/peliculas" style={{ color: "#aaa", textDecoration: "none" }}>Homeflix</Link>
    </nav>
  );
}
