import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Navbar from "../components/navbar.jsx";
import Cartucho from "../components/Cartucho.jsx";
import BACKEND_URL from "../config.js"; // ✅ usamos la variable desde .env

function Videogames() {
  const { consolaNombre } = useParams();
  const [juegos, setJuegos] = useState([]);

  useEffect(() => {
    const fetchJuegos = async () => {
      try {
        const response = await fetch(
          `${BACKEND_URL}/arcade/juegos/${consolaNombre}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        if (!response.ok) {
          throw new Error("Error en la solicitud");
        }
        const data = await response.json();
        setJuegos(data);
      } catch (error) {
        console.error("Error al obtener los juegos:", error);
      }
    };

    if (consolaNombre) fetchJuegos();
  }, [consolaNombre]);

  return (
    <div
      className="min-h-screen bg-black"
      style={{
        backgroundImage: `url('/assets/fondo/comecocos.jpg')`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundAttachment: "fixed",
      }}
    >
      {/* Navbar */}
      <div className="fixed top-0 left-0 w-full z-50 bg-black bg-opacity-80">
        <Navbar />
      </div>

      {/* Título */}
      <div className="pt-32 text-center">
        <h1 className="text-3xl sm:text-5xl font-bold text-yellow-400 retro-title tracking-wide">
          <span className="bg-black px-4 py-2 rounded-lg shadow-lg border-2 border-yellow-400">
            JUEGOS PARA <span>{consolaNombre.toUpperCase()}</span>
          </span>
        </h1>
      </div>

      {/* Contenido */}
      <div className="flex justify-center mt-8 px-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8 w-full max-w-5xl">
          {juegos.length > 0 ? (
            juegos.map((juego, index) => (
              <Cartucho
                key={index}
                nombre={juego.nombre}
                consola={juego.consola}
                activo={juego.play}
                imagen={`/assets/videojuegos/${juego.imagen}`}
              />
            ))
          ) : (
            <p className="text-white text-lg sm:text-xl col-span-full text-center">
              No hay juegos disponibles para esta consola
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Videogames;
