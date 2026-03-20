import React from "react";

export default function ErrorMessage({ message, onRetry }) {
  const containerStyle = {
    border: "2px solid #FF0000",
    boxShadow: "0 0 10px #FF0000, 0 0 28px rgba(255, 0, 0, 0.35)",
    background: "rgba(255, 0, 0, 0.07)",
    borderRadius: "6px",
    padding: "20px 24px",
    display: "flex",
    flexDirection: "column",
    gap: "14px",
    alignItems: "flex-start",
    maxWidth: "500px",
  };

  const messageStyle = {
    fontFamily: "'Orbitron', sans-serif",
    fontWeight: 500,
    fontSize: "13px",
    color: "#ff4444",
    textShadow: "0 0 4px rgba(255, 68, 68, 0.5)",
    lineHeight: 1.6,
    margin: 0,
  };

  const retryButtonStyle = {
    fontFamily: "'Orbitron', sans-serif",
    fontWeight: 700,
    fontSize: "11px",
    letterSpacing: "1.5px",
    color: "#ffffff",
    background: "rgba(255, 0, 0, 0.3)",
    border: "1px solid rgba(255, 0, 0, 0.6)",
    borderRadius: "4px",
    padding: "8px 18px",
    cursor: "pointer",
    transition: "background 0.2s, box-shadow 0.2s",
  };

  return (
    <div style={containerStyle}>
      <p style={messageStyle}>{message}</p>
      {onRetry && (
        <button
          style={retryButtonStyle}
          onClick={onRetry}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = "rgba(255, 0, 0, 0.5)";
            e.currentTarget.style.boxShadow = "0 0 8px rgba(255, 0, 0, 0.5)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = "rgba(255, 0, 0, 0.3)";
            e.currentTarget.style.boxShadow = "none";
          }}
        >
          REINTENTAR
        </button>
      )}
    </div>
  );
}
