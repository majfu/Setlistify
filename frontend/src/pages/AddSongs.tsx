import { useEffect, useState } from "react";
import type {
  ArtistRecommendation,
  RecommendationsResponse,
} from "../models/recommendations";
import SongsField from "../components/SongsField";

const RECOMMENDATIONS_STORAGE_KEY = "setlistify:recommendations";

function AddSongs() {
  const [recommendations, setRecommendations] = useState<
    ArtistRecommendation[]
  >(() => {
    const stored = sessionStorage.getItem(RECOMMENDATIONS_STORAGE_KEY);
    if (!stored) return [];
    const parsed: RecommendationsResponse = JSON.parse(stored);
    return parsed.recommendations ?? [];
  });
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (recommendations.length === 0) return;
    sessionStorage.setItem(
      RECOMMENDATIONS_STORAGE_KEY,
      JSON.stringify({ recommendations }),
    );
  }, [recommendations]);

  if (recommendations.length === 0) return null;

  const handlePrev = () => {
    setCurrentIndex(
      (i) => (i - 1 + recommendations.length) % recommendations.length,
    );
  };

  const handleNext = () => {
    setCurrentIndex((i) => (i + 1) % recommendations.length);
  };

  const handleToggleTrack = (trackName: string) => {
    setRecommendations((prev) =>
      prev.map((rec, idx) => {
        if (idx !== currentIndex) return rec;
        const track = rec.tracks[trackName];
        return {
          ...rec,
          tracks: {
            ...rec.tracks,
            [trackName]: { ...track, isSelected: !track.isSelected },
          },
        };
      }),
    );
  };

  const handleSelectAll = () => {
    setRecommendations((prev) =>
      prev.map((rec, idx) => {
        if (idx !== currentIndex) return rec;
        const updatedTracks = Object.fromEntries(
          Object.entries(rec.tracks).map(([name, track]) => [
            name,
            { ...track, isSelected: true },
          ]),
        );
        return { ...rec, tracks: updatedTracks };
      }),
    );
  };

  return (
    <div className="flex flex-col items-center">
      <div className="text-5xl mb-40 bg-sky-100 p-10 rounded-3xl">
        Add some songs!
      </div>
      <div>
        <SongsField
          artistRecommendation={recommendations[currentIndex]}
          currentIndex={currentIndex}
          totalCount={recommendations.length}
          onPrev={handlePrev}
          onNext={handleNext}
          onToggleTrack={handleToggleTrack}
          onSelectAll={handleSelectAll}
        />
      </div>
    </div>
  );
}
export default AddSongs;
