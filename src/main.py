from contextlib import asynccontextmanager

import uvicorn
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.routing import Router

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


app = FastAPI(
    lifespan=lifespan,

)

app.include_router(
    api_router,
)

app.include_router(
    index_router,
)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        log_level="debug",
        reload=True,
        host=settings.run.host,
        port=settings.run.port,
    )
