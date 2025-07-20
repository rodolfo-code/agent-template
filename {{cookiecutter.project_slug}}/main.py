from fastapi import FastAPI
from app.presentation.{{cookiecutter.agent_name}}_router import router as {{cookiecutter.agent_name}}_router


app = FastAPI(title="{{ cookiecutter.project_name }}")

app.include_router({{cookiecutter.agent_name}}_router, prefix="/api")


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 