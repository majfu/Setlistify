import { useState } from "react";
import InputField from "../components/InputField";
import ArtistsList from "../components/ArtistsList";
import AppButton from "../components/AppButton";

function AddArtists() {
  const [artistInput, setArtistInput] = useState<string>("");
  const [artistsList, setArtistsList] = useState<string[]>([]);

  const addArtistToList = () => {
    if (!artistInput.length) return;
    setArtistsList([...artistsList, artistInput]);
    setArtistInput("");
  };

  const removeArtistFromList = (artist: string) => {
    setArtistsList(artistsList.filter((a) => a !== artist));
  };

  return (
    <div className="flex flex-col">
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
    </div>
  );
}

export default AddArtists;
