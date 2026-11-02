> **Autenticación del taller:** todas las operaciones de productos, categorías y relaciones requieren `Authorization: Bearer <accessToken>`. Obtener el token mediante login en usuarios y pegarlo en **Authorize** de este Swagger. Los ejemplos de cuerpos de esta guía presuponen ese encabezado. `/health` es público. Usar las rutas exactas que muestra Swagger; las rutas de colección pueden terminar en `/`.
>
> Permisos: todos los roles leen; ADMIN/OPERADOR escriben productos y relaciones; solo ADMIN elimina productos o escribe categorías. Guía completa de ejecución y demostración: [Instrucciones.md](../Instrucciones.md).

# Descripción del microservicio

`product-service` es un microservicio desarrollado con **FastAPI + SQLAlchemy + PostgreSQL** encargado de gestionar:

- Productos.
- Categorías.
- Relación muchos-a-muchos entre productos y categorías.

La API utiliza **UUID** como identificadores y dispone de documentación interactiva mediante **Swagger**.

## URLs durante desarrollo

- **URL base:** `http://127.0.0.1:8000`
- **API REST:** `http://127.0.0.1:8000/api/v1`
- **Swagger:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

## Endpoints principales

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/health` | Comprueba que el microservicio está funcionando |
| POST | `/api/v1/products` | Registra un nuevo producto |
| GET | `/api/v1/products` | Lista productos |
| GET | `/api/v1/products/{id}` | Consulta un producto por UUID |
| PATCH | `/api/v1/products/{id}` | Actualiza parcialmente un producto |
| DELETE | `/api/v1/products/{id}` | Realiza eliminación lógica del producto |
| POST | `/api/v1/categories` | Registra una categoría |
| GET | `/api/v1/categories` | Lista las categorías |
| GET | `/api/v1/categories/{id}` | Consulta una categoría |
| PATCH | `/api/v1/categories/{id}` | Actualiza parcialmente una categoría |
| DELETE | `/api/v1/categories/{id}` | Realiza eliminación lógica de la categoría |
| POST | `/api/v1/product-categories` | Asigna una categoría a un producto |
| GET | `/api/v1/product-categories` | Lista las relaciones producto-categoría |
| GET | `/api/v1/product-categories/{id}` | Consulta una relación específica |
| PATCH | `/api/v1/product-categories/{id}` | Activa o desactiva una relación |
| DELETE | `/api/v1/product-categories/{id}` | Elimina una relación producto-categoría |
| GET | `/api/v1/product-categories/by-product/{product_id}` | Obtiene las categorías de un producto |
| GET | `/api/v1/product-categories/by-category/{category_id}` | Obtiene los productos de una categoría |

## Cómo utilizar los endpoints

### Crear una categoría

```http
POST /api/v1/categories
Content-Type: application/json
```

```json
{
  "codigo": "MON",
  "nombre": "Monitores",
  "descripcion": "Monitores y pantallas",
  "estado": true
}
```

### Listar categorías

```http
GET /api/v1/categories?page=1&limit=20
```

La paginación permite controlar la cantidad de registros consultados.

### Consultar una categoría

```http
GET /api/v1/categories/UUID_CATEGORIA
```

Ejemplo:

```http
GET /api/v1/categories/b527e7cf-e83c-41c7-a631-a31ef1fd7a65
```

### Actualizar categoría

```http
PATCH /api/v1/categories/UUID_CATEGORIA
Content-Type: application/json
```

```json
{
  "nombre": "Monitores profesionales",
  "estado": true
}
```

Como se utiliza `PATCH`, solamente necesitas enviar los campos que deseas modificar.

### Eliminar categoría

```http
DELETE /api/v1/categories/UUID_CATEGORIA
```

En el diseño actual se realiza una eliminación lógica:

```text
estado = false
fecha_eliminacion = fecha actual
```

## Productos

### Crear un producto

```http
POST /api/v1/products
Content-Type: application/json
```

```json
{
  "sku": "PROD-100",
  "nombre": "Monitor LG 27 pulgadas",
  "descripcion": "Monitor IPS Full HD",
  "marca": "LG",
  "precio_venta": 249.99,
  "stock": 15,
  "stock_minimo": 3,
  "estado": true
}
```

### Listar productos

```http
GET /api/v1/products?page=1&limit=20
```

### Consultar producto

```http
GET /api/v1/products/UUID_PRODUCTO
```

### Actualizar producto

Por ejemplo, actualizar precio y stock:

```http
PATCH /api/v1/products/UUID_PRODUCTO
Content-Type: application/json
```

```json
{
  "precio_venta": 229.99,
  "stock": 12
}
```

### Eliminar producto

```http
DELETE /api/v1/products/UUID_PRODUCTO
```

La eliminación también es lógica.

## Relación producto-categoría

Un producto puede pertenecer a varias categorías y una categoría puede contener varios productos.

```text
PRODUCTS
    N
    │
    ▼
PRODUCT_CATEGORIES
    ▲
    │
    N
CATEGORIES
```

### Asignar categoría a producto

Primero debes conocer:

- `product_id`
- `category_id`

Después:

```http
POST /api/v1/product-categories
Content-Type: application/json
```

```json
{
  "product_id": "UUID_PRODUCTO",
  "category_id": "UUID_CATEGORIA",
  "estado": true
}
```

Por ejemplo:

```json
{
  "product_id": "fdc3402e-c163-468f-b415-e57c1ab63732",
  "category_id": "efea863d-8b39-47ed-93cb-a9741bf18f58",
  "estado": true
}
```

La misma combinación producto-categoría no puede registrarse dos veces.

### Consultar todas las relaciones

```http
GET /api/v1/product-categories?page=1&limit=20
```

### Consultar categorías de un producto

```http
GET /api/v1/product-categories/by-product/UUID_PRODUCTO
```

Por ejemplo:

```http
GET /api/v1/product-categories/by-product/fdc3402e-c163-468f-b415-e57c1ab63732
```

Puede devolver:

```json
[
  {
    "product_id": "fdc3402e-c163-468f-b415-e57c1ab63732",
    "category_id": "efea863d-8b39-47ed-93cb-a9741bf18f58",
    "estado": true,
    "category": {
      "codigo": "TEC",
      "nombre": "Tecnología"
    }
  }
]
```

### Consultar productos de una categoría

```http
GET /api/v1/product-categories/by-category/UUID_CATEGORIA
```

Por ejemplo:

```http
GET /api/v1/product-categories/by-category/efea863d-8b39-47ed-93cb-a9741bf18f58
```