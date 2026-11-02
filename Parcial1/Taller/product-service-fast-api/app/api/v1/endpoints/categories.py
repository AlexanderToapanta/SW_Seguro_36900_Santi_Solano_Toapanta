from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.crud.category import (
    create_category,
    delete_category,
    get_categories,
    get_category,
    update_category,
)

from app.schemas.auth import AuthenticatedUser

from app.schemas.category import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
)

from app.security.dependencies import (
    require_roles,
)

from app.security.roles import (
    ADMIN_ONLY,
    READ_ROLES,
)

# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


# ============================================================
# POST /categories
#
# Crear una nueva categoría.
#
# Seguridad:
# SOLO ADMIN
# ============================================================


@router.post(
    "/",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear categoría",
    description=("Crea una nueva categoría. " "Requiere rol ADMIN."),
)
def create_category_endpoint(
    payload: CategoryCreate,
    current_user: AuthenticatedUser = Depends(require_roles(*ADMIN_ONLY)),
    db: Session = Depends(get_db),
):
    try:

        category = create_category(
            db,
            payload,
        )

        return category

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=("Ya existe una categoría " "con ese código"),
        )


# ============================================================
# GET /categories
#
# Listar categorías.
#
# Seguridad:
# ADMIN
# OPERADOR
# CLIENTE
# ============================================================


@router.get(
    "/",
    response_model=list[CategoryRead],
    status_code=status.HTTP_200_OK,
    summary="Listar categorías",
    description=("Obtiene las categorías " "registradas en el sistema."),
)
def list_categories_endpoint(
    page: int = Query(
        default=1,
        ge=1,
        description="Número de página",
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description=("Cantidad máxima de registros " "por página"),
    ),
    current_user: AuthenticatedUser = Depends(require_roles(*READ_ROLES)),
    db: Session = Depends(get_db),
):

    skip = (page - 1) * limit

    return get_categories(
        db,
        skip=skip,
        limit=limit,
    )


# ============================================================
# GET /categories/{category_id}
#
# Consultar una categoría por UUID.
#
# Seguridad:
# ADMIN
# OPERADOR
# CLIENTE
# ============================================================


@router.get(
    "/{category_id}",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
    summary="Consultar categoría",
    description=("Obtiene una categoría " "mediante su UUID."),
)
def get_category_endpoint(
    category_id: UUID,
    current_user: AuthenticatedUser = Depends(require_roles(*READ_ROLES)),
    db: Session = Depends(get_db),
):

    category = get_category(
        db,
        category_id,
    )

    if category is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("Categoría no encontrada"),
        )

    return category


# ============================================================
# PATCH /categories/{category_id}
#
# Actualizar parcialmente una categoría.
#
# Seguridad:
# SOLO ADMIN
# ============================================================


@router.patch(
    "/{category_id}",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
    summary="Actualizar categoría",
    description=("Actualiza parcialmente " "una categoría. " "Requiere rol ADMIN."),
)
def update_category_endpoint(
    category_id: UUID,
    payload: CategoryUpdate,
    current_user: AuthenticatedUser = Depends(require_roles(*ADMIN_ONLY)),
    db: Session = Depends(get_db),
):

    category = get_category(
        db,
        category_id,
    )

    if category is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("Categoría no encontrada"),
        )

    try:

        return update_category(
            db,
            category,
            payload,
        )

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No fue posible actualizar "
                "la categoría. "
                "Verifique que el código "
                "no esté registrado."
            ),
        )


# ============================================================
# DELETE /categories/{category_id}
#
# Eliminación lógica de una categoría.
#
# Seguridad:
# SOLO ADMIN
# ============================================================


@router.delete(
    "/{category_id}",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
    summary="Eliminar categoría",
    description=(
        "Realiza la eliminación lógica " "de una categoría. " "Requiere rol ADMIN."
    ),
)
def delete_category_endpoint(
    category_id: UUID,
    current_user: AuthenticatedUser = Depends(require_roles(*ADMIN_ONLY)),
    db: Session = Depends(get_db),
):

    category = get_category(
        db,
        category_id,
    )

    if category is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("Categoría no encontrada"),
        )

    return delete_category(
        db,
        category,
    )
