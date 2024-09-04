"""
Info routes for the API.
"""

# imports

# packages
from fastapi import APIRouter, Request
from soli import SOLI

# project
from soli_api.models.health import HealthResponse, SOLIGraphInfo

# API router
router = APIRouter(prefix="/info", tags=["info"])


@router.get("/health", tags=["info"], response_model=HealthResponse)
async def health(request: Request) -> HealthResponse:
    """
    Health check endpoint to check the status of the API.

    Args:
        request (Request): FastAPI request object

    Returns:
        HealthResponse: Pydantic model with health status and SOLI graph information
    """
    soli: SOLI = request.app.state.soli
    return HealthResponse(
        status="healthy",
        soli_graph=SOLIGraphInfo(
            num_classes=len(soli),
            title=soli.title,
            description=soli.description,
            source_type=soli.source_type,
            http_url=soli.http_url,
            github_repo_owner=soli.github_repo_owner,
            github_repo_name=soli.github_repo_name,
            github_repo_branch=soli.github_repo_branch,
        ),
    )
