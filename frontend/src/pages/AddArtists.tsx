import { useEffect, useState } from "react";
import InputField from "../components/InputField";
import ArtistsList from "../components/ArtistsList";
import AppButton from "../components/AppButton";
import { getTrackRecommendations } from "../AppService";
import LoadingOverlay from "../components/LoadingOverlay";
import { useNavigate } from "react-router-dom";

const ARTISTS_STORAGE_KEY = "setlistify:artistsList";
const RECOMMENDATIONS_STORAGE_KEY = "setlistify:recommendations";
const ADD_SONGS_PAGE_PATH = "/add-songs";

function AddArtists() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [artistInput, setArtistInput] = useState<string>("");

  const [artistsList, setArtistsList] = useState<string[]>(() => {
    const stored = sessionStorage.getItem(ARTISTS_STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  });

  useEffect(() => {
    sessionStorage.setItem(ARTISTS_STORAGE_KEY, JSON.stringify(artistsList));
  }, [artistsList]);

  const addArtistToList = () => {
    if (!artistInput.length) return;
    setArtistsList([...artistsList, artistInput]);
    setArtistInput("");
  };

  const removeArtistFromList = (artist: string) => {
    setArtistsList(artistsList.filter((a) => a !== artist));
  };

  const getRecommendations = async () => {
    if (!artistsList.length) {
      alert("Add at least one artist to get recommendations");
      return;
    }

    setIsLoading(true);

    const recommendationsData = await getTrackRecommendations(artistsList);
    sessionStorage.setItem(
      RECOMMENDATIONS_STORAGE_KEY,
      JSON.stringify(recommendationsData),
    );

    setIsLoading(false);
    navigate(ADD_SONGS_PAGE_PATH);
  };

  return (
    <div className="flex flex-col">
      {isLoading && <LoadingOverlay infoText="Fetching recommendations..." />}

      <div className="self-center text-5xl mb-40 bg-sky-100 p-10 rounded-3xl">
        Let me help you create a playlist!
      </div>
      <div className="flex flex-col mb-20 gap-5">
        <div>Type in the name of an artist:</div>
        <div className="flex items-center gap-20 mt-5 ">
          <InputField
            placeholderText="..."
            userInput={artistInput}
            setUserInput={setArtistInput}
            width={600}
            height={100}
          />
          <AppButton
            text="+"
            width={60}
            height={60}
            onClick={addArtistToList}
          />
        </div>
      </div>
      <ArtistsList
        listTitle="Chosen Artists:"
        artistsList={artistsList}
        onDelete={removeArtistFromList}
      />
      <div className="self-end mt-20">
        <AppButton
          text="Get the recommendations!"
          width={500}
          height={80}
          onClick={getRecommendations}
        />
      </div>
    </div>
  );
}

export default AddArtists;
