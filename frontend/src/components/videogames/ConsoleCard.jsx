import React from "react";
import { useNavigate } from "react-router-dom";

export default function ConsoleCard({ consola }) {
  const navigate = useNavigate();
  return (
    <button
      onClick={() => navigate(`/juegos/${consola.toLowerCase()}`)}
      style={{ padding: "16px 24px", background: "#333", color: "#fff", border: "1px solid #555", borderRadius: "6px", cursor: "pointer", fontSize: "14px" }}
    >
      {consola.toUpperCase()}
    </button>
  );
}
