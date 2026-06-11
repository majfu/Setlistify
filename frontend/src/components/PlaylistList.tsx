import AppButton from "./AppButton";
import type { Playlist } from "../models/playlists";

interface PlaylistListProps {
  playlists: Playlist[];
  onDelete: (id: number) => void;
}

function formatDate(isoDate: string): string {
  return new Date(isoDate).toLocaleDateString(undefined, {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

function PlaylistList({ playlists, onDelete }: PlaylistListProps) {
  if (playlists.length === 0) {
    return <div className="text-3xl text-center p-10">No playlists yet.</div>;
  }

  return (
    <div className="flex flex-col gap-20">
      {playlists.map((playlist) => (
        <div
          key={playlist.id}
          className="flex justify-between items-center bg-sky-50 p-10 rounded-3xl gap-20"
        >
          <div className="flex flex-col">
            <div className="text-3xl">{playlist.title}</div>
            <div className="text-xl text-sky-900">
              {formatDate(playlist.createdAt)}
            </div>
          </div>
          <div className="flex gap-10">
            <AppButton text="Add more songs" width={250} height={70} />
            <AppButton
              text="Delete"
              width={150}
              height={70}
              onClick={() => onDelete(playlist.id)}
            />
          </div>
        </div>
      ))}
    </div>
  );
}

export default PlaylistList;
