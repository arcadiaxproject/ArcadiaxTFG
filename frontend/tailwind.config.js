module.exports = {
  content: ["./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        arcade: ['"Press Start 2P"', "monospace"],
        orbitron: ["Orbitron", "sans-serif"],
      },
      colors: {
        neon: {
          cyan: "#00f5ff",
          pink: "#ff00e5",
          yellow: "#ffe600",
          green: "#00ff66",
          red: "#ff1a1a",
        },
      },
      animation: {
        "pulse-neon": "pulseNeon 2s ease-in-out infinite",
        "fade-in": "fadeIn 0.3s ease-out",
      },
      keyframes: {
        pulseNeon: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.7" },
        },
        fadeIn: {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};
