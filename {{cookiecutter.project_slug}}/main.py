"""
{{ cookiecutter.project_name }}
"""

from fastapi import FastAPI

app = FastAPI(title="{{ cookiecutter.project_name }}")

# TODO: Importe e configure seu router aqui
# from app.presentation.domain_router import router
# app.include_router(router, prefix="/domain")


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 