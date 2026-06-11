import { useEffect, useState } from "react";
import AppButton from "../components/AppButton";
import PlaylistList from "../components/PlaylistList";
import { deletePlaylist, getPlaylists } from "../AppService";
import type { Playlist } from "../models/playlists";

const PAGE_SIZE = 5;

function Browse() {
  const [page, setPage] = useState(1);
  const [playlists, setPlaylists] = useState<Playlist[]>([]);
  const [total, setTotal] = useState(0);

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  const loadPlaylists = async () => {
    const data = await getPlaylists(page, PAGE_SIZE);
    setPlaylists(data.playlists);
    setTotal(data.total);
  };

  useEffect(() => {
    loadPlaylists();
  }, [page]);

  const handleDelete = async (id: number) => {
    await deletePlaylist(id);
    if (playlists.length === 1 && page > 1) {
      setPage((p) => p - 1);
    } else {
      loadPlaylists();
    }
  };

  const handlePrev = () => setPage((p) => Math.max(1, p - 1));
  const handleNext = () => setPage((p) => Math.min(totalPages, p + 1));

  return (
    <div className="flex flex-col items-center">
      <div className="text-5xl mb-40 bg-sky-100 p-10 rounded-3xl">
        Your playlists
      </div>

      <div className="flex flex-col bg-white p-20 rounded-3xl w-1150px">
        <PlaylistList playlists={playlists} onDelete={handleDelete} />

        <div className="flex justify-between items-center mt-30">
          <AppButton text="<" width={80} height={80} onClick={handlePrev} />
          <div className="text-3xl bg-sky-100 p-6 rounded-3xl text-center">
            {page} out of {totalPages}
          </div>
          <AppButton text=">" width={80} height={80} onClick={handleNext} />
        </div>
      </div>
    </div>
  );
}
export default Browse;
