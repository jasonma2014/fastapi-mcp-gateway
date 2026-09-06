import uvicorn
from fastapi import FastAPI

app = FastAPI(title="FastAPI MCP Gateway")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def main() -> None:
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
