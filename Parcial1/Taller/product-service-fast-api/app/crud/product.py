from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(db: Session, obj_in: ProductCreate) -> Product:
    db_obj = Product(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_product(db: Session, product_id):
    stmt = select(Product).where(
        Product.id == product_id,
        Product.fecha_eliminacion.is_(None),
    )
    return db.scalar(stmt)


def get_products(db: Session, skip: int = 0, limit: int = 20):
    stmt = (
        select(Product)
        .where(Product.fecha_eliminacion.is_(None))
        .offset(skip)
        .limit(limit)
        .order_by(Product.nombre.asc())
    )
    return db.scalars(stmt).all()


def update_product(db: Session, db_obj: Product, obj_in: ProductUpdate) -> Product:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_product(db: Session, db_obj: Product) -> Product:
    db_obj.estado = False
    db_obj.fecha_eliminacion = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_obj)
    return db_obj