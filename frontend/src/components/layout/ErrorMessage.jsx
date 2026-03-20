import React from "react";

export default function ErrorMessage({ message, onRetry }) {
  return (
    <div style={{ color: "#f55", padding: "20px" }}>
      <p>{message}</p>
      {onRetry && <button onClick={onRetry}>Reintentar</button>}
    </div>
  );
}
