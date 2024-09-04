"""Main API module to define the FastAPI app and its configuration"""

# Standard library imports
from contextlib import asynccontextmanager
from typing import Any, Dict

import uvicorn

# Third-party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from soli import SOLI

# Project imports
import soli_api.routes.info
import soli_api.routes.root
import soli_api.routes.search
import soli_api.routes.taxonomy
from soli_api.api_config import load_config


@asynccontextmanager
async def lifespan_handler(app_instance: FastAPI):
    """Context manager to handle the lifespan events of the FastAPI app

    Args:
        app_instance (FastAPI): FastAPI app instance

    Yields:
        None
    """
    # Initialize the SOLI graph
    app_instance.state.config = load_config()
    app_instance.state.soli = initialize_soli(app_instance.state.config["soli"])

    yield


def initialize_soli(soli_config: Dict[str, Any]) -> SOLI:
    """Initialize SOLI instance based on configuration

    Args:
        soli_config (Dict[str, Any]): SOLI configuration dictionary

    Returns:
        SOLI: Initialized SOLI instance
    """
    return SOLI(
        source_type=soli_config["source"],
        github_repo_owner=soli_config["repository"].split("/")[0],
        github_repo_name=soli_config["repository"].split("/")[1],
        github_repo_branch=soli_config["branch"],
        use_cache=True,
    )


def get_app() -> FastAPI:
    """Factory to create FastAPI app with proper configuration

    Returns:
        FastAPI: FastAPI app with configuration
    """
    # Load the configuration
    config = load_config()
    api_config = config["api"]
    app_instance = FastAPI(
        title=api_config["title"],
        description=api_config["description"],
        version=api_config["version"],
        openapi_url="/openapi.json",
        openapi_tags=[],
        docs_url="/docs",
        terms_of_service=api_config["terms_of_service"],
        contact=api_config["contact"],
        lifespan=lifespan_handler,
    )

    # Enable CORS as this is a public API by default.
    app_instance.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=api_config.get("cors_origins", ["*"]),
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Attach the routes
    app_instance.include_router(soli_api.routes.info.router)
    app_instance.include_router(soli_api.routes.root.router)
    app_instance.include_router(soli_api.routes.search.router)
    app_instance.include_router(soli_api.routes.taxonomy.router)

    return app_instance


# get instance from factory
app = get_app()

if __name__ == "__main__":
    # Load the configuration and run the dev server
    config = load_config()
    bind_host = config.get("api", {}).get("bind_ip", "0.0.0.0")
    bind_port = config.get("api", {}).get("bind_port", 8000)
    uvicorn.run(app, host=bind_host, port=bind_port)

    # Alternatively, run the app on CLI from the uvicorn command:
    # uvicorn soli_api.api:app --reload
