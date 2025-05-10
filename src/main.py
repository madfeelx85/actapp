import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="API",
    description="API",
    version="1.0.0",
    )

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, log_level="debug", host="0.0.0.0", port=8000)