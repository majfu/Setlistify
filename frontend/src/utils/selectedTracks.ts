import type { ArtistRecommendation } from "../models/recommendations";
import type { SelectedTrack } from "../models/playlists";

export function toSelectedTracks(
  recommendations: ArtistRecommendation[],
): SelectedTrack[] {
  return recommendations.flatMap((rec) =>
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
