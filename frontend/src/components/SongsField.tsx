import type { ArtistRecommendation } from "../models/recommendations";
import AppButton from "./AppButton";

interface SongsFieldProps {
  artistRecommendation: ArtistRecommendation;
  currentIndex: number;
  totalCount: number;
  onPrev: () => void;
  onNext: () => void;
  onToggleTrack: (trackName: string) => void;
  onSelectAll: () => void;
}

function SongsField({
  artistRecommendation,
  currentIndex,
  totalCount,
  onPrev,
  onNext,
  onToggleTrack,
  onSelectAll,
}: SongsFieldProps) {
  const tracks = Object.entries(artistRecommendation.tracks);
  const aiRecommendedTracks = tracks.filter(
    ([, track]) => track.isAIRecommended,
  );
  const otherTracks = tracks.filter(([, track]) => !track.isAIRecommended);

  const renderTrack = ([trackName, trackData]: (typeof tracks)[number]) => (
    <button
      key={trackName}
      type="button"
      onClick={() => onToggleTrack(trackName)}
      className={`p-5 rounded-3xl text-center hover:cursor-pointer ${
        trackData.isSelected ? "bg-sky-900 text-white" : "bg-sky-50"
      }`}
    >
      {trackName}
    </button>
  );

  return (
    <div className="flex flex-col bg-white p-20 rounded-3xl">
      <div className="flex justify-between items-center mb-30">
        <AppButton text="<" width={80} height={80} onClick={onPrev} />
        <div className="flex items-center gap-15">
          <div className="text-4xl bg-sky-100 p-10 rounded-3xl text-center">
            {artistRecommendation.artistName}
          </div>
          <div className="text-3xl bg-sky-100 p-6 rounded-3xl text-center">
            {currentIndex + 1} out of {totalCount}
          </div>
        </div>
        <AppButton text=">" width={80} height={80} onClick={onNext} />
      </div>

      <div className="flex justify-center mb-30">
        <AppButton
          text="Select all"
          width={300}
          height={80}
          onClick={onSelectAll}
        />
      </div>

      <div className="flex flex-col gap-30">
        <div>
          <div className="text-3xl bg-sky-100 p-6 rounded-3xl text-center mb-15">
            AI Recommended
          </div>
          <div className="flex max-w-600 flex-wrap gap-20">
            {aiRecommendedTracks.map(renderTrack)}
          </div>
        </div>
        <div>
          <div className="text-3xl bg-sky-100 p-6 rounded-3xl text-center mb-15">
            Other
          </div>
          <div className="flex max-w-600 flex-wrap gap-20">
            {otherTracks.map(renderTrack)}
          </div>
        </div>
      </div>
    </div>
  );
}

export default SongsField;
