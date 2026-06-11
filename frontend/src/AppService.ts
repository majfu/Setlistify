import axios from "axios";
import type { RecommendationsResponse } from "./models/recommendations";
import type { PlaylistCreate, SelectedTrack } from "./models/playlists";

const BACKEND_URL = "http://127.0.0.1:8000";

export const getTrackRecommendations = async (
  artistsList: string[],
): Promise<RecommendationsResponse> => {
  const response = await axios.post<RecommendationsResponse>(
    `${BACKEND_URL}/recommendations/`,
    { artistsList },
    { withCredentials: true },
  );
  return response.data;
};

export const createPlaylist = async (
  playlistTitle: string,
  selectedTracks: SelectedTrack[],
): Promise<void> => {
  const body: PlaylistCreate = { playlistTitle, selectedTracks };
  await axios.post(`${BACKEND_URL}/playlists/`, body, {
    withCredentials: true,
  });
};
