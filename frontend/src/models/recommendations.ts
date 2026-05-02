export interface ArtistsList {
  artistsList: string[];
}

export interface TrackData {
  uri: string;
  isAIRecommended: boolean;
  popularity: number | null;
  isSelected: boolean;
}

export interface ArtistRecommendation {
  artistName: string;
  tracks: Record<string, TrackData>;
}

export interface RecommendationsResponse {
  recommendations: ArtistRecommendation[];
}
