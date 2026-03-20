import { BrowserRouter, Route, Routes } from "react-router-dom";
import Homepage from "./pages/HomePage";
import Consolas from "./pages/Consolas";
import JuegosConsola from "./pages/Videogames";
import Netflix from "./pages/Netflix";
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Homepage></Homepage>} />
        <Route path="/consolas" element={<Consolas />} />
        <Route path="/juegos/:consolaNombre" element={<JuegosConsola />} />
        <Route path="/netflix" element={<Netflix />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
