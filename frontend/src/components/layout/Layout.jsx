import React from "react";
import Navbar from "./Navbar";

export default function Layout({ children }) {
  return (
    <div style={{ minHeight: "100vh", background: "#111", color: "#fff" }}>
      <Navbar />
      <main style={{ padding: "24px" }}>{children}</main>
    </div>
  );
}
