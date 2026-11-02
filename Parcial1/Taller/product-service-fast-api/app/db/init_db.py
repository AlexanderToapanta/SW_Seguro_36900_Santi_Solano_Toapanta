from app.db.base_class import Base
from app.db.session import engine

from app.models.category import Category
from app.models.product import Product
from app.models.product_category import ProductCategory


def init_db() -> None:
    Base.metadata.create_all(
        bind=engine,
    )

if __name__ == "__main__":
    init_db()
