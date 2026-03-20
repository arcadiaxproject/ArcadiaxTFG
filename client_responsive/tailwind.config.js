/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // Analiza todos los archivos en src
  ],
  theme: {
    extend: {
      fontFamily: {
        orbitron: ['"Orbitron"', 'sans-serif'],
        matrix: ['"Courier New"', 'monospace'],
      }
    }
  },
  plugins: [], // Puedes agregar plugins aquí más adelante
};
