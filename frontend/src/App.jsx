import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Consoles from "./pages/Consoles";
import Games from "./pages/Games";
import Films from "./pages/Films";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/consolas" element={<Consoles />} />
        <Route path="/juegos/:consolaNombre" element={<Games />} />
        <Route path="/peliculas" element={<Films />} />
      </Routes>
    </BrowserRouter>
  );
}
