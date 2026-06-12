from fastapi import Request

from app.exceptions.exceptions import NotAuthenticatedError


def get_auth_headers(request: Request) -> dict:
    access_token = request.session.get("access_token")
    if not access_token:
        raise NotAuthenticatedError()
    return {"Authorization": f"Bearer {access_token}"}
