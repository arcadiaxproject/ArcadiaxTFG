import React from 'react';
import BACKEND_URL from '../config.js'; // ✅ Usamos la IP desde .env

function Cartucho({ nombre, imagen, activo, consola }) {
  const handleToggle = async () => {
    try {
      if (activo) {
        const response = await fetch(`${BACKEND_URL}/arcade/reset`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          console.log(`El videojuego ${nombre} ha sido apagado.`);
          window.location.reload();
        } else {
          console.error('Error al apagar el videojuego.');
        }
      } else {
        const response = await fetch(`${BACKEND_URL}/arcade/videojuego/${nombre}/${consola}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ activo: true }),
        });

        if (response.ok) {
          console.log(`El videojuego ${nombre} ha sido encendido.`);
          window.location.reload();
        } else {
          console.error('Error al encender el videojuego.');
        }
      }
    } catch (error) {
      console.error('Error en la solicitud:', error);
    }
  };

  return (
    <div className="relative w-56 h-[320px] bg-gray-200 rounded-2xl shadow-2xl p-2 border-4 border-gray-700 mx-auto flex flex-col items-center">
      <div
        className={`w-40 h-24 rounded-lg border-2 border-gray-800 shadow-inner mb-2 ${
          activo ? 'bg-green-600' : 'bg-red-600'
        }`}
      >
        <img
          src={imagen}
          alt={nombre}
          className="w-full h-full object-cover rounded-lg"
        />
      </div>

      {/* Cruceta */}
      <div className="absolute left-4 bottom-16">
        <div className="w-8 h-2 bg-black rounded mb-1"></div>
        <div className="flex">
          <div className="w-2 h-8 bg-black rounded mr-1"></div>
          <div className="w-2 h-8 bg-black rounded ml-1"></div>
        </div>
        <div className="w-8 h-2 bg-black rounded mt-1"></div>
      </div>

      {/* Botón encendido */}
      <div className="absolute bottom-14 left-1/2 transform -translate-x-1/2">
        <button
          onClick={handleToggle}
          className={`w-10 h-10 rounded-full border-4 shadow-lg flex items-center justify-center ${
            activo ? 'bg-green-500 border-green-700' : 'bg-red-500 border-red-700'
          }`}
          style={{
            backgroundImage: `url(${
              activo ? '/assets/botones/encendido.png' : '/assets/botones/apagado.png'
            })`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
        />
      </div>

      {/* Botones A y B */}
      <div className="absolute right-4 bottom-12 flex flex-col space-y-2">
        <div className="bg-red-600 w-6 h-6 rounded-full shadow-lg"></div>
        <div className="bg-red-600 w-6 h-6 rounded-full shadow-lg"></div>
      </div>

      {/* Select y Start */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-2">
        <div className="bg-gray-800 w-12 h-4 rounded-lg shadow-inner text-center text-white text-xs"></div>
        <div className="bg-gray-800 w-12 h-4 rounded-lg shadow-inner text-center text-white text-xs"></div>
      </div>

      {/* Nombre */}
      <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2 text-sm font-bold text-gray-800">
        {nombre.toUpperCase()}
      </div>
    </div>
  );
}

export default Cartucho;
