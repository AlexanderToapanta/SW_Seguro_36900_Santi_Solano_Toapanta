# Verificación del taller — 2 de noviembre de 2026

Alcance: los microservicios de usuarios y productos y su integración JWT/RBAC.

| Bloque | Comprobación ejecutada | Resultado |
|---|---|---|
| Usuarios | Migración inicial reconocida; prueba unitaria, lint y pruebas e2e | 1 prueba unitaria; lint sin errores; 16 escenarios e2e (17 entradas contando suite) aprobados |
| Productos | Dependencias, PostgreSQL real temporal, contratos y errores HTTP simulados del servicio de usuarios | 20 pruebas aprobadas; `pip check` sin conflictos |
| Integración | Dos APIs reales y dos bases temporales, sin sustituir la autenticación | 19 escenarios aprobados |

## Comprobación final con las bases locales

Ambas APIs arrancaron en sus puertos de trabajo (3001 y 8000). Los dos Swagger y health respondieron 200; productos sin token devolvió 401; el login de `jperez` y la consulta de productos con su token funcionaron.

## Cobertura relevante

- Login por nombre/correo, contraseña incorrecta, usuario con varios roles y contrato `/auth/me`.
- Ausencia de token, firma manipulada, expiración, issuer/audience/tipo incorrectos: rechazo.
- Swagger con Bearer en las rutas protegidas de ambas APIs.
- CRUD de productos, categorías y relaciones; duplicados, padres inexistentes, UUID y paginación inválidos.
- Permisos diferenciados de ADMIN, OPERADOR y CLIENTE.
- Revocación de un rol con el mismo token, desactivación de roles/usuarios, logout y cambio de contraseña.
- Campos extra rechazados; PATCH no acepta null en campos obligatorios; precio con máximo dos decimales y stock dentro del rango de la columna.
- Borrado lógico y ocultamiento de relaciones cuyos productos o categorías fueron eliminados.
- Timeout, conexión fallida, JSON o contrato externo inválido, códigos HTTP inesperados.
- Límites originales de login y `/auth/me` conservados y comprobados. El 429 de usuarios se traduce a 503 en productos.
- Caída real del proceso de usuarios: productos devuelve 503, no guarda una escritura rechazada; al recuperar usuarios vuelve a funcionar.

## Cambios que resolvieron fallos encontrados

Se corrigieron entradas desconocidas aceptadas, valores null indebidos, redondeo de precios que podía guardar cero y provocar error 500, exposición de relaciones con padres eliminados, composición de la URL de PostgreSQL con contraseñas especiales y validación del identificador de petición reenviado.

Se completó la configuración local sin credenciales fijas en Compose, con puertos de bases ligados a localhost y seed automático desactivado. Se añadieron pruebas reproducibles y documentación de arranque para Ubuntu.

## Límites de esta verificación

Es una entrega local del taller, no una certificación de despliegue productivo. Las bases corren en Docker y las APIs en procesos locales. Productos crea sus tablas al inicializarse; no se agregó un sistema de migraciones ni una interfaz gráfica, porque no son parte de esta integración. El endpoint health de productos no comprueba la disponibilidad de usuarios. El límite de usuarios puede limitar el tráfico agregado de productos desde una misma IP.

Las pruebas automatizadas crean y eliminan bases temporales; no reinicializan las bases de trabajo. Los comandos para reproducirlas y la demostración manual están en [README del taller](README.md).
