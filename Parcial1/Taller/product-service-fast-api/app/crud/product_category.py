from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.product_category import ProductCategory
from app.models.product import Product
from app.models.category import Category
from app.schemas.product_category import ProductCategoryCreate, ProductCategoryUpdate


def visible_relations():
    # El borrado lógico de un padre también debe respetarse en las consultas N:M.
    return (select(ProductCategory)
        .join(ProductCategory.product)
        .join(ProductCategory.category)
        .where(Product.fecha_eliminacion.is_(None), Category.fecha_eliminacion.is_(None)))


def create_product_category(db: Session, obj_in: ProductCategoryCreate) -> ProductCategory:
    db_obj = ProductCategory(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_product_category(db: Session, relation_id):
    stmt = (
        visible_relations()
        .options(
            joinedload(ProductCategory.product),
            joinedload(ProductCategory.category),
        )
        .where(ProductCategory.id == relation_id)
    )
    return db.scalar(stmt)


def get_product_categories(db: Session, skip: int = 0, limit: int = 20):
    stmt = (
        visible_relations()
        .options(
            joinedload(ProductCategory.product),
            joinedload(ProductCategory.category),
        )
        .offset(skip)
        .limit(limit)
        .order_by(ProductCategory.fecha_creacion.desc())
    )
    return db.scalars(stmt).all()


def get_categories_by_product(db: Session, product_id):
    stmt = (
        visible_relations()
        .options(
            joinedload(ProductCategory.product),
            joinedload(ProductCategory.category),
        )
        .where(ProductCategory.product_id == product_id)
    )
    return db.scalars(stmt).all()


def get_products_by_category(db: Session, category_id):
    stmt = (
        visible_relations()
        .options(
            joinedload(ProductCategory.product),
            joinedload(ProductCategory.category),
        )
        .where(ProductCategory.category_id == category_id)
    )
    return db.scalars(stmt).all()


def update_product_category(
    db: Session,
    db_obj: ProductCategory,
    obj_in: ProductCategoryUpdate,
) -> ProductCategory:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_product_category(db: Session, db_obj: ProductCategory) -> None:
    db.delete(db_obj)
    db.commit()