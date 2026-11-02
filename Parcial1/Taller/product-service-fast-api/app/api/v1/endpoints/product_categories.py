from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.crud.category import (
    get_category,
)

from app.crud.product import (
    get_product,
)

from app.crud.product_category import (
    create_product_category,
    delete_product_category,
    get_categories_by_product,
    get_product_categories,
    get_product_category,
    get_products_by_category,
    update_product_category,
)

from app.schemas.auth import (
    AuthenticatedUser,
)

from app.schemas.product_category import (
    ProductCategoryCreate,
    ProductCategoryRead,
    ProductCategoryUpdate,
)

from app.security.dependencies import (
    require_roles,
)

from app.security.roles import (
    PRODUCT_CATEGORY_WRITE_ROLES,
    READ_ROLES,
)

# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/product-categories",
    tags=["Product Categories"],
)


# ============================================================
# POST /product-categories
#
# Asignar una categoría a un producto.
#
# Seguridad:
# ADMIN
# OPERADOR
# ============================================================


@router.post(
    "/",
    response_model=ProductCategoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Asignar categoría a producto",
    description=(
        "Crea una relación entre "
        "un producto y una categoría. "
        "Requiere rol ADMIN u OPERADOR."
    ),
)
def create_product_category_endpoint(
    payload: ProductCategoryCreate,
    current_user: AuthenticatedUser = Depends(
        require_roles(*PRODUCT_CATEGORY_WRITE_ROLES)
    ),
    db: Session = Depends(get_db),
):

    # --------------------------------------------------------
    # Verificar que el producto exista
    # --------------------------------------------------------

    product = get_product(
        db,
        payload.product_id,
    )

    if product is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("Producto no encontrado"),
        )

    # --------------------------------------------------------
    # Verificar que la categoría exista
    # --------------------------------------------------------

    category = get_category(
        db,
        payload.category_id,
    )

    if category is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("Categoría no encontrada"),
        )

    # --------------------------------------------------------
    # Crear relación
    # --------------------------------------------------------

    try:

        relation = create_product_category(
            db,
            payload,
        )

        return relation

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=("La relación entre el producto " "y la categoría ya existe"),
        )


# ============================================================
# GET /product-categories
#
# Listar todas las relaciones.
#
# Seguridad:
# ADMIN
# OPERADOR
# CLIENTE
# ============================================================


@router.get(
    "/",
    response_model=list[ProductCategoryRead],
    status_code=status.HTTP_200_OK,
    summary=("Listar relaciones producto-categoría"),
    description=("Obtiene las relaciones registradas " "entre productos y categorías."),
)
def list_product_categories_endpoint(
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

    return get_product_categories(
        db,
        skip=skip,
        limit=limit,
    )


# ============================================================
# IMPORTANTE:
#
# Las rutas específicas:
#
# /by-product/{product_id}
# /by-category/{category_id}
#
# deben declararse ANTES de:
#
# /{relation_id}
#
# para evitar ambigüedad en FastAPI.
# ============================================================


# ============================================================
# GET /product-categories/by-product/{product_id}
#
# Obtener categorías asignadas a un producto.
#
# Seguridad:
# ADMIN
# OPERADOR
# CLIENTE
# ============================================================


@router.get(
    "/by-product/{product_id}",
    response_model=list[ProductCategoryRead],
    status_code=status.HTTP_200_OK,
    summary=("Consultar categorías de un producto"),
    description=("Obtiene todas las categorías " "asignadas a un producto."),
)
def get_categories_of_product_endpoint(
    product_id: UUID,
    current_user: AuthenticatedUser = Depends(require_roles(*READ_ROLES)),
    db: Session = Depends(get_db),
):

    product = get_product(
        db,
        product_id,
    )

    if product is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("Producto no encontrado"),
        )

    return get_categories_by_product(
        db,
        product_id,
    )


# ============================================================
# GET /product-categories/by-category/{category_id}
#
# Obtener productos asociados a una categoría.
#
# Seguridad:
# ADMIN
# OPERADOR
# CLIENTE
# ============================================================


@router.get(
    "/by-category/{category_id}",
    response_model=list[ProductCategoryRead],
    status_code=status.HTTP_200_OK,
    summary=("Consultar productos de una categoría"),
    description=("Obtiene todos los productos " "asociados a una categoría."),
)
def get_products_of_category_endpoint(
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

    return get_products_by_category(
        db,
        category_id,
    )


# ============================================================
# GET /product-categories/{relation_id}
#
# Obtener una relación específica.
#
# Seguridad:
# ADMIN
# OPERADOR
# CLIENTE
# ============================================================


@router.get(
    "/{relation_id}",
    response_model=ProductCategoryRead,
    status_code=status.HTTP_200_OK,
    summary=("Consultar relación producto-categoría"),
    description=("Obtiene una relación específica " "mediante su UUID."),
)
def get_product_category_endpoint(
    relation_id: UUID,
    current_user: AuthenticatedUser = Depends(require_roles(*READ_ROLES)),
    db: Session = Depends(get_db),
):

    relation = get_product_category(
        db,
        relation_id,
    )

    if relation is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("Relación producto-categoría " "no encontrada"),
        )

    return relation


# ============================================================
# PATCH /product-categories/{relation_id}
#
# Actualizar relación.
#
# Actualmente sirve principalmente para:
#
# estado = true / false
#
# Seguridad:
# ADMIN
# OPERADOR
# ============================================================


@router.patch(
    "/{relation_id}",
    response_model=ProductCategoryRead,
    status_code=status.HTTP_200_OK,
    summary=("Actualizar relación producto-categoría"),
    description=(
        "Actualiza una relación entre "
        "producto y categoría. "
        "Requiere rol ADMIN u OPERADOR."
    ),
)
def update_product_category_endpoint(
    relation_id: UUID,
    payload: ProductCategoryUpdate,
    current_user: AuthenticatedUser = Depends(
        require_roles(*PRODUCT_CATEGORY_WRITE_ROLES)
    ),
    db: Session = Depends(get_db),
):

    relation = get_product_category(
        db,
        relation_id,
    )

    if relation is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("Relación producto-categoría " "no encontrada"),
        )

    try:

        return update_product_category(
            db,
            relation,
            payload,
        )

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=("No fue posible actualizar " "la relación producto-categoría"),
        )


# ============================================================
# DELETE /product-categories/{relation_id}
#
# Eliminar una relación.
#
# Seguridad:
# ADMIN
# OPERADOR
# ============================================================


@router.delete(
    "/{relation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary=("Eliminar relación producto-categoría"),
    description=(
        "Elimina una relación entre "
        "producto y categoría. "
        "Requiere rol ADMIN u OPERADOR."
    ),
)
def delete_product_category_endpoint(
    relation_id: UUID,
    current_user: AuthenticatedUser = Depends(
        require_roles(*PRODUCT_CATEGORY_WRITE_ROLES)
    ),
    db: Session = Depends(get_db),
):

    relation = get_product_category(
        db,
        relation_id,
    )

    if relation is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("Relación producto-categoría " "no encontrada"),
        )

    delete_product_category(
        db,
        relation,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
