import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound";
import AddArtists from "./pages/AddArtists";
import AddSongs from "./pages/AddSongs";
import SetTitle from "./pages/SetTitle";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/add-artists" element={<AddArtists />} />
        <Route path="/add-songs" element={<AddSongs />} />
        <Route path="/set-title" element={<SetTitle />} />
        <Route path="/404" element={<NotFound />} />
        <Route path="*" element={<Navigate to="/404" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
