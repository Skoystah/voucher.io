import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import Config
from web.handlers.user import create_user_router
from web.handlers.voucher import create_voucher_router

# Origins allowed to call the API cross-origin. The deployed frontend is served
# same-origin behind the /api proxy and needs no CORS at all; this list only
# matters for local development against a separately served frontend.
DEFAULT_ORIGINS = [
    "https://voucher.abisko.fyi",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]


def _allowed_origins() -> list[str]:
    raw = os.getenv("ALLOW_ORIGINS")
    if not raw:
        return DEFAULT_ORIGINS
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


def create_app(config: Config) -> FastAPI:
    app = FastAPI()

    app.include_router(create_voucher_router(config))
    app.include_router(create_user_router(config))

    # Cookies are sent with these requests, so the origin list must be explicit
    # — a wildcard here would either be rejected by browsers or force reflective
    # CORS, which is unsafe.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_allowed_origins(),
        allow_methods=["GET", "PUT", "POST", "DELETE"],
        allow_headers=["Content-type"],
        allow_credentials=True,
    )

    return app
