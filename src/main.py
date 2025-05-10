import uvicorn
from fastapi import FastAPI

from core.config import settings

from api import router as api_router
app = FastAPI(
    title="API",
    description="API",
    version="1.0.0",
    )
app.include_router(
    api_router,
    prefix=settings.api.prefix,
)



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        log_level="debug",
        host=settings.run.host,
        port=settings.run.port,
    )