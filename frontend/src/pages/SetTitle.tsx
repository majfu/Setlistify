import { useState } from "react";
import InputField from "../components/InputField";
import AppButton from "../components/AppButton";

function SetTitle() {
  const [playlistTitle, setPlaylistTitle] = useState<string>("");

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
        <AppButton text="Create playlist!" width={600} height={70} />
      </div>
    </div>
  );
}
export default SetTitle;
