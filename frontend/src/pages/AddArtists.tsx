import { useState } from "react";
import InputField from "../components/InputField";

function AddArtists() {
  const [artistInput, setArtistInput] = useState<string>("");

  return (
    <div className="flex flex-col">
      <div className="self-center text-5xl mb-20 bg-sky-100 p-10 rounded-3xl">
        Let me help you create a playlist!
      </div>
      <div className="mb-10">Type in the name of an artist:</div>
      <InputField
        placeholderText="Artist..."
        userInput={artistInput}
        setUserInput={setArtistInput}
        width={600}
        height={100}
      />
    </div>
  );
}

export default AddArtists;
