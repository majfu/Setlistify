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

export interface Playlist {
  id: number;
  title: string;
  createdAt: string;
}

export interface PlaylistsPage {
  playlists: Playlist[];
  total: number;
}
