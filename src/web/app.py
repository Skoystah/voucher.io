from config import Config
from web.handlers.voucher import create_voucher_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app(config: Config) -> FastAPI:
    app = FastAPI()

    app.include_router(create_voucher_router(config))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET", "PUT", "POST", "DELETE"],
        allow_headers=["Content-type"],
    )

    return app
