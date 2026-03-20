import React, { useEffect, useState } from "react";
import Navbar from "../components/navbar.jsx";

function HomePage() {
  const [audio, setAudio] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    const newAudio = new Audio("/assets/musica/sonic.mp3");
    newAudio.loop = true;
    setAudio(newAudio);
  }, []);

  const handleToggleMusic = () => {
    if (audio) {
      if (isPlaying) {
        audio.pause();
        setIsPlaying(false);
      } else {
        audio.play().catch((error) => {
          console.error("Error al reproducir el audio:", error);
        });
        setIsPlaying(true);
      }
    }
  };

  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center py-6"
      style={{
        backgroundImage: `url('/assets/fondo/arcade.png')`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <Navbar />

      {/* Botón para reproducir/pausar música */}
      <button
        className={`nes-btn ${
          isPlaying ? "is-warning" : "is-primary"
        } mt-6 px-6 py-3 text-sm md:text-base`}
        onClick={handleToggleMusic}
      >
        {isPlaying ? "🔇 Parar Música" : "🎵 Reproducir Música"}
      </button>

      {/* Cartel de neón */}
      <div className="w-10/12 sm:w-8/12 md:w-6/12 lg:w-4/12 p-6 rounded-lg bg-black bg-opacity-80 neon-sign text-center shadow-xl border-2 border-yellow-400 mt-8">
        <h2 className="text-3xl md:text-4xl font-extrabold mb-4 text-yellow-400 retro-font">
          ArcadiaX
        </h2>
        <p className="text-sm md:text-base text-cyan-300 leading-relaxed retro-font">
          Explora el mundo de los juegos clásicos con nuestra recreativa casera.
          Vive la nostalgia de los 80 con una selección de consolas retro,
          música y un ambiente arcade.
        </p>
        <p className="mt-4 text-sm md:text-base text-yellow-300 font-bold">
          ¡Prepárate para revivir la magia!
        </p>
      </div>
    </div>
  );
}

export default HomePage;
