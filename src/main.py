from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from api import router as api_router
from web.view.index import router as index_router
from core.config import settings
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
)
main_app.mount("/static", StaticFiles(directory="static"), name="static")

main_app.include_router(
    api_router,
)

main_app.include_router(
    index_router,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        log_level="debug",
        reload=True,
        host=settings.run.host,
        port=settings.run.port,
    )
