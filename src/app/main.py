from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.routes.health import router as health_router
from app.api.routes.projects import router as projects_router
from app.core.config import get_settings
from app.core.errors import project_not_found_handler, validation_exception_handler
from app.services.projects import ProjectNotFoundError


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="0.1.0",
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )

    app.add_exception_handler(
        ProjectNotFoundError,
        project_not_found_handler,
    )

    app.include_router(
        health_router,
        prefix=settings.api_prefix,
        tags=["health"],
    )

    app.include_router(
        projects_router,
        prefix=settings.api_prefix,
        tags=["projects"],
    )
    return app
    
app = create_app()


