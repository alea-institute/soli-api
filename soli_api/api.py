"""Main API module to define the FastAPI app and its configuration"""

# imports
import logging
import os
from contextlib import asynccontextmanager
from typing import Any, Dict

# packages
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from soli import SOLI
from alea_llm_client import OpenAIModel, AnthropicModel, VLLMModel

# project imports
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

    # get log level
    log_level = {
        "info": logging.INFO,
        "debug": logging.DEBUG,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }.get(
        app_instance.state.config.get("log_level", "info").lower().strip(), logging.INFO
    )

    # set up the logger at api.log
    app_instance.state.logger = logging.getLogger("soli_api")
    app_instance.state.logger.setLevel(log_level)
    log_handler = logging.FileHandler("api.log")
    log_handler.setLevel(log_level)
    log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    log_handler.setFormatter(log_formatter)
    app_instance.state.logger.addHandler(log_handler)

    # initialize the SOLI instance
    app_instance.state.soli = initialize_soli(
        app_instance.state.config["soli"],
        app_instance.state.config["llm"],
    )

    # log it
    app_instance.state.logger.info(
        "SOLI instance initialized with llm %s", app_instance.state.soli.llm.model
    )

    yield

    # log shutdown
    app_instance.state.logger.info("Shutting down API")


def initialize_soli(soli_config: Dict[str, Any], llm_config: Dict[str, Any]) -> SOLI:
    """Initialize SOLI instance based on configuration

    Args:
        soli_config (Dict[str, Any]): SOLI configuration dictionary
        llm_config (Dict[str, Any]): LLM configuration dictionary

    Returns:
        SOLI: Initialized SOLI instance
    """
    # initialize an llm
    llm_engine = llm_config.get("type", "openai").lower().strip()
    llm_model = llm_config.get("model", "gpt-4o").lower().strip()
    llm_endpoint = llm_config.get("endpoint", None)
    llm_api_key = llm_config.get("api_key", os.getenv("OPENAI_API_KEY"))

    # create the llm
    if llm_engine in ("openai",):
        llm_args = {
            "model": llm_model,
            "api_key": llm_api_key,
        }
        if llm_endpoint is not None:
            llm_args["endpoint"] = llm_endpoint
        llm = OpenAIModel(**llm_args)
    elif llm_engine in ("anthropic",):
        llm_args = {
            "model": llm_model,
            "api_key": llm_api_key,
        }
        if llm_endpoint is not None:
            llm_args["endpoint"] = llm_endpoint
        llm = AnthropicModel(**llm_args)
    elif llm_engine in ("vllm",):
        llm_args = {
            "model": llm_model,
            "api_key": llm_api_key,
        }
        if llm_endpoint is not None:
            llm_args["endpoint"] = llm_endpoint
        llm = VLLMModel(**llm_args)
    else:
        llm = None

    return SOLI(
        source_type=soli_config["source"],
        github_repo_owner=soli_config["repository"].split("/")[0],
        github_repo_name=soli_config["repository"].split("/")[1],
        github_repo_branch=soli_config["branch"],
        use_cache=True,
        llm=llm,
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
