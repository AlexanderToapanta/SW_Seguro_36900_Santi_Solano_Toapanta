# Taller JWT: usuarios y productos

Integración de dos microservicios mediante autenticación JWT y autorización por roles:

- `ms-users-nestjs`: usuarios, roles, login y validación de tokens con NestJS y PostgreSQL.
- `product-service-fast-api`: productos, categorías y sus relaciones con FastAPI y PostgreSQL.

Cada operación protegida de productos consulta `GET /api/v1/auth/me` en usuarios y aplica los permisos correspondientes. Cada servicio mantiene su propia base de datos; el secreto JWT pertenece al servicio de usuarios.

## Requisitos y preparación inicial

Docker con Compose, Node.js 24 y Python con soporte `venv` (probado con Python 3.14). Ejecutar los comandos desde la carpeta `Taller`.

En usuarios:

```bash
cd ms-users-nestjs
cp example.env.dist .env
```

Configurar una contraseña de base de datos propia y un `JWT_SECRET` de al menos 32 caracteres. Si ya existe `.env`, conservar su configuración.

```bash
npm ci
docker compose up -d --wait
npm run migration:run
npm run seed
cd ..
```

En productos:

```bash
cd product-service-fast-api
cp example.env.dist .env
```

Configurar una contraseña de base de datos propia, `USER_SERVICE_URL=http://127.0.0.1:3001` y `ENABLE_SEED=false`. Si ya existe `.env`, conservar su configuración.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
docker compose -f docker-compose.product-db.yml up -d --wait
.venv/bin/python -m app.db.init_db
.venv/bin/python -m app.db.seed
cd ..
```

La preparación y la carga de datos se realizan una vez. Repetir los seeds puede restablecer datos y contraseñas de ejemplo. Los archivos `.env` se excluyen de Git.

## Iniciar los servicios

En cuatro terminales, partiendo de `Taller`. Esperar a que cada base esté lista antes de iniciar su API.

**1. PostgreSQL de usuarios (5432):**

```bash
cd ms-users-nestjs
docker compose up postgres
```

**2. API de usuarios (3001):**

```bash
cd ms-users-nestjs
npm run start:dev
```

**3. PostgreSQL de productos (5433):**

```bash
cd product-service-fast-api
docker compose -f docker-compose.product-db.yml up product-postgres
```

**4. API de productos (8000):**

```bash
cd product-service-fast-api
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Solo las bases de datos se ejecutan en contenedores. Para detener las APIs, usar `Ctrl+C`. Para detener las bases, ejecutar `docker compose stop` en usuarios y `docker compose -f docker-compose.product-db.yml stop` en productos. Los volúmenes conservan los datos; `down -v` los elimina.

## Probar la integración en Swagger

1. Abrir [usuarios](http://localhost:3001/docs) y [productos](http://127.0.0.1:8000/docs).
2. En productos, ejecutar `GET /health`: responde **200**. Ejecutar `GET /api/v1/products/` sin token: responde **401**.
3. En usuarios, ejecutar `POST /api/v1/auth/login` con las credenciales de ejemplo:

```json
{"identifier":"jperez","password":"ClaveSegura2026!"}
```

4. Copiar el valor de `accessToken`. En **Authorize** de productos, pegar únicamente el token, sin comillas ni el prefijo `Bearer`.
5. Repetir `GET /api/v1/products/`: responde **200**. El administrador puede crear, editar y eliminar productos.
6. Iniciar sesión como `mgomez`, con la misma contraseña de ejemplo, y sustituir el token en productos: consultar devuelve **200**, pero crear devuelve **403**.
7. Autorizar también Swagger de usuarios con el token de `mgomez` y ejecutar `POST /api/v1/auth/logout`. La siguiente consulta a productos con ese token devuelve **401**.

Swagger añade el encabezado `Authorization: Bearer <token>` a cada petición autorizada. La autorización debe configurarse en cada Swagger por separado.

| Operación | ADMIN (`jperez`) | OPERADOR (`amendoza`) | CLIENTE (`mgomez`) |
|---|---|---|---|
| Consultar productos, categorías y relaciones | Sí | Sí | Sí |
| Crear/editar productos | Sí | Sí | No |
| Eliminar productos | Sí | No | No |
| Crear/editar/eliminar categorías | Sí | No | No |
| Crear/editar/eliminar relaciones | Sí | Sí | No |

Los datos de acceso son exclusivos del laboratorio. Los permisos reflejan cambios de roles y desactivaciones. El logout y el cambio de contraseña invalidan tokens anteriores.

Si usuarios no está disponible, productos devuelve **503** en las rutas protegidas. También devuelve 503 si usuarios responde 429 por su límite de peticiones; esperar al reinicio de la ventana antes de reintentar. `/health` de productos verifica su propia disponibilidad.

## Pruebas automatizadas

Con ambas bases encendidas, ejecutar desde `Taller`:

```bash
cd ms-users-nestjs
npm test
npm run lint
npm run test:e2e
cd ../product-service-fast-api
.venv/bin/python scripts/test_local.py
.venv/bin/python ../scripts/test_integration.py
```

Los runners crean bases temporales y las eliminan al finalizar; las pruebas de integración arrancan sus propias APIs. Los usuarios de PostgreSQL del laboratorio necesitan permiso para crear bases.

Resultados: [Verificacion.md](Verificacion.md). Documentación de cada servicio: [usuarios](ms-users-nestjs/README.md) y [productos](product-service-fast-api/README.md).
