## 1. Lista de Activos de SecureShop

1. API Gateway
2. Código Fuente
3. Repositorio de GitHub
4. Base de Datos de Usuarios
5. Base de Datos de Productos
6. Base de Datos de Pedidos
7. Microservicio de Usuarios
8. Microservicio de Productos
9. Microservicio de Pedidos
10. Credenciales y Tokens
11. Información de Usuarios
12. Catálogo de Productos
13. Servicio de Autenticación
14. Servidor de Aplicaciones
15. Información de Proveedores


## 2. Clasificación de Activos

- API Gateway -> Infraestructura
- Código Fuente -> Software
- Repositorio de GitHub -> Servicio
- Base de Datos de Usuarios -> Datos
- Base de Datos de Productos -> Datos
- Base de Datos de Pedidos -> Datos
- Microservicio de Usuarios -> Software
- Microservicio de Productos -> Software
- Microservicio de Pedidos -> Software
- Credenciales y Tokens -> Información
- Información de Usuarios -> Información
- Catálogo de Productos -> Información
- Servicio de Autenticación -> Servicio
- Servidor de Aplicaciones -> Infraestructura
- Información de Proveedores -> Información


## 3. Consecuencias y Amenazas

| **Activo** | **Tipo** | **Consecuencia** | **Amenazas** |
|---|---|---|---|
| **API Gateway** | Infraestructura | Si es accedido sin autorización, podrían descubrirse o utilizarse rutas internas; si es modificado, podrían redirigirse solicitudes o eliminarse restricciones; y si queda indisponible, los clientes no podrían comunicarse con los microservicios. | 1. Ataques DDoS<br>2. Acceso no autorizado a endpoints<br>3. Manipulación de solicitudes |
| **Código Fuente** | Software | Si es accedido, podrían descubrirse vulnerabilidades o lógica interna; si es modificado, podrían introducirse errores o código malicioso; y si queda indisponible, se dificultaría el mantenimiento y desarrollo del sistema. | 1. Robo del código fuente<br>2. Introducción de código malicioso<br>3. Eliminación accidental o intencional |
| **Repositorio de GitHub** | Servicio | Si es accedido sin autorización, podría exponerse el código; si es modificado, podrían introducirse cambios maliciosos; y si queda indisponible, se dificultaría el trabajo y colaboración del equipo. | 1. Robo de credenciales de desarrolladores<br>2. Modificación no autorizada del repositorio<br>3. Eliminación del repositorio |
| **Base de Datos de Usuarios** | Datos | Si es accedida, podrían exponerse datos personales; si es modificada, podrían alterarse o eliminarse cuentas; y si queda indisponible, SecureShop no podría consultar ni administrar correctamente a sus usuarios. | 1. Inyección SQL<br>2. Acceso no autorizado<br>3. Pérdida o corrupción de datos |
| **Base de Datos de Productos** | Datos | Si es accedida, podría exponerse información comercial; si es modificada, podrían alterarse precios o existencias; y si queda indisponible, el catálogo no podría funcionar correctamente. | 1. Inyección SQL<br>2. Modificación fraudulenta de precios<br>3. Pérdida de información |
| **Base de Datos de Pedidos** | Datos | Si es accedida, podrían exponerse pedidos e información de clientes; si es modificada, podrían alterarse productos, cantidades o estados; y si queda indisponible, SecureShop no podría registrar ni procesar pedidos. | 1. Acceso no autorizado a pedidos<br>2. Alteración fraudulenta de pedidos<br>3. Eliminación o pérdida de pedidos |
| **Microservicio de Usuarios** | Software | Si es accedido sin autorización, podrían ejecutarse operaciones restringidas; si es modificado, podría alterarse la lógica de gestión de usuarios; y si queda indisponible, los usuarios no podrían registrarse o administrar sus cuentas. | 1. Explotación de vulnerabilidades<br>2. Acceso no autorizado a funciones<br>3. Denegación de servicio |
| **Microservicio de Productos** | Software | Si es accedido sin autorización, podrían utilizarse funciones administrativas; si es modificado, podrían alterarse precios o inventario; y si queda indisponible, los clientes no podrían consultar los productos. | 1. Modificación no autorizada del catálogo<br>2. Ataques de inyección<br>3. Denegación de servicio |
| **Microservicio de Pedidos** | Software | Si es accedido sin autorización, podrían consultarse o ejecutarse operaciones sobre pedidos; si es modificado, podrían generarse pedidos fraudulentos; y si queda indisponible, los clientes no podrían completar compras. | 1. Creación de pedidos fraudulentos<br>2. Manipulación de datos del pedido<br>3. Denegación de servicio |
| **Credenciales y Tokens** | Información | Si son accedidos, un atacante podría suplantar usuarios; si son modificados, podrían alterarse privilegios; y si quedan indisponibles, los usuarios podrían tener problemas para autenticarse. | 1. Robo de credenciales<br>2. Robo de tokens de sesión<br>3. Ataques de fuerza bruta |
| **Información de Usuarios** | Información | Si es accedida, podrían exponerse nombres, correos, direcciones u otros datos personales; si es modificada, podrían generarse errores en cuentas y entregas; y si queda indisponible, no se podría gestionar correctamente la información de los clientes. | 1. Filtración de información personal<br>2. Acceso interno no autorizado<br>3. Alteración de datos personales |
| **Catálogo de Productos** | Información | Si es accedido indebidamente, podría revelarse información comercial interna; si es modificado, podrían cambiarse precios, descripciones o disponibilidad; y si queda indisponible, los clientes no podrían visualizar los productos. | 1. Alteración de precios<br>2. Eliminación de productos<br>3. Publicación de información falsa |
| **Servicio de Autenticación** | Servicio | Si es accedido sin autorización, podría utilizarse para obtener acceso a cuentas; si es modificado, podrían alterarse las reglas de autenticación; y si queda indisponible, los usuarios no podrían iniciar sesión en SecureShop. | 1. Ataques de fuerza bruta<br>2. Robo de sesiones<br>3. Denegación de servicio |
| **Servidor de Aplicaciones** | Infraestructura | Si es accedido, un atacante podría obtener control sobre componentes de SecureShop; si es modificado, podrían alterarse configuraciones o aplicaciones; y si queda indisponible, la plataforma podría dejar de funcionar parcial o totalmente. | 1. Acceso remoto no autorizado<br>2. Malware<br>3. Fallo de hardware o sistema |
| **Información de Proveedores** | Información | Si es accedida, podrían revelarse contactos, acuerdos o precios comerciales; si es modificada, podrían alterarse datos de proveedores o condiciones comerciales; y si queda indisponible, podrían producirse problemas en compras y abastecimiento. | 1. Filtración de información comercial<br>2. Modificación de datos bancarios o contactos<br>3. Eliminación de registros |