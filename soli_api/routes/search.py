"""
Search routes.
"""

# imports

# packages
from fastapi import APIRouter, Request
from soli import SOLI

# project
from soli_api.models.owl import OWLClassList, OWLSearchResults

# API router
router = APIRouter(prefix="/search", tags=["search"])


@router.get("/prefix", tags=["search"], response_model=OWLClassList)
async def search_prefix(request: Request, query: str) -> OWLClassList:
    """
    Get class information for labels that start with the query string.

    Args:
        request (Request): FastAPI request object
        query (str): Query string

    Returns:
        OWLClassList: Pydantic model with list of classes
    """
    # make sure that the query string is at least 2 characters long to avoid attacks
    if len(query) < 2:
        return OWLClassList(classes=[])

    soli: SOLI = request.app.state.soli
    return OWLClassList(classes=soli.search_by_prefix(query))


@router.get("/label", tags=["search"], response_model=OWLSearchResults)
async def search_label(request: Request, query: str) -> OWLSearchResults:
    """
    Get class information using the soli-python search_by_label method.

    Args:
        request (Request): FastAPI request object
        query (str): Query string

    Returns:
        OWLClassList: Pydantic model with list of classes
    """
    soli: SOLI = request.app.state.soli
    return OWLSearchResults(results=soli.search_by_label(query))


@router.get("/definition", tags=["search"], response_model=OWLSearchResults)
async def search_definition(request: Request, query: str) -> OWLSearchResults:
    """
    Get class information using the soli-python search_by_definition method.

    Args:
        request (Request): FastAPI request object
        query (str): Query string

    Returns:
        OWLClassList: Pydantic model with list of classes
    """
    soli: SOLI = request.app.state.soli
    return OWLSearchResults(results=soli.search_by_definition(query))
