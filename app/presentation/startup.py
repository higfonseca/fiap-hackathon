from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.infrastructure.container import ApplicationContainer
from app.infrastructure.settings import settings
from app.presentation.routers import authentication_router, health_router, record_router


def get_app() -> FastAPI:
    container = ApplicationContainer()
    routers = [health_router, record_router, authentication_router]
    tags_metadata = [metadata for router in routers if hasattr(router, "metadata") for metadata in router.metadata]

    app = FastAPI(
        title="FIAP Hackathon",
        description="Manage employee's clock in/out",
        version="0.1.0",
        openapi_tags=tags_metadata,
        openapi_url="/docs/openapi.json",
        docs_url="/docs",
    )

    for router in routers:
        container.wire([router])
        app.include_router(router.router)

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.trusted_hosts)
    return app
