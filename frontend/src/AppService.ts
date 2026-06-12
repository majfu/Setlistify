import axios from "axios";
import type { RecommendationsResponse } from "./models/recommendations";
import type {
  PlaylistCreate,
  PlaylistsPage,
  SelectedTrack,
} from "./models/playlists";

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

export const getPlaylists = async (
  page: number,
  pageSize: number,
): Promise<PlaylistsPage> => {
  const response = await axios.get<PlaylistsPage>(`${BACKEND_URL}/playlists/`, {
    params: { page, page_size: pageSize },
    withCredentials: true,
  });
  return response.data;
};

export const deletePlaylist = async (playlistId: number): Promise<void> => {
  await axios.delete(`${BACKEND_URL}/playlists/${playlistId}`, {
    withCredentials: true,
  });
};

export const addSongsToPlaylist = async (
  playlistId: number,
  selectedTracks: SelectedTrack[],
): Promise<void> => {
  await axios.post(
    `${BACKEND_URL}/playlists/${playlistId}/tracks`,
    { selectedTracks },
    { withCredentials: true },
  );
};
