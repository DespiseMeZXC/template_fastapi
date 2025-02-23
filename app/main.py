from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from core.config import settings
from api import router as api_router
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    yield
    #shutdow
    print("dispose engine")
    await db_helper.dispose()

main_app = FastAPI(lifespan=lifespan)
main_app.include_router(api_router, prefix=settings.api_prefix.prefix)

@main_app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:main_app", host=settings.run_config.host, port=settings.run_config.port, reload=True)
