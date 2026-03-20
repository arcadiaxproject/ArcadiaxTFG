import React, { useEffect } from "react";
import Layout from "../components/layout/Layout";
import { usePlayback } from "../hooks/usePlayback";

export default function Home() {
  const { current, fetchCurrent } = usePlayback();

  useEffect(() => { fetchCurrent(); }, [fetchCurrent]);

  return (
    <Layout>
      <h1>ArcadiaX</h1>
      <p>Selecciona Arcades para ver los videojuegos o Homeflix para las peliculas.</p>
      {current.type !== "none" && (
        <p style={{ color: "#0f0" }}>Reproduciendo: {current.data?.nombre}</p>
      )}
    </Layout>
  );
}
