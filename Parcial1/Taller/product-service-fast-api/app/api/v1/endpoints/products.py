from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from sqlalchemy.exc import (
    IntegrityError,
)

from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.crud.product import (
    create_product,
    delete_product,
    get_product,
    get_products,
    update_product,
)

from app.schemas.auth import (
    AuthenticatedUser,
)

from app.schemas.product import (
    ProductCreate,
    ProductRead,
    ProductUpdate,
)

from app.security.dependencies import (
    require_roles,
)

from app.security.roles import (
    ADMIN_ONLY,
    PRODUCT_WRITE_ROLES,
    READ_ROLES,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


# ============================================================
# CREAR
# ADMIN / OPERADOR
# ============================================================


@router.post(
    "/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
def create_product_endpoint(
    payload: ProductCreate,
    _current_user: AuthenticatedUser = Depends(require_roles(*PRODUCT_WRITE_ROLES)),
    db: Session = Depends(get_db),
):

    try:

        return create_product(
            db,
            payload,
        )

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=409,
            detail=("Ya existe un producto " "con ese SKU"),
        )


# ============================================================
# LISTAR
# ADMIN / OPERADOR / CLIENTE
# ============================================================


@router.get(
    "/",
    response_model=list[ProductRead],
)
def list_products_endpoint(
    page: int = Query(
        1,
        ge=1,
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100,
    ),
    _current_user: AuthenticatedUser = Depends(require_roles(*READ_ROLES)),
    db: Session = Depends(get_db),
):

    skip = (page - 1) * limit

    return get_products(
        db,
        skip=skip,
        limit=limit,
    )


# ============================================================
# CONSULTAR
# ADMIN / OPERADOR / CLIENTE
# ============================================================


@router.get(
    "/{product_id}",
    response_model=ProductRead,
)
def get_product_endpoint(
    product_id: UUID,
    _current_user: AuthenticatedUser = Depends(require_roles(*READ_ROLES)),
    db: Session = Depends(get_db),
):

    db_obj = get_product(
        db,
        product_id,
    )

    if not db_obj:

        raise HTTPException(
            status_code=404,
            detail=("Producto no encontrado"),
        )

    return db_obj


# ============================================================
# ACTUALIZAR
# ADMIN / OPERADOR
# ============================================================


@router.patch(
    "/{product_id}",
    response_model=ProductRead,
)
def update_product_endpoint(
    product_id: UUID,
    payload: ProductUpdate,
    _current_user: AuthenticatedUser = Depends(require_roles(*PRODUCT_WRITE_ROLES)),
    db: Session = Depends(get_db),
):

    db_obj = get_product(
        db,
        product_id,
    )

    if not db_obj:

        raise HTTPException(
            status_code=404,
            detail=("Producto no encontrado"),
        )

    try:

        return update_product(
            db,
            db_obj,
            payload,
        )

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=409,
            detail=("Conflicto al actualizar " "el producto"),
        )


# ============================================================
# ELIMINAR
# SOLO ADMIN
# ============================================================


@router.delete(
    "/{product_id}",
    response_model=ProductRead,
)
def delete_product_endpoint(
    product_id: UUID,
    _current_user: AuthenticatedUser = Depends(require_roles(*ADMIN_ONLY)),
    db: Session = Depends(get_db),
):

    db_obj = get_product(
        db,
        product_id,
    )

    if not db_obj:

        raise HTTPException(
            status_code=404,
            detail=("Producto no encontrado"),
        )

    return delete_product(
        db,
        db_obj,
    )
