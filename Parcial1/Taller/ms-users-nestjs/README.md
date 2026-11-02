# Microservicio de usuarios y autenticación

API REST con NestJS, TypeScript, PostgreSQL, JWT y autorización por roles.
Gestiona usuarios, roles y asignaciones. Los permisos se consultan en la base de
datos en cada petición protegida. El logout y el cambio de contraseña invalidan
los tokens anteriores del usuario.

## Requisitos

- Node.js 24 y npm.
- Docker con Docker Compose y acceso al daemon.
- Puertos locales 5432 (PostgreSQL) y 3001 (API) disponibles.

## Preparación inicial

Desde la carpeta del repositorio:

```bash
npm ci
cp example.env.dist .env
```

Configura `.env` antes de continuar. Sustituye `DB_PASSWORD` y `JWT_SECRET`
por valores propios; el secreto JWT debe tener al menos 32 caracteres.
Si `.env` ya existe, conserva su configuración. Nunca lo subas a Git.

```bash
docker compose up -d --wait
npm run migration:run
npm run seed
npm run start:dev
```

La siembra carga cinco usuarios, tres roles y seis asignaciones. Al repetirla,
actualiza los usuarios de ejemplo, restablece sus contraseñas y puede restaurar
registros eliminados; úsala únicamente con los datos del laboratorio.

## Acceso local

- API: http://localhost:3001/api/v1
- Estado: http://localhost:3001/api/v1/health
- Swagger: http://localhost:3001/docs (fuera de producción).

Login: `POST /api/v1/auth/login`

```json
{
  "identifier": "jperez",
  "password": "ClaveSegura2026!"
}
```

También se acepta el correo en `identifier`. Envía el `accessToken` obtenido
como `Authorization: Bearer TOKEN` en las peticiones protegidas.

| Usuario de ejemplo | Roles |
|---|---|
| jperez | ADMIN |
| mgomez | CLIENTE |
| cvega | CLIENTE, OPERADOR |
| amendoza | OPERADOR |
| lcastro | CLIENTE |

Todos los usuarios de ejemplo tienen la contraseña `ClaveSegura2026!`.
ADMIN administra; OPERADOR consulta; CLIENTE puede consultar su sesión y cerrarla.
El detalle de las 18 rutas está en [info/endpoints.md](info/endpoints.md).

## Comprobaciones

Con PostgreSQL encendido y `.env` preparado:

```bash
npm run build
npm test
npm run lint
npm run test:e2e
```

Las pruebas de integración compilan y arrancan una API temporal, crean una base
de datos independiente y la eliminan al terminar. No modifican los datos locales.
La cuenta de PostgreSQL necesita permiso `CREATEDB`, incluido en la cuenta de
laboratorio creada por este Docker Compose.

Verifican login por usuario/correo, JWT inválido, acceso sin token, permisos por
rol, validación, paginación, CRUD, asignación y retiro inmediato de roles,
desactivación de usuarios y roles, cambio de contraseña, logout y rate limiting.

## Ejecución compilada

```bash
npm run build
npm run start:prod
```

`start:prod` ejecuta el código compilado; el entorno efectivo sigue siendo el
valor de `NODE_ENV` en `.env`. Con `NODE_ENV=production` Swagger se desactiva.
La sincronización automática del esquema está desactivada en todos los entornos.
Los cambios de tablas se aplican explícitamente mediante migraciones.

Para detener PostgreSQL conservando sus datos:

```bash
docker compose stop
```

## Migraciones

La configuración está en `src/database/data-source.ts` y la migración inicial
en `src/database/migrations/`. Incluye usuarios, roles, asignaciones, índices,
restricciones y `token_version`.

```bash
npm run migration:show
npm run migration:run
```

Para una base nueva, ejecuta `migration:run` antes de la siembra o de iniciar la API.
Repetir el comando no vuelve a aplicar las migraciones ya registradas.

Si la base ya fue creada por la versión anterior con `synchronize`, primero:

```bash
npm run migration:baseline
```

Este comando comprueba que el esquema existente coincide con las entidades y
registra la migración inicial sin recrear tablas ni modificar los registros.
Solo acepta una base sin historial y una única migración inicial; si la estructura
es diferente, se detiene. Se usa una sola vez al adoptar una base antigua.

Para cambios futuros, modifica las entidades y genera una migración contra una
base de desarrollo que tenga aplicadas las anteriores:

```bash
npm run migration:generate -- src/database/migrations/NombreDelCambio
```

Revisa el SQL generado y luego ejecuta `npm run migration:run`.
Para revertir la última migración en una base de prueba: `npm run migration:revert`.
Revertir la migración inicial elimina las tablas; no lo uses sobre datos que
necesites conservar. Las pruebas de integración comprueban creación, reversión
y reaplicación exclusivamente en su base temporal.
