import React from "react";
import Layout from "../components/layout/Layout";
import Loading from "../components/layout/Loading";
import ErrorMessage from "../components/layout/ErrorMessage";
import ConsoleCard from "../components/videogames/ConsoleCard";
import { useConsoles } from "../hooks/useVideogames";

export default function Consoles() {
  const { consoles, loading, error } = useConsoles();

  return (
    <Layout>
      <h2>Elige tu consola</h2>
      {loading && <Loading text="Cargando consolas..." />}
      {error && <ErrorMessage message={error} />}
      {!loading && !error && (
        <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
          {consoles.length > 0
            ? consoles.map((c) => <ConsoleCard key={c} consola={c} />)
            : <p>No hay consolas disponibles.</p>
          }
        </div>
      )}
    </Layout>
  );
}
