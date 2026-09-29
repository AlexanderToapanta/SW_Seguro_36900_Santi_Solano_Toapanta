## Lista de Activos

- API Gateway
- Código Fuente
- Repositorio de GitHub
- Base de Datos de Usuarios
- Base de Datos de Productos
- Base de Datos de Pedidos
- Microservicio de Usuarios
- Microservicio de Productos
- Microservicio de Pedidos
- Credenciales y Tokens

## Clasificación de Activos

- API Gateway -> Infraestructura
- Código Fuente -> Software
- Repositorio de GitHub -> Servicio
- Base de Datos de Usuarios -> Datos
- Base de Datos de Productos -> Datos
- Base de Datos de Pedidos -> Datos
- Microservicio de Usuarios -> Software
- Microservicio de Productos -> Software
- Microservicio de Pedidos -> Software
- Credenciales y Tokens -> Información sensible

## Tabla con su Consecuencia

| **Activo** | **Tipo** | **Consecuencia** |
|---|---|---|
| **API Gateway** | Infraestructura | Si es accedido sin autorización, un atacante podría descubrir o utilizar rutas internas de SecureShop; si es modificado, podría redirigir solicitudes o permitir accesos no autorizados; y si queda indisponible, los clientes no podrían comunicarse con los microservicios de la aplicación. |
| **Código Fuente** | Software | Si es accedido, podrían conocerse detalles internos del sistema y posibles vulnerabilidades; si es modificado, podrían introducirse errores o código malicioso; y si queda indisponible, se dificultaría el desarrollo, mantenimiento y despliegue de SecureShop. |
| **Repositorio de GitHub** | Servicio | Si es accedido sin autorización, podría exponerse el código y el historial del proyecto; si es modificado, podrían introducirse cambios maliciosos o eliminarse archivos; y si queda indisponible, el equipo de desarrollo tendría dificultades para colaborar, actualizar y desplegar el sistema. |
| **Base de Datos de Usuarios** | Datos | Si es accedida, podrían exponerse datos de los usuarios; si es modificada, podrían alterarse o eliminarse cuentas y registros; y si queda indisponible, SecureShop no podría consultar ni gestionar correctamente la información de sus usuarios. |
| **Base de Datos de Productos** | Datos | Si es accedida, podría exponerse información sobre productos, precios y existencias; si es modificada, podrían alterarse precios, productos o stock; y si queda indisponible, el catálogo de productos no podría consultarse correctamente. |
| **Base de Datos de Pedidos** | Datos | Si es accedida, podrían exponerse los pedidos e información asociada a los clientes; si es modificada, podrían cambiarse productos, cantidades, estados o datos de los pedidos; y si queda indisponible, SecureShop no podría registrar, consultar ni procesar pedidos. |
| **Microservicio de Usuarios** | Software | Si es accedido sin autorización, podrían ejecutarse operaciones restringidas relacionadas con los usuarios; si es modificado, podría alterarse la lógica de registro o gestión de cuentas; y si queda indisponible, los usuarios no podrían registrarse ni utilizar las funciones relacionadas con sus cuentas. |
| **Microservicio de Productos** | Software | Si es accedido sin autorización, podrían utilizarse funciones internas relacionadas con el catálogo; si es modificado, podría alterarse la lógica de productos, precios o inventario; y si queda indisponible, los clientes no podrían consultar correctamente los productos disponibles. |
| **Microservicio de Pedidos** | Software | Si es accedido sin autorización, podrían consultarse o ejecutarse operaciones sobre pedidos; si es modificado, podrían generarse pedidos fraudulentos o alterarse pedidos existentes; y si queda indisponible, los clientes no podrían realizar compras ni SecureShop procesar pedidos. |
| **Credenciales y Tokens** | Información sensible | Si son accedidos, un atacante podría suplantar a usuarios o acceder a funciones protegidas; si son modificados, podrían alterarse permisos o privilegios; y si quedan indisponibles, los usuarios podrían tener problemas para autenticarse y acceder a SecureShop. |