"""
Models for the health check endpoint.
"""

# imports
from typing import Optional

# packages
from pydantic import BaseModel


class SOLIGraphInfo(BaseModel):
    """
    Basic information about the SOLI graph, including the number of classes, title, and description.
    """

    # Number of classes in the SOLI graph
    num_classes: int

    # Title of the SOLI graph
    title: str

    # Description of the SOLI graph
    description: str

    # Source type of the SOLI graph; http or github
    source_type: str

    # Source URL of the SOLI graph if source type is http
    http_url: Optional[str]

    # GitHub owner of the SOLI graph if source type is github
    github_repo_owner: Optional[str]

    # GitHub repository name of the SOLI graph if source type is github
    github_repo_name: Optional[str]

    # GitHub repository branch of the SOLI graph if source type is github
    github_repo_branch: Optional[str]


class HealthResponse(BaseModel):
    """
    Response model for the health check endpoint, including the status of the service and information about the SOLI graph.
    """

    # Status of the service
    status: str

    # Information about the SOLI graph
    soli_graph: SOLIGraphInfo
