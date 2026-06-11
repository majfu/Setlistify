export interface SelectedTrack {
  title: string;
  artistName: string;
  uri: string;
  isAIRecommended: boolean;
  popularity: number | null;
  isSelected: boolean;
}

export interface PlaylistCreate {
  playlistTitle: string;
  selectedTracks: SelectedTrack[];
}
