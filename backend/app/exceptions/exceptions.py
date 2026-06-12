class AppError(Exception):

    status_code = 500
    message = "Internal server error"

    def __init__(self, message: str | None = None):
        self.message = message or self.message
        super().__init__(self.message)


class NotAuthenticatedError(AppError):
    status_code = 401
    message = "Not authenticated with Spotify"


class PlaylistNotFoundError(AppError):
    status_code = 404
    message = "Playlist not found"


class ExternalServiceError(AppError):

    status_code = 502
    message = "An external service is currently unavailable"


class SpotifyError(ExternalServiceError):
    message = "Spotify request failed"


class SetlistFmError(ExternalServiceError):
    message = "setlist.fm request failed"


class RecommendationGenerationError(ExternalServiceError):
    message = "Failed to generate recommendations"
