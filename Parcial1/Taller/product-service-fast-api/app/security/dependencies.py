from collections.abc import Callable

from fastapi import (
    Depends,
    HTTPException,
    Request,
    Security,
    status,
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.clients.user_service import (
    validate_user_token,
)

from app.schemas.auth import (
    AuthenticatedUser,
)


# ============================================
# Bearer JWT
# ============================================

bearer_scheme = HTTPBearer(
    scheme_name="BearerAuth",
    bearerFormat="JWT",
    description=(
        "JWT generado por User Service"
    ),
    auto_error=False,
)


# ============================================
# Usuario autenticado
# ============================================

async def get_current_user(
    request: Request,

    credentials:
        HTTPAuthorizationCredentials
        | None = Security(
            bearer_scheme
        ),
) -> AuthenticatedUser:

    if credentials is None:

        raise HTTPException(
            status_code=
                status.HTTP_401_UNAUTHORIZED,
            detail=(
                "Se requiere un token de acceso"
            ),
            headers={
                "WWW-Authenticate":
                    "Bearer",
            },
        )

    if (
        credentials.scheme.lower()
        != "bearer"
    ):

        raise HTTPException(
            status_code=
                status.HTTP_401_UNAUTHORIZED,
            detail=(
                "Esquema de autenticación "
                "inválido"
            ),
            headers={
                "WWW-Authenticate":
                    "Bearer",
            },
        )

    client = (
        request
        .app
        .state
        .user_service_client
    )

    request_id = (
        request.headers.get(
            "X-Request-Id"
        )
    )

    return await validate_user_token(
        client=client,
        token=credentials.credentials,
        request_id=request_id,
    )


# ============================================
# Autorización RBAC
# ============================================

def require_roles(
    *allowed_roles: str,
) -> Callable:

    normalized_allowed = {
        role.upper()
        for role in allowed_roles
    }

    async def role_dependency(
        current_user:
            AuthenticatedUser = Depends(
                get_current_user
            ),
    ) -> AuthenticatedUser:

        user_roles = {
            role.upper()
            for role
            in current_user.roles
        }

        authorized = bool(
            user_roles
            & normalized_allowed
        )

        if not authorized:

            raise HTTPException(
                status_code=
                    status.HTTP_403_FORBIDDEN,
                detail=(
                    "No posee los roles "
                    "requeridos para realizar "
                    "esta operación"
                ),
            )

        return current_user

    return role_dependency