import type { TrackData } from "./recommendations";

export interface PlaylistCreate {
  playlistTitle: string;
  selectedTracks: TrackData[];
}
