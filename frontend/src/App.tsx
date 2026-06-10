import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound";
import Home from "./pages/Home";
import AddArtists from "./pages/AddArtists";
import AddSongs from "./pages/AddSongs";
import SetTitle from "./pages/SetTitle";
import Browse from "./pages/Browse";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/add-artists" element={<AddArtists />} />
        <Route path="/browse" element={<Browse />} />
        <Route path="/add-songs" element={<AddSongs />} />
        <Route path="/set-title" element={<SetTitle />} />
        <Route path="/404" element={<NotFound />} />
        <Route path="*" element={<Navigate to="/404" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
