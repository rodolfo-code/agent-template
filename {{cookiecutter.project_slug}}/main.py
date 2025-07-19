"""
{{ cookiecutter.project_name }} - FastAPI Application
{{ cookiecutter.description }}

Author: {{ cookiecutter.author_name }}
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.infrastructure.config.config import get_settings
from app.presentation import {{ cookiecutter.domain_name }}_router

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    settings = get_settings()
    
    # Startup
    logger.info(
        "Starting {{ cookiecutter.project_name }}",
        version="0.1.0",
        environment=settings.ENVIRONMENT,
        python_version=os.sys.version,
    )
    
    try:
        yield
    finally:
        # Shutdown
        logger.info("Shutting down {{ cookiecutter.project_name }}")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title="{{ cookiecutter.project_name }}",
        description="{{ cookiecutter.description }}",
        version="0.1.0",
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
        lifespan=lifespan,
    )

    # CORS middleware
    if settings.ENABLE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"] if settings.ENVIRONMENT == "development" else [],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include routers
    app.include_router(
        domain_router,
        prefix="/{{ cookiecutter.domain_name }}",
        tags=["{{ cookiecutter.domain_name }}"]
    )

    @app.get("/health", tags=["health"])
    async def health_check():
        """Health check endpoint."""
        return JSONResponse(
            content={
                "status": "healthy",
                "service": "{{ cookiecutter.project_name }}",
                "version": "0.1.0",
                "environment": settings.ENVIRONMENT,
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Global exception handler."""
        logger.error(
            "Unhandled exception",
            exc_info=exc,
            path=request.url.path,
            method=request.method,
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later.",
            }
        )

    return app


# Create the FastAPI app
app = create_app()

if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD and settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower(),
    ) 