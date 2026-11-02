import re
import httpx

from fastapi import (
    HTTPException,
    status,
)

from pydantic import ValidationError

from app.core.config import settings
from app.schemas.auth import AuthenticatedUser


async def validate_user_token(
    client: httpx.AsyncClient,
    token: str,
    request_id: str | None = None,
) -> AuthenticatedUser:

    headers = {
        "Authorization": (f"Bearer {token}"),
    }

    if request_id and re.fullmatch(r"[A-Za-z0-9._-]{1,64}", request_id):
        headers["X-Request-Id"] = request_id[:64]

    try:

        response = await client.get(
            settings.USER_SERVICE_AUTH_ME_PATH,
            headers=headers,
        )

    except httpx.TimeoutException:

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=("El servicio de autenticación " "no respondió a tiempo"),
        )

    except httpx.RequestError:

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=("El servicio de autenticación " "no está disponible"),
        )

    # ========================================
    # JWT inválido, expirado, revocado,
    # usuario desactivado, logout, etc.
    # ========================================

    if response.status_code == 401:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=("Token inválido o sesión expirada"),
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    # ========================================
    # User Service explícitamente denegó acceso
    # ========================================

    if response.status_code == 403:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado",
        )

    # ========================================
    # Rate limit o falla del User Service
    # ========================================

    if response.status_code == 429 or response.status_code >= 500:

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=("Servicio de autenticación " "temporalmente no disponible"),
        )

    # ========================================
    # Respuesta inesperada
    # ========================================

    if response.status_code != 200:

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=("Respuesta inesperada del " "servicio de autenticación"),
        )

    try:

        return AuthenticatedUser.model_validate(response.json())

    except (
        ValueError,
        ValidationError,
    ):

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=("Respuesta inválida del " "servicio de autenticación"),
        )
