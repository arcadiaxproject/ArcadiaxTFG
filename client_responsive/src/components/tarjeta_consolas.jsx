import React from 'react';
import { useNavigate } from 'react-router-dom';

function ConsolaItem({ consola }) {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/juegos/${consola.toLowerCase()}`);
  };

  return (
    <button
      onClick={handleClick}
      type="button"
      className="w-full max-w-[160px] sm:max-w-[140px] md:max-w-[150px] h-[180px] sm:h-[160px] md:h-[180px] bg-yellow-400 hover:bg-yellow-300 transition duration-300 rounded-md shadow-md flex flex-col justify-between items-center p-2 border-[2px] border-yellow-600"
    >
      {/* Pestaña superior */}
      <div className="w-full h-1 bg-yellow-200 rounded-t-sm mb-1"></div>

      {/* Imagen */}
      <div className="w-full h-[90px] sm:h-[70px] md:h-[90px] flex items-center justify-center overflow-hidden rounded">
        <img
          src={`/assets/consolas/${encodeURIComponent(consola)}.jpg`}
          alt={consola}
          className="object-contain h-full w-full"
          onError={(e) => {
            e.target.src = '/assets/consolas/consolas.jpg';
          }}
        />
      </div>

      {/* Texto */}
      <span className="mt-1 text-black text-center text-xs md:text-sm font-bold font-[PressStart2P] tracking-tight leading-tight">
        {consola.toUpperCase()}
      </span>
    </button>
  );
}

export default ConsolaItem;
