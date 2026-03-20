import React from "react";

export default function Loading({ text = "Cargando..." }) {
  return <p style={{ color: "#aaa", padding: "20px" }}>{text}</p>;
}
