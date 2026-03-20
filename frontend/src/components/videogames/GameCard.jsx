import React from "react";

export default function GameCard({ game, onPlay, onStop, isPlaying }) {
  return (
    <div style={{ border: isPlaying ? "2px solid #0f0" : "1px solid #555", borderRadius: "6px", padding: "16px", background: "#222", minWidth: "160px" }}>
      <p style={{ margin: "0 0 8px", fontWeight: "bold" }}>{game.nombre}</p>
      <p style={{ margin: "0 0 12px", color: "#aaa", fontSize: "12px" }}>{game.consola.toUpperCase()}</p>
      {isPlaying ? (
        <button onClick={onStop} style={{ background: "#c00", color: "#fff", border: "none", borderRadius: "4px", padding: "6px 12px", cursor: "pointer" }}>
          Parar
        </button>
      ) : (
        <button onClick={() => onPlay(game.nombre, game.consola)} style={{ background: "#060", color: "#fff", border: "none", borderRadius: "4px", padding: "6px 12px", cursor: "pointer" }}>
          Jugar
        </button>
      )}
    </div>
  );
}
