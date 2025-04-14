from fastapi import Request
from fastapi.responses import RedirectResponse

from routes.auth import AuthError


def unauthorized_handler(request: Request, error: AuthError):
    return RedirectResponse("/auth")
