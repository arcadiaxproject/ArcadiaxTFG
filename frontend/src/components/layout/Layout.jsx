import React from "react";
import Navbar from "./Navbar";

export default function Layout({ children }) {
  const wrapperStyle = {
    minHeight: "100vh",
    background: "#0a0a0f",
    color: "#ffffff",
  };

  const mainStyle = {
    paddingTop: "80px",
    padding: "80px 2rem 2rem 2rem",
  };

  return (
    <div style={wrapperStyle}>
      <Navbar />
      <main style={mainStyle}>{children}</main>
    </div>
  );
}
