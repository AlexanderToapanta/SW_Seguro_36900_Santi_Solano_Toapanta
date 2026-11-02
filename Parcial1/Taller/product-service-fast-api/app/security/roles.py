ROLE_ADMIN = "ADMIN"
ROLE_OPERATOR = "OPERADOR"
ROLE_CLIENT = "CLIENTE"


# Todos los usuarios autenticados
READ_ROLES = (
    ROLE_ADMIN,
    ROLE_OPERATOR,
    ROLE_CLIENT,
)


# Gestión de productos
PRODUCT_WRITE_ROLES = (
    ROLE_ADMIN,
    ROLE_OPERATOR,
)


# Gestión de relaciones producto-categoría
PRODUCT_CATEGORY_WRITE_ROLES = (
    ROLE_ADMIN,
    ROLE_OPERATOR,
)


# Operaciones administrativas
ADMIN_ONLY = (ROLE_ADMIN,)
