"""
FastAPI router for {{ cookiecutter.domain_name }}.
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/process")
async def process():
    """Process content."""
    pass 