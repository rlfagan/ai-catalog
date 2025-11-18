"""
API v1 Router
Aggregates all API endpoints
"""

from fastapi import APIRouter

router = APIRouter()

# Placeholder endpoints - will be expanded
@router.get("/search", tags=["Search"])
async def search_models(
    q: str | None = None,
    pipeline_tag: str | None = None,
    page: int = 1,
    per_page: int = 20
):
    """
    Search for models with filters

    This is a placeholder that will be implemented after database setup
    """
    return {
        "total": 0,
        "page": page,
        "per_page": per_page,
        "total_pages": 0,
        "results": [],
        "message": "Database not initialized yet. Run init_db.py script first."
    }

@router.get("/models/{model_id:path}", tags=["Models"])
async def get_model(model_id: str):
    """
    Get details for a specific model

    This is a placeholder that will be implemented after database setup
    """
    return {
        "message": "Database not initialized yet. Run init_db.py script first.",
        "model_id": model_id
    }

@router.get("/trending", tags=["Trending"])
async def get_trending(limit: int = 20):
    """
    Get trending models

    This is a placeholder that will be implemented after database setup
    """
    return {
        "timeframe": "week",
        "models": [],
        "message": "Database not initialized yet. Run init_db.py script first."
    }

@router.get("/stats", tags=["Statistics"])
async def get_stats():
    """
    Get catalog statistics

    This is a placeholder that will be implemented after database setup
    """
    return {
        "total_models": 0,
        "message": "Database not initialized yet. Run init_db.py script first."
    }
