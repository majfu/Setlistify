import { useState } from "react";
import { useNavigate } from "react-router-dom";
import InputField from "../components/InputField";
import AppButton from "../components/AppButton";
import { createPlaylist } from "../AppService";
import type {
  ArtistRecommendation,
  RecommendationsResponse,
} from "../models/recommendations";
import type { SelectedTrack } from "../models/playlists";

const RECOMMENDATIONS_STORAGE_KEY = "setlistify:recommendations";
const HOME_PAGE_PATH = "/home";

function getSelectedTracks(): SelectedTrack[] {
  const stored = sessionStorage.getItem(RECOMMENDATIONS_STORAGE_KEY);
  if (!stored) return [];

  const parsed: RecommendationsResponse = JSON.parse(stored);
  return (parsed.recommendations ?? []).flatMap((rec: ArtistRecommendation) =>
    Object.entries(rec.tracks)
      .filter(([, track]) => track.isSelected)
      .map(([title, track]) => ({
        title,
        artistName: rec.artistName,
        uri: track.uri,
        isAIRecommended: track.isAIRecommended,
        popularity: track.popularity,
        isSelected: track.isSelected,
      })),
  );
}

function SetTitle() {
  const navigate = useNavigate();
  const [playlistTitle, setPlaylistTitle] = useState<string>("");

  const handleCreatePlaylist = async () => {
    try {
      await createPlaylist(playlistTitle, getSelectedTracks());
      alert("Playlist successfully created!");
    } catch {
      alert("Sorry, something went wrong during playlist creation");
    } finally {
      navigate(HOME_PAGE_PATH);
    }
  };

  return (
    <div className="flex flex-col items-center text-4xl mt-30 gap-10">
      <div className="text-5xl mb-40 bg-sky-100 p-10 rounded-3xl">
        So close to the perfect playlist!
      </div>
      <div className="text-3xl bg-sky-100 p-6 rounded-3xl text-center mb-15">
        Playlist title:
      </div>
      <InputField
        placeholderText="Title..."
        userInput={playlistTitle}
        setUserInput={setPlaylistTitle}
        width={1200}
        height={90}
      />
      <div className="mt-10">
        <AppButton
          text="Create playlist!"
          width={600}
          height={70}
          onClick={handleCreatePlaylist}
        />
      </div>
    </div>
  );
}
export default SetTitle;
