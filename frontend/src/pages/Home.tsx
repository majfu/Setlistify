import { useNavigate } from "react-router-dom";
import AppButton from "../components/AppButton";

const ADD_ARTISTS_PAGE_PATH = "/add-artists";
const BROWSE_PAGE_PATH = "/browse";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-around">
      <div className="text-5xl mb-50 bg-sky-100 rounded-3xl p-20">
        What would you like to do?
      </div>
      <div className="flex flex-col gap-20">
        <AppButton
          text="Create new playlist"
          width={800}
          height={100}
          onClick={() => navigate(ADD_ARTISTS_PAGE_PATH)}
        />
        <AppButton
          text="Browse playlists"
          width={800}
          height={100}
          onClick={() => navigate(BROWSE_PAGE_PATH)}
        />
      </div>
    </div>
  );
}
export default Home;
