# Microservicio de productos — Taller JWT

FastAPI, SQLAlchemy y PostgreSQL para productos, categorías y sus relaciones. Autentica cada petición protegida consultando `/api/v1/auth/me` del microservicio NestJS de usuarios; aplica permisos ADMIN, OPERADOR y CLIENTE sin compartir el secreto JWT.

La guía de arranque, demostración, cuentas y preparación desde cero está en [README del taller](../README.md). Los resultados están en [Verificacion.md](../Verificacion.md). El enunciado detallado se conserva en [TallerJWT.md](TallerJWT.md) y las operaciones en [GuiaEndpoints.md](GuiaEndpoints.md).

## Arranque local

Con `.env`, entorno virtual y base ya preparados:

```bash
# Terminal para PostgreSQL
docker compose -f docker-compose.product-db.yml up product-postgres
```

```bash
# Otra terminal para FastAPI
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Usuarios debe estar disponible en `http://127.0.0.1:3001`. Swagger de productos: http://127.0.0.1:8000/docs. Solo `/health` es público entre las rutas de negocio; la documentación también es accesible.

El archivo de ejemplo es `example.env.dist`; copiarlo a `.env` y cambiar la contraseña antes de preparar una instalación nueva. PostgreSQL de productos escucha únicamente en localhost:5433. `ENABLE_SEED=false` evita reactivar datos de ejemplo en cada arranque.

## Inicialización manual y pruebas

```bash
.venv/bin/python -m app.db.init_db
.venv/bin/python -m app.db.seed
.venv/bin/python scripts/test_local.py
.venv/bin/python ../scripts/test_integration.py
```

Los dos primeros comandos son de preparación, no se necesitan en cada arranque. Las pruebas usan bases temporales y las eliminan al terminar. Las de integración necesitan ambas instancias de PostgreSQL y las dependencias del servicio de usuarios.

Las entradas rechazan campos desconocidos, precios con más de dos decimales y nulos en campos obligatorios. Las relaciones de productos o categorías eliminados no aparecen en consultas. Un fallo de autenticación externa impide la operación; no se autoriza por omisión.
