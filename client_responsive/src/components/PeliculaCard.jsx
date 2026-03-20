import React from "react";

function PeliculaCard({ pelicula, onPlayToggle }) {
  const handlePlayClick = () => {
    onPlayToggle(pelicula.nombre);
  };

  return (
    <div
      onClick={handlePlayClick}
      className={`relative bg-black border-4 rounded-lg w-64 h-40 shadow-lg hover:scale-105 transition-all cursor-pointer ${
        pelicula.play ? "shadow-green-500" : "shadow-red-500"
      }`}
    >
      {/* Bobinas pequeñas */}
      <div className="absolute top-[20%] left-4 w-16 h-16 bg-gray-600 rounded-full border-2 border-black"></div>
      <div className="absolute top-[20%] right-4 w-16 h-16 bg-gray-600 rounded-full border-2 border-black"></div>

      {/* Imagen centrada */}
      <div className="absolute inset-0 flex items-center justify-center">
        <img
          src={`/assets/netflix/peliculas/${pelicula.imagen}`}
          alt={pelicula.nombre}
          className="w-28 h-24 object-cover rounded-md shadow-inner"
        />
      </div>

      {/* Indicador inferior */}
      <div className="absolute bottom-1 left-1 px-2 py-0.5 bg-black bg-opacity-75 text-white text-xs font-bold rounded max-w-[90%] overflow-hidden whitespace-nowrap text-ellipsis">
        {pelicula.play ? "Reproduciendo" : pelicula.nombre.toUpperCase()}
      </div>
    </div>
  );
}

export default PeliculaCard;
