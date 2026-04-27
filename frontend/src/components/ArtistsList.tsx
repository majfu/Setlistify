import AppButton from "./AppButton";

interface artistsListProps {
  listTitle: string;
  artistsList: string[];
  onDelete: (artist: string) => void;
}

function ArtistsList({ listTitle, artistsList, onDelete }: artistsListProps) {
  return (
    <div>
      <div className="mb-10">{listTitle}</div>
      <div className="bg-white border-6 border-sky-950 rounded-3xl p-3">
        {artistsList.map((artist) => (
          <div className="hover:bg-sky-50 p-5 rounded-xl" key={artist}>
            <div className="flex items-center justify-between py-4">
              <div>{artist}</div>
              <AppButton
                text="-"
                width={40}
                height={40}
                onClick={() => onDelete(artist)}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ArtistsList;
