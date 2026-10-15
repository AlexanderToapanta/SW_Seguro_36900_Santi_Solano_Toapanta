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

La clasificación de las bases de datos corresponde a su contenido almacenado. La información de proveedores se considera parte de la gestión interna de abastecimiento de SecureShop.

- API Gateway -> Servicio
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
| **API Gateway** | Servicio | Si es accedido sin autorización, podrían descubrirse o utilizarse rutas internas; si es modificado, podrían redirigirse solicitudes o eliminarse restricciones; y si queda indisponible, los clientes no podrían comunicarse con los microservicios. | 1. Ataques DDoS<br>2. Acceso no autorizado a endpoints<br>3. Manipulación de solicitudes |
| **Código Fuente** | Software | Si es accedido sin autorización, podrían descubrirse vulnerabilidades o lógica interna; si es modificado, podrían introducirse errores o código malicioso; y si queda indisponible, se dificultaría el mantenimiento y desarrollo del sistema. | 1. Robo del código fuente<br>2. Introducción de código malicioso<br>3. Eliminación accidental o intencional |
| **Repositorio de GitHub** | Servicio | Si es accedido sin autorización, podría exponerse el código; si es modificado, podrían introducirse cambios maliciosos; y si queda indisponible, se dificultaría el trabajo y colaboración del equipo. | 1. Robo de credenciales de desarrolladores<br>2. Modificación no autorizada del repositorio<br>3. Eliminación del repositorio |
| **Base de Datos de Usuarios** | Datos | Si es accedida, podrían exponerse datos personales; si es modificada, podrían alterarse o eliminarse cuentas; y si queda indisponible, SecureShop no podría consultar ni administrar correctamente a sus usuarios. | 1. Inyección SQL<br>2. Acceso no autorizado<br>3. Pérdida o corrupción de datos |
| **Base de Datos de Productos** | Datos | Si es accedida sin autorización, podría exponerse información comercial interna; si es modificada, podrían alterarse precios o existencias; y si queda indisponible, el catálogo no podría funcionar correctamente. | 1. Inyección SQL<br>2. Modificación fraudulenta de precios<br>3. Pérdida de información |
| **Base de Datos de Pedidos** | Datos | Si es accedida, podrían exponerse pedidos e información de clientes; si es modificada, podrían alterarse productos, cantidades o estados; y si queda indisponible, SecureShop no podría registrar ni procesar pedidos. | 1. Acceso no autorizado a pedidos<br>2. Alteración fraudulenta de pedidos<br>3. Eliminación o pérdida de pedidos |
| **Microservicio de Usuarios** | Software | Si es accedido sin autorización, podrían ejecutarse operaciones restringidas; si es modificado, podría alterarse la lógica de gestión de usuarios; y si queda indisponible, los usuarios no podrían registrarse o administrar sus cuentas. | 1. Explotación de dependencias vulnerables<br>2. Acceso no autorizado a funciones<br>3. Denegación de servicio |
| **Microservicio de Productos** | Software | Si es accedido sin autorización, podrían utilizarse funciones administrativas; si es modificado, podrían alterarse precios o inventario; y si queda indisponible, los clientes no podrían consultar los productos. | 1. Modificación no autorizada del catálogo<br>2. Ataques de inyección<br>3. Denegación de servicio |
| **Microservicio de Pedidos** | Software | Si es accedido sin autorización, podrían consultarse o ejecutarse operaciones sobre pedidos; si es modificado, podrían generarse pedidos fraudulentos; y si queda indisponible, los clientes no podrían completar compras. | 1. Creación de pedidos fraudulentos<br>2. Manipulación de datos del pedido<br>3. Denegación de servicio |
| **Credenciales y Tokens** | Información | Si son accedidos, un atacante podría suplantar usuarios; si son modificados, podría impedirse la autenticación o, si se aceptan tokens manipulados, alterarse privilegios; y si quedan indisponibles, los usuarios podrían tener problemas para autenticarse. | 1. Robo de credenciales<br>2. Robo de tokens de sesión<br>3. Ataques de fuerza bruta |
| **Información de Usuarios** | Información | Si es accedida, podrían exponerse nombres, correos, direcciones u otros datos personales; si es modificada, podrían generarse errores en cuentas y entregas; y si queda indisponible, no se podría gestionar correctamente la información de los clientes. | 1. Filtración de información personal<br>2. Acceso interno no autorizado<br>3. Alteración de datos personales |
| **Catálogo de Productos** | Información | La consulta del catálogo público no supone una pérdida de confidencialidad; si se accede sin autorización a su información interna, podrían revelarse costos o productos no publicados; si es modificado, podrían cambiarse precios, descripciones o disponibilidad; y si queda indisponible, los clientes no podrían visualizar los productos. | 1. Alteración de precios<br>2. Eliminación de productos<br>3. Publicación de información falsa |
| **Servicio de Autenticación** | Servicio | Si es accedido sin autorización, podría utilizarse para obtener acceso a cuentas; si es modificado, podrían alterarse las reglas de autenticación; y si queda indisponible, los usuarios no podrían iniciar sesión en SecureShop. | 1. Ataques de fuerza bruta<br>2. Robo de sesiones<br>3. Denegación de servicio |
| **Servidor de Aplicaciones** | Infraestructura | Si es accedido sin autorización, un atacante podría obtener control sobre componentes de SecureShop; si es modificado, podrían alterarse configuraciones o aplicaciones; y si queda indisponible, la plataforma podría dejar de funcionar parcial o totalmente. | 1. Acceso remoto no autorizado<br>2. Malware<br>3. Fallo de hardware o sistema |
| **Información de Proveedores** | Información | Si es accedida, podrían revelarse contactos, acuerdos o precios comerciales; si es modificada, podrían alterarse datos de proveedores o condiciones comerciales; y si queda indisponible, podrían producirse problemas en compras y abastecimiento. | 1. Filtración de información comercial<br>2. Modificación de datos bancarios o contactos<br>3. Eliminación de registros |

## 4. Mecanismos de Control y Mitigación

Los siguientes mecanismos corresponden a las 45 amenazas identificadas. Su implementación debe realizarse en el código o la configuración del proyecto; esta documentación no acredita por sí sola que estén implementados.

### 4.1. API Gateway

| Amenaza | Mecanismo de control y mitigación |
|---|---|
| Ataques DDoS | Configurar protección DDoS en el proveedor de alojamiento y límites de solicitudes por IP o cliente en el Gateway. Los límites locales reducen abusos, pero no bastan ante ataques volumétricos. |
| Acceso no autorizado a endpoints | Validar tokens y permisos por ruta en el Gateway y comprobar también la autorización en cada microservicio. |
| Manipulación de solicitudes | Habilitar HTTPS y validar los tipos, el tamaño y los campos permitidos en las solicitudes. |

### 4.2. Código Fuente

| Amenaza | Mecanismo de control y mitigación |
|---|---|
| Robo del código fuente | Mantener el repositorio privado y conceder acceso únicamente a integrantes autorizados. |
| Introducción de código malicioso | Proteger la rama principal y exigir revisión mediante pull requests antes de integrar cambios. |
| Eliminación accidental o intencional | Mantener una copia independiente del repositorio y verificar que permite recuperar el código y su historial. |

### 4.3. Repositorio de GitHub

| Amenaza | Mecanismo de control y mitigación |
|---|---|
| Robo de credenciales de desarrolladores | Activar autenticación de dos factores y utilizar cuentas individuales, sin compartir credenciales. |
| Modificación no autorizada del repositorio | Asignar permisos mínimos y proteger la rama principal contra cambios directos y sobrescrituras forzadas. |
| Eliminación del repositorio | Restringir los permisos administrativos y conservar una copia externa recuperable. |

### 4.4. Base de Datos de Usuarios

| Amenaza | Mecanismo de control y mitigación |
|---|---|
| Inyección SQL | Utilizar consultas parametrizadas; no concatenar entradas del usuario en instrucciones SQL. |
| Acceso no autorizado | Utilizar una cuenta exclusiva del microservicio de Usuarios con permisos mínimos y mantener la base de datos en una red privada. |
| Pérdida o corrupción de datos | Programar copias de seguridad y verificar su funcionamiento mediante una restauración. |

### 4.5. Base de Datos de Productos

| Amenaza | Mecanismo de control y mitigación |
|---|---|
| Inyección SQL | Implementar consultas parametrizadas en todas las operaciones sobre productos. |
| Modificación fraudulenta de precios | Autorizar cambios únicamente a roles administrativos y registrar usuario, fecha, precio anterior y precio nuevo. |
| Pérdida de información | Configurar copias de seguridad periódicas y comprobar la recuperación de los registros. |

### 4.6. Base de Datos de Pedidos

| Amenaza | Mecanismo de control y mitigación |
|---|---|
| Acceso no autorizado a pedidos | Verificar en el servidor que cada pedido pertenece al usuario autenticado, salvo acceso administrativo autorizado. |
| Alteración fraudulenta de pedidos | Restringir los permisos de modificación y validar las transiciones de estado; un cliente no debe poder marcar su pedido como pagado. |
| Eliminación o pérdida de pedidos | Restringir la eliminación definitiva y mantener copias de seguridad verificadas. |

### 4.7. Microservicio de Usuarios

| Amenaza | Mecanismo de control y mitigación |
|---|---|
| Explotación de dependencias vulnerables | Incorporar análisis de dependencias en la integración continua y actualizar las bibliotecas vulnerables. |
| Acceso no autorizado a funciones | Implementar autorización por rol y por propietario del recurso en las operaciones protegidas. |
| Denegación de servicio | Limitar solicitudes, tamaño de entradas y tiempos de ejecución. |

### 4.8. Microservicio de Productos

| Amenaza | Mecanismo de control y mitigación |
|---|---|
| Modificación no autorizada del catálogo | Restringir la creación, modificación y eliminación de productos a usuarios con rol administrativo. |
| Ataques de inyección | Validar los campos recibidos y utilizar consultas parametrizadas para acceder a la base de datos. |
| Denegación de servicio | Limitar solicitudes y aplicar paginación con un máximo de resultados por consulta. |

### 4.9. Microservicio de Pedidos

| Amenaza | Mecanismo de control y mitigación |
|---|---|
| Creación de pedidos fraudulentos | Exigir autenticación y validar productos, cantidades y existencias en el servidor antes de registrar un pedido. |
| Manipulación de datos del pedido | Calcular precios y totales en el servidor a partir del catálogo, sin confiar en importes enviados por el cliente. |
| Denegación de servicio | Limitar la creación de pedidos por usuario y establecer tiempos máximos para llamadas a otros servicios. |

### 4.10. Credenciales y Tokens

| Amenaza | Mecanismo de control y mitigación |
|---|---|
| Robo de credenciales | Almacenar contraseñas con hash seguro, como Argon2id, y guardar secretos de servicios fuera del código y del repositorio. |
| Robo de tokens de sesión | Utilizar HTTPS, evitar tokens en logs y establecer caducidad. Si se usan cookies, configurar HttpOnly, Secure y una política SameSite adecuada. |
| Ataques de fuerza bruta | Limitar intentos por cuenta e IP y aplicar retrasos progresivos ante fallos repetidos. |

### 4.11. Información de Usuarios

| Amenaza | Mecanismo de control y mitigación |
|---|---|
| Filtración de información personal | Devolver únicamente campos necesarios en la API y excluir contraseñas, hashes y datos sensibles innecesarios. |
| Acceso interno no autorizado | Aplicar permisos por rol y registrar accesos administrativos a información personal. |
| Alteración de datos personales | Verificar que el usuario modifica su propio perfil y exigir reautenticación para cambios sensibles, como contraseña o correo. |

### 4.12. Catálogo de Productos

| Amenaza | Mecanismo de control y mitigación |
|---|---|
| Alteración de precios | Restringir los cambios a roles autorizados y conservar un historial de modificaciones. |
| Eliminación de productos | Implementar eliminación lógica para desactivar productos y permitir su recuperación. |
| Publicación de información falsa | Incorporar un estado de borrador y exigir aprobación de un usuario autorizado antes de publicar productos o cambios relevantes. |

### 4.13. Servicio de Autenticación

| Amenaza | Mecanismo de control y mitigación |
|---|---|
| Ataques de fuerza bruta | Aplicar límites de intentos y retrasos progresivos por cuenta e IP. |
| Robo de sesiones | Configurar caducidad, rotación de tokens de renovación y revocación de sesiones comprometidas. |
| Denegación de servicio | Limitar solicitudes de inicio de sesión y establecer un máximo de operaciones de autenticación concurrentes. |

### 4.14. Servidor de Aplicaciones

| Amenaza | Mecanismo de control y mitigación |
|---|---|
| Acceso remoto no autorizado | Restringir el acceso administrativo con firewall y autenticación SSH mediante claves; deshabilitar el acceso directo de root. |
| Malware | Mantener el sistema actualizado y ejecutar los servicios con usuarios sin privilegios administrativos. |
| Fallo de hardware o sistema | Configurar monitoreo, copias de seguridad y un procedimiento de recuperación en otra instancia. |

### 4.15. Información de Proveedores

| Amenaza | Mecanismo de control y mitigación |
|---|---|
| Filtración de información comercial | Restringir consultas a roles de compras o administración y excluir estos datos de endpoints públicos. |
| Modificación de datos bancarios o contactos | Exigir reautenticación para cambios sensibles y aprobación de otro usuario autorizado para cambios bancarios; conservar el historial. |
| Eliminación de registros | Implementar eliminación lógica y copias de seguridad que permitan recuperar registros. |
