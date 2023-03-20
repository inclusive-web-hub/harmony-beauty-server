"""The main module"""

from fastapi import (
    FastAPI,
)
from fastapi.middleware.cors import (
    CORSMiddleware,
)
from functools import (
    lru_cache,
)
import logging
from typing import (
    Dict,
)
import uvicorn

from app.auth import (
    router as auth_router,
)
from app.config import (
    settings,
)
from app.users import (
    router as users_router,
)
from app.utils import (
    engine,
)

logger = logging.getLogger(__name__)


@lru_cache()
def get_app() -> FastAPI:
    """
    A method that creates, configures and returns a FastAPI app instance

    Return:
        FastAPI : a FastAPI app instance
    """
    app_settings = settings()
    if app_settings.DEBUG == "info":
        app = FastAPI(
            docs_url="/docs",
            redoc_url="/redocs",
            title="Harmony Beauty Server",
            description="The server side of Harmony Beauty.",
            version="1.0",
            openapi_url="/api/v1/openapi.json",
        )
    else:
        app = FastAPI(
            docs_url=None,
            redoc_url=None,
            title=None,
            description=None,
            version=None,
            openapi_url=None,
        )
    app = FastAPI(
        docs_url="/docs",
        redoc_url="/redocs",
        title="Harmony Beauty Server",
        description="The server side of Harmony Beauty.",
        version="0.1.0",
        openapi_url="/api/v1/openapi.json",
    )

    origins = [
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://localhost:3000",
    ]

    origins.extend(app_settings.cors_origins)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup() -> None:
        logger.info("Connecting to MongoDB...")
        await engine.init_engine_app(app)
        logger.info("Connected to MongoDB!")

    @app.on_event("shutdown")
    async def shutdown() -> None:
        logger.info("Closing connection with MongoDB...")
        # bug: TypeError: object NoneType can't be used in 'await' expression
        try:
            await app.state.client.close()
        except Exception as err:
            logger.error(repr(err))
        logger.info("Closed connection with MongoDB!")

    @app.get("/api")
    async def root() -> Dict[str, str]:
        return {"message": "Welcome to the Harmony Beauty Server."}

    app.include_router(auth_router.router, tags=["auth"])
    app.include_router(users_router.router, tags=["users"])

    return app


shop_app = get_app()


def serve() -> None:
    """
    A method that run a uvicorn command.
    """
    try:
        uvicorn.run(
            "app.main:shop_app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
        )
    except Exception as err:
        logger.error(repr(err))


if __name__ == "__main__":
    serve()
