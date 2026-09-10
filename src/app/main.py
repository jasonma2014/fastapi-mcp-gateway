import uvicorn
from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="0.1.0",
    )
    app.include_router(
        health_router,
        prefix=settings.api_prefix,
        tags=["health"],
    )
    return app
    
app = create_app()



@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def main() -> None:
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
