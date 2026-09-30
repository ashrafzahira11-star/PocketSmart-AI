from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import Base, engine

from .routers import (
    auth_routes,
    page_routes,
    planner_routes,
)


BASE_DIR = Path(
    __file__
).resolve().parent


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(

    title=settings.app_name,

    version="1.0.0",

    description=
        "Budget-aware GenAI recommendation assistant."
)


app.mount(

    "/static",

    StaticFiles(
        directory=str(
            BASE_DIR / "static"
        )
    ),

    name="static"
)


app.include_router(
    page_routes.router
)

app.include_router(
    auth_routes.router
)

app.include_router(
    planner_routes.router
)


@app.get("/health")
def health():

    return {

        "status": "ok",

        "app":
            settings.app_name,

        "gemini_configured":
            bool(
                settings.gemini_api_key
            )
            and settings.use_gemini,

        "model":
            settings.gemini_model,
    }


@app.get("/docs-note")
def docs_note():

    return {

        "message":
            "Open /docs for the interactive FastAPI API documentation."
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "app.main:app",

        host="127.0.0.1",

        port=8000,

        reload=True
    )