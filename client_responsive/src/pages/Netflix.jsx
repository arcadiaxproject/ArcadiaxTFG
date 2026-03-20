import React, { useEffect, useState } from "react";
import PeliculaCard from "../components/PeliculaCard.jsx";
import Navbar from "../components/navbar.jsx";
import axios from "axios";
import BACKEND_URL from "../config.js"; // 🟢 Usamos el backend desde .env

function Netflix() {
  const [peliculas, setPeliculas] = useState([]);

  useEffect(() => {
    const fetchPeliculas = async () => {
      try {
        const response = await axios.get(`${BACKEND_URL}/multimedia/peliculas`, {
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (Array.isArray(response.data)) {
          setPeliculas(response.data);
        } else {
          console.error("Respuesta inesperada del servidor:", response.data);
        }
      } catch (error) {
        console.error("Error al obtener las películas:", error.message);
      }
    };

    fetchPeliculas();
  }, []);

  const handlePlayToggle = async (nombre) => {
    const peliculaActual = peliculas.find((p) => p.nombre === nombre);
    if (!peliculaActual) return;

    if (peliculaActual.play) {
      try {
        const response = await axios.put(`${BACKEND_URL}/pelicula/resetear`);
        if (response.status === 200) {
          setPeliculas((prev) =>
            prev.map((p) => ({ ...p, play: false }))
          );
        }
      } catch (error) {
        console.error("Error al resetear películas:", error);
      }
    } else {
      try {
        const response = await axios.put(
          `${BACKEND_URL}/multimedia/pelicula/${nombre}`,
          { play: true }
        );
        if (response.status === 200) {
          setPeliculas((prev) =>
            prev.map((p) =>
              p.nombre === nombre ? { ...p, play: true } : { ...p, play: false }
            )
          );
        }
      } catch (error) {
        console.error("Error al iniciar reproducción:", error);
      }
    }
  };

  return (
    <div
      className="min-h-screen w-full flex flex-col items-center justify-start"
      style={{
        backgroundImage: `url('/assets/fondo/tele.jpg')`,
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center center",
      }}
    >
      <Navbar />

      <div className="w-full max-w-[1440px] mt-32 p-4">
        <div className="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 justify-items-center">
          {peliculas.length > 0 ? (
            peliculas.map((pelicula, index) => (
              <PeliculaCard
                key={index}
                pelicula={pelicula}
                onPlayToggle={handlePlayToggle}
              />
            ))
          ) : (
            <p className="text-white font-mono text-2xl col-span-full text-center">
              🎞️ No hay películas disponibles
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Netflix;
