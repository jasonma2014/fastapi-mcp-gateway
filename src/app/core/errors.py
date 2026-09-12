from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.services.projects import ProjectNotFoundError


def _field_path(location: tuple[object, ...]) -> str:
    parts = [
        str(part) for part in location
        if part not in {"body", "query", "path", "header"}
    ]
    if not parts:
        return "request"
    return ".".join(parts)


async def validation_exception_handler(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    issues = []
    for error in exc.errors():
        location = tuple(error.get("loc", ()))
        issues.append(
            {
                "field": _field_path(location),
                "message": error.get("msg", "Invalid value"),
                "type": error.get("type", "validation_error"),
            }
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "The request contains invalid input",
                "issues": issues,
            }
        },
    )


async def project_not_found_handler(
    _request: Request,
    exc: ProjectNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": {
                "code": "PROJECT_NOT_FOUND",
                "message": str(exc),
            }
        },
    )


