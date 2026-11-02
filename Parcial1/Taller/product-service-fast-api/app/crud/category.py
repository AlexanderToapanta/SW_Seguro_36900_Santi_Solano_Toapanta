from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def create_category(db: Session, obj_in: CategoryCreate) -> Category:
    db_obj = Category(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_category(db: Session, category_id):
    stmt = select(Category).where(
        Category.id == category_id,
        Category.fecha_eliminacion.is_(None),
    )
    return db.scalar(stmt)


def get_categories(db: Session, skip: int = 0, limit: int = 20):
    stmt = (
        select(Category)
        .where(Category.fecha_eliminacion.is_(None))
        .offset(skip)
        .limit(limit)
        .order_by(Category.nombre.asc())
    )
    return db.scalars(stmt).all()


def update_category(db: Session, db_obj: Category, obj_in: CategoryUpdate) -> Category:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_category(db: Session, db_obj: Category) -> Category:
    db_obj.estado = False
    db_obj.fecha_eliminacion = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_obj)
    return db_obj