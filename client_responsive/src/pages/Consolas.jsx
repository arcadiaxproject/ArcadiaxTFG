import React, { useEffect, useState } from "react";
import axios from "axios";
import ConsolaItem from "../components/tarjeta_consolas.jsx";
import Navbar from "../components/navbar.jsx";
import BACKEND_URL from "../config.js"; // 🟢 Aquí importamos la URL del backend

function Consolas() {
  const [competitivoConsolas, setCompetitivoConsolas] = useState([]);
  const [historiaConsola, setHistoriaConsola] = useState(null);
  console.log("Backend URL:", BACKEND_URL);

  useEffect(() => {
    const fetchCompetitivoConsolas = async () => {
      try {
        const response = await axios.get(`${BACKEND_URL}/arcade/consolas`, {
          withCredentials: true,
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (Array.isArray(response.data)) {
          setCompetitivoConsolas(response.data);
        } else {
          console.error("Respuesta inesperada del servidor:", response.data);
        }
      } catch (error) {
        console.error("Error en la solicitud:", error.message);
      }
    };

    const fetchHistoriaConsola = async () => {
      try {
        const response = await axios.get(`${BACKEND_URL}/consolas/historia`, {
          withCredentials: true,
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (typeof response.data === "string" || response.data instanceof String) {
          setHistoriaConsola(response.data);
        } else {
          console.error("Respuesta no es una cadena:", response.data);
        }
      } catch (error) {
        console.error("Error en la solicitud:", error.message);
      }
    };

    fetchCompetitivoConsolas();
    fetchHistoriaConsola();
  }, []);

  return (
    <div
      className="min-h-screen bg-black"
      style={{
        backgroundImage: `url('/assets/fondo/arcade.jpg')`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundAttachment: "fixed",
      }}
    >
      <div className="fixed top-0 left-0 w-full z-50">
        <Navbar />
      </div>

      <div className="pt-20 px-2 pb-4 flex flex-col items-center justify-start min-h-screen">
        <div className="mb-4 w-full">
          <h2 className="text-lg sm:text-xl md:text-2xl font-bold text-center mb-4 uppercase tracking-wide"
              style={{
                color: "#010203",
                textShadow: `0 0 4px #ff1a1a, 0 0 10px #ff1a1a, 0 0 20px #ff0000`,
                fontFamily: '"Orbitron", sans-serif',
              }}
          >
            SUPERVIVENCIA
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 max-w-6xl mx-auto justify-items-center">
            {competitivoConsolas.length > 0 ? (
              competitivoConsolas.map((consola, index) => (
                <ConsolaItem key={`competitivo-${index}`} consola={consola} />
              ))
            ) : (
              <p className="text-white text-sm col-span-full text-center">
                No hay consolas disponibles
              </p>
            )}
          </div>
        </div>

        <div className="mt-2 w-full">
          <h2 className="text-lg sm:text-xl md:text-2xl font-bold text-center mb-4 uppercase tracking-wide"
              style={{
                color: "#010203",
                textShadow: `0 0 4px #00ff66, 0 0 10px #00ff66, 0 0 20px #00cc44`,
                fontFamily: '"Orbitron", sans-serif',
              }}
          >
            MODO HISTORIA
          </h2>
          <div className="flex justify-center">
            <div className="w-full max-w-6xl flex justify-center">
              {historiaConsola ? (
                <ConsolaItem consola={historiaConsola} />
              ) : (
                <p className="text-white text-sm text-center">
                  No hay consolas disponibles
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Consolas;
