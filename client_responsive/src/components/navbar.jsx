import React, { useState } from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="fixed top-0 left-0 w-full bg-gradient-to-r from-gray-900 via-black to-gray-900 p-4 shadow-lg z-50">
      <div className="flex items-center justify-between">
        {/* Logo */}
        <div className="text-cyan-300 text-2xl md:text-3xl font-bold arcade-font">
          ArcadiaX
        </div>

        {/* Botón de Menú para pantallas pequeñas */}
        <button
          className="md:hidden text-white text-2xl hover:text-cyan-300 transition-all duration-300"
          onClick={() => setIsOpen(!isOpen)}
        >
          ☰
        </button>

        {/* Enlaces para pantallas grandes */}
        <div className="hidden md:flex gap-4 items-center ml-auto">
          <Link
            to="/"
            className="px-4 py-2 rounded-md border-2 border-cyan-300 text-cyan-300 text-center hover:bg-cyan-300 hover:text-black transition-all duration-300 text-sm md:text-base arcade-font"
          >
            🏠 Inicio
          </Link>
          <Link
            to="/consolas"
            className="px-4 py-2 rounded-md border-2 border-yellow-400 text-yellow-400 text-center hover:bg-yellow-400 hover:text-black transition-all duration-300 text-sm md:text-base arcade-font"
          >
            🕹️ Arcades
          </Link>
          <Link
            to="/netflix"
            className="px-4 py-2 rounded-md border-2 border-red-500 text-red-500 text-center hover:bg-red-500 hover:text-white transition-all duration-300 text-sm md:text-base arcade-font"
          >
            🍿 HOMEFLIX
          </Link>
         
        </div>
      </div>

      {/* Menú desplegable móvil */}
      <div
        className={`${
          isOpen ? "block" : "hidden"
        } md:hidden flex flex-col gap-4 mt-4 items-end`}
      >
        <Link
          to="/"
          className="px-4 py-2 rounded-md border-2 border-cyan-300 text-cyan-300 text-center hover:bg-cyan-300 hover:text-black transition-all duration-300 text-sm arcade-font"
        >
          🏠 Inicio
        </Link>
        <Link
          to="/consolas"
          className="px-4 py-2 rounded-md border-2 border-yellow-400 text-yellow-400 text-center hover:bg-yellow-400 hover:text-black transition-all duration-300 text-sm arcade-font"
        >
          🕹️ Arcades
        </Link>
        <Link
          to="/netflix"
          className="px-4 py-2 rounded-md border-2 border-red-500 text-red-500 text-center hover:bg-red-500 hover:text-white transition-all duration-300 text-sm arcade-font"
        >
          🍿 HOMEFLIX
        </Link>
        
      </div>
    </div>
  );
};

export default Navbar;
