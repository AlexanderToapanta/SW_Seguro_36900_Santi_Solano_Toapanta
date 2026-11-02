from contextlib import (
    asynccontextmanager,
)

import httpx

from fastapi import FastAPI

from app.api.v1.api import (
    api_router,
)

from app.core.config import (
    settings,
)

from app.db.init_db import (
    init_db,
)

from app.db.seed import (
    seed_database,
)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):

    print("🚀 Iniciando Product Service...")

    # ========================================
    # Base de datos
    # ========================================

    init_db()

    if settings.ENABLE_SEED:

        seed_database()

    # ========================================
    # Cliente HTTP compartido para
    # comunicación con User Service
    # ========================================

    timeout = httpx.Timeout(
        settings.USER_SERVICE_TIMEOUT_SECONDS,
        connect=2.0,
    )

    app.state.user_service_client = httpx.AsyncClient(
        base_url=(settings.USER_SERVICE_URL.rstrip("/")),
        timeout=timeout,
        follow_redirects=False,
    )

    print("✅ Product Service inicializado")

    try:

        yield

    finally:

        await app.state.user_service_client.aclose()

        print("🛑 Product Service detenido")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=("Microservicio de gestión " "de productos y categorías"),
    lifespan=lifespan,
)


# ============================================
# Health público
# ============================================


@app.get(
    "/health",
    tags=["Health"],
)
def health():

    return {
        "status": "ok",
        "service": settings.APP_NAME,
    }


# ============================================
# API
# ============================================

app.include_router(
    api_router,
    prefix=settings.API_V1_STR,
)
