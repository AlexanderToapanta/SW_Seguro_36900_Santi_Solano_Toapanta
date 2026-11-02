from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.models.category import Category
from app.models.product import Product
from app.models.product_category import ProductCategory


# ============================================================
# CATEGORÍAS
# ============================================================

CATEGORIES = [
    {
        "codigo": "TEC",
        "nombre": "Tecnología",
        "descripcion": "Productos tecnológicos y electrónicos",
        "estado": True,
    },
    {
        "codigo": "PER",
        "nombre": "Periféricos",
        "descripcion": "Dispositivos periféricos para computadoras",
        "estado": True,
    },
    {
        "codigo": "ACC",
        "nombre": "Accesorios",
        "descripcion": "Accesorios tecnológicos",
        "estado": True,
    },
    {
        "codigo": "RED",
        "nombre": "Redes",
        "descripcion": "Equipos y accesorios de conectividad",
        "estado": True,
    },
    {
        "codigo": "ALM",
        "nombre": "Almacenamiento",
        "descripcion": "Dispositivos de almacenamiento de datos",
        "estado": True,
    },
]


# ============================================================
# PRODUCTOS
# ============================================================

PRODUCTS = [
    {
        "sku": "PROD-001",
        "nombre": "Laptop Lenovo ThinkPad",
        "descripcion": "Laptop empresarial con 16 GB RAM y SSD",
        "marca": "Lenovo",
        "precio_venta": Decimal("1200.00"),
        "stock": 10,
        "stock_minimo": 2,
        "estado": True,
    },
    {
        "sku": "PROD-002",
        "nombre": "Mouse Inalámbrico",
        "descripcion": "Mouse inalámbrico ergonómico",
        "marca": "Logitech",
        "precio_venta": Decimal("25.90"),
        "stock": 50,
        "stock_minimo": 5,
        "estado": True,
    },
    {
        "sku": "PROD-003",
        "nombre": "Teclado Mecánico",
        "descripcion": "Teclado mecánico USB",
        "marca": "Redragon",
        "precio_venta": Decimal("65.00"),
        "stock": 30,
        "stock_minimo": 5,
        "estado": True,
    },
    {
        "sku": "PROD-004",
        "nombre": "Router WiFi 6",
        "descripcion": "Router inalámbrico WiFi 6",
        "marca": "TP-Link",
        "precio_venta": Decimal("95.50"),
        "stock": 20,
        "stock_minimo": 3,
        "estado": True,
    },
    {
        "sku": "PROD-005",
        "nombre": "SSD 1TB",
        "descripcion": "Unidad de estado sólido de 1 TB",
        "marca": "Kingston",
        "precio_venta": Decimal("89.99"),
        "stock": 25,
        "stock_minimo": 4,
        "estado": True,
    },
]


# ============================================================
# RELACIONES PRODUCTO - CATEGORÍA
#
# Se trabaja con SKU y código porque son identificadores
# naturales y conocidos antes de generar los UUID.
# ============================================================

PRODUCT_CATEGORIES = [
    {
        "sku": "PROD-001",
        "category_code": "TEC",
    },

    {
        "sku": "PROD-002",
        "category_code": "TEC",
    },
    {
        "sku": "PROD-002",
        "category_code": "PER",
    },
    {
        "sku": "PROD-002",
        "category_code": "ACC",
    },

    {
        "sku": "PROD-003",
        "category_code": "TEC",
    },
    {
        "sku": "PROD-003",
        "category_code": "PER",
    },

    {
        "sku": "PROD-004",
        "category_code": "TEC",
    },
    {
        "sku": "PROD-004",
        "category_code": "RED",
    },

    {
        "sku": "PROD-005",
        "category_code": "TEC",
    },
    {
        "sku": "PROD-005",
        "category_code": "ALM",
    },
]


# ============================================================
# SEED DE CATEGORÍAS
# ============================================================

def seed_categories(
    db: Session,
) -> dict[str, Category]:

    categories: dict[str, Category] = {}

    print("📂 Registrando categorías...")

    for item in CATEGORIES:

        statement = select(Category).where(
            Category.codigo == item["codigo"]
        )

        category = db.scalar(statement)

        if category is None:

            category = Category(
                **item,
            )

            db.add(category)

            db.flush()

            print(
                f"   ✅ Categoría creada: "
                f"{category.codigo} - "
                f"{category.nombre}"
            )

        else:

            print(
                f"   ℹ️ Categoría existente: "
                f"{category.codigo}"
            )

        categories[category.codigo] = category

    db.commit()

    return categories


# ============================================================
# SEED DE PRODUCTOS
# ============================================================

def seed_products(
    db: Session,
) -> dict[str, Product]:

    products: dict[str, Product] = {}

    print("📦 Registrando productos...")

    for item in PRODUCTS:

        statement = select(Product).where(
            Product.sku == item["sku"]
        )

        product = db.scalar(statement)

        if product is None:

            product = Product(
                **item,
            )

            db.add(product)

            db.flush()

            print(
                f"   ✅ Producto creado: "
                f"{product.sku} - "
                f"{product.nombre}"
            )

        else:

            print(
                f"   ℹ️ Producto existente: "
                f"{product.sku}"
            )

        products[product.sku] = product

    db.commit()

    return products


# ============================================================
# SEED PRODUCTO - CATEGORÍA
# ============================================================

def seed_product_categories(
    db: Session,
    products: dict[str, Product],
    categories: dict[str, Category],
) -> None:

    print(
        "🔗 Registrando relaciones "
        "producto-categoría..."
    )

    for relation in PRODUCT_CATEGORIES:

        sku = relation["sku"]

        category_code = relation[
            "category_code"
        ]

        product = products.get(
            sku
        )

        category = categories.get(
            category_code
        )

        if product is None:

            print(
                f"   ⚠️ Producto no encontrado: "
                f"{sku}"
            )

            continue

        if category is None:

            print(
                f"   ⚠️ Categoría no encontrada: "
                f"{category_code}"
            )

            continue

        statement = select(
            ProductCategory
        ).where(
            ProductCategory.product_id
            == product.id,

            ProductCategory.category_id
            == category.id,
        )

        product_category = db.scalar(
            statement
        )

        if product_category is None:

            product_category = (
                ProductCategory(
                    product_id=
                        product.id,

                    category_id=
                        category.id,

                    estado=True,
                )
            )

            db.add(
                product_category
            )

            print(
                f"   ✅ {product.sku} "
                f"→ {category.codigo}"
            )

        else:

            # Si ya existe pero estaba
            # desactivada, se reactiva.
            if not product_category.estado:

                product_category.estado = (
                    True
                )

                print(
                    f"   ♻️ Relación reactivada: "
                    f"{product.sku} "
                    f"→ {category.codigo}"
                )

            else:

                print(
                    f"   ℹ️ Relación existente: "
                    f"{product.sku} "
                    f"→ {category.codigo}"
                )

    db.commit()


# ============================================================
# SEED PRINCIPAL
# ============================================================

def seed_database() -> None:

    db = SessionLocal()

    try:

        print(
            "\n"
            "======================================"
        )

        print(
            "🌱 Iniciando siembra de Product Service"
        )

        print(
            "======================================"
        )

        categories = seed_categories(
            db
        )

        products = seed_products(
            db
        )

        seed_product_categories(
            db,
            products,
            categories,
        )

        print(
            "======================================"
        )

        print(
            "✅ Siembra completada correctamente"
        )

        print(
            f"📂 Categorías: "
            f"{len(categories)}"
        )

        print(
            f"📦 Productos: "
            f"{len(products)}"
        )

        print(
            f"🔗 Relaciones configuradas: "
            f"{len(PRODUCT_CATEGORIES)}"
        )

        print(
            "======================================"
            "\n"
        )

    except Exception as error:

        db.rollback()

        print(
            "❌ Error durante la siembra"
        )

        print(
            str(error)
        )

        raise

    finally:

        db.close()


# ============================================================
# EJECUCIÓN MANUAL
# ============================================================

if __name__ == "__main__":
    seed_database()