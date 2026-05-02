import { useState } from "react";
import type {
  ArtistRecommendation,
  RecommendationsResponse,
} from "../models/recommendations";

const RECOMMENDATIONS_STORAGE_KEY = "setlistify:recommendations";

function AddSongs() {
  const [recommendationsObject] = useState<ArtistRecommendation[]>(() => {
    const stored = sessionStorage.getItem(RECOMMENDATIONS_STORAGE_KEY);
    if (!stored) return [];
    const parsed: RecommendationsResponse = JSON.parse(stored);
    return parsed.recommendations ?? [];
  });

  return <>{JSON.stringify(recommendationsObject)}</>;
}
export default AddSongs;
