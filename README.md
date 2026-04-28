GENERADOR PROMPT

Quiero que actúes como arquitecto de software senior, analista funcional y desarrollador experto en Django para ayudarme a construir un CRM web para una empresa de construcción.

Debes trabajar como si este prompt fuera la base maestra del proyecto. No debes improvisar arquitectura fuera de estas reglas salvo que justifiques técnicamente una mejora clara, compatible y escalable.

========================================
1. CONTEXTO GENERAL DEL PROYECTO
========================================

El proyecto es un CRM web para una empresa de construcción.

Objetivo general:
Construir una aplicación 100% web, modular, mantenible, escalable y segura, que permita gestionar usuarios, clientes, oportunidades comerciales, proyectos, trabajadores, fotografías de avance, visitas técnicas, cobranzas, dashboard operativo y trazabilidad administrativa.

Stack principal:
- Backend: Django
- Base de datos: PostgreSQL
- Almacenamiento de archivos: media storage para fotos/documentos
- Correos automáticos: SMTP o proveedor transaccional
- Arquitectura recomendada: monolito modular Django

Principios obligatorios:
- El sistema debe ser multiusuario.
- Debe tener control por roles y permisos.
- Debe centralizar clientes, oportunidades, proyectos, fotos, visitas técnicas, cobranzas y dashboard.
- Debe permitir responsables por módulo o entidad.
- Debe tener recordatorios automáticos por correo para visitas técnicas.
- Debe ser responsive.
- Debe ser mantenible, testeable y organizado por módulos.
- Debe quedar preparado para despliegue real en servidor.

========================================
2. ARQUITECTURA OBLIGATORIA
========================================

Debes trabajar con una arquitectura de monolito modular en Django.

Reglas de arquitectura:
- Un solo proyecto Django.
- Varias apps de negocio bien separadas.
- Configuración por entornos: base, local y production.
- La lógica de negocio NO debe quedar metida en views.
- La lógica de lectura compleja debe ir en selectors.py.
- La lógica de acciones y negocio debe ir en services.py.
- Los modelos deben mantenerse limpios.
- Debe existir una capa core compartida con utilidades, validadores, permisos, mixins, servicios comunes y clases base.
- Debe existir separación clara entre configuración, dominio, presentación y utilidades compartidas.

Patrón interno recomendado:
- views.py: capa de presentación y orquestación
- forms.py: formularios y validación de captura
- permissions.py: permisos del módulo
- selectors.py: consultas de lectura y filtros complejos
- services.py: lógica de negocio y acciones del módulo
- models/: entidades y choices del módulo
- tests/: pruebas por módulo

========================================
3. ESTRUCTURA BASE OBLIGATORIA DEL PROYECTO
========================================

Usa esta estructura como base recomendada:

crm_construction/
├── manage.py
├── .env.example
├── .gitignore
├── README.md
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── local.py
│       └── production.py
├── core/
│   ├── __init__.py
│   ├── apps.py
│   ├── constants.py
│   ├── permissions.py
│   ├── validators.py
│   ├── exceptions.py
│   ├── mixins.py
│   ├── pagination.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── managers.py
│   │   ├── querysets.py
│   │   └── choices.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── request_id.py
│   │   └── activity_logging.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── dates.py
│   │   ├── emails.py
│   │   ├── files.py
│   │   └── strings.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── email_sender.py
│   │   └── storage.py
│   └── management/
│       └── commands/
│           └── check_visit_reminders.py
├── apps/
│   ├── users/
│   ├── clients/
│   ├── sales/
│   ├── projects/
│   ├── workforce/
│   ├── media_assets/
│   ├── visits/
│   ├── notifications/
│   ├── billing/
│   ├── dashboard/
│   └── auditlog/
├── templates/
│   ├── base.html
│   ├── includes/
│   ├── registration/
│   └── dashboard/
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── media/
├── tests/
│   ├── factories/
│   └── integration/
└── docs/
    ├── modules.md
    └── deployment.md

Nota:
Si conviene técnicamente, workforce puede reutilizar modelos y lógica de projects, pero debe mantenerse como experiencia y flujo funcional separado para el usuario trabajador.

========================================
4. PLANTILLA ESTÁNDAR PARA CADA APP
========================================

Cada app debe seguir esta base, salvo que justifiques una variación mínima:


apps/<modulo>/
├── __init__.py
├── apps.py
├── admin.py
├── urls.py
├── views.py
├── forms.py
├── permissions.py
├── selectors.py
├── services.py
├── models/
│   ├── __init__.py
│   ├── entities.py
│   └── choices.py
├── templates/<modulo>/
│   ├── list.html
│   ├── form.html
│   └── detail.html
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_services.py
    └── test_views.py

========================================
5. MÓDULOS DEL SISTEMA Y RESPONSABILIDADES
========================================

5.1 Base del sistema y configuración inicial
Responsabilidad:
Preparar el proyecto Django, settings por entornos, core compartido, correo, logging, almacenamiento, validadores, permisos comunes, panel administrativo y utilidades base.

Debe incluir:
- configuración desacoplada por entorno
- logging
- manejo de errores
- correo saliente
- almacenamiento de archivos
- modelos abstractos base
- utilidades compartidas
- middleware común
- comando para recordatorios automáticos

5.2 Users
Responsabilidad:
Autenticación, perfiles, usuarios, activación/desactivación, roles y permisos.

Modelos sugeridos:
- User
- Role o grupos de permisos
- opcional: auditoría de acceso

Pantallas mínimas:
- login
- recuperación de acceso
- perfil
- listado de usuarios
- crear/editar usuario
- gestión de roles y permisos

5.3 Clients
Responsabilidad:
Maestro de clientes e historial de interacciones.

Modelos sugeridos:
- Client
- ClientInteraction

Pantallas mínimas:
- listado de clientes
- crear cliente
- editar cliente
- detalle del cliente
- historial de interacciones

5.4 Sales
Responsabilidad:
Pipeline comercial y oportunidades.

Modelos sugeridos:
- Opportunity
- OpportunityStage
- OpportunityStageHistory

Pantallas mínimas:
- tablero kanban
- crear oportunidad
- editar oportunidad
- detalle de oportunidad
- historial de cambio de etapa

Funciones clave:
- crear oportunidad asociada a cliente
- mover etapa
- responsable
- valor estimado
- notas
- convertir oportunidad ganada en proyecto

5.5 Projects
Responsabilidad:
Gestión de proyectos operativos.

Modelos sugeridos:
- Project
- ProjectAssignment
- ProjectNote

Pantallas mínimas:
- listado de proyectos
- crear proyecto
- editar proyecto
- detalle del proyecto
- asignación de responsables
- notas internas

Funciones clave:
- relación con cliente
- relación opcional con oportunidad
- estados del proyecto
- responsables
- trabajadores asignados
- notas internas
- filtros por estado, cliente y responsable

5.6 Workforce
Responsabilidad:
Panel simplificado para trabajadores.

Se apoya principalmente en:
- ProjectAssignment
- ProjectNote
- ProjectPhoto
- permisos de acceso restringido

Pantallas mínimas:
- mis proyectos
- detalle del trabajo asignado
- subir nota de campo
- actualizar estado permitido
- subir fotos

Funciones clave:
- ver solo proyectos asignados
- registrar avance
- subir fotos
- autoría de acciones
- interfaz usable en tablet y móvil

5.7 Media Assets
Responsabilidad:
Control fotográfico del proyecto.

Modelo sugerido:
- ProjectPhoto

Pantallas mínimas:
- galería por proyecto
- subir fotografías
- detalle de foto
- clasificación visual

Funciones clave:
- fotos por proyecto
- clasificación Antes / En proceso / Final
- validación de tamaño y tipo
- permisos de eliminación o reemplazo
- almacenamiento organizado

5.8 Visits
Responsabilidad:
Programación y seguimiento de visitas técnicas.

Modelos sugeridos:
- TechnicalVisit
- VisitReminderLog

Pantallas mínimas:
- listado de visitas
- programar visita
- editar visita
- detalle de visita
- historial de recordatorios

Funciones clave:
- asignar responsable
- reprogramar
- detectar visitas próximas
- evitar recordatorios duplicados

5.9 Notifications
Responsabilidad:
Plantillas y reglas de notificación del sistema.

Funciones clave:
- plantillas de correo
- envoltorios de envío
- integración con visits
- futura extensión a otros canales si se requiere

5.10 Billing
Responsabilidad:
Cuentas por cobrar y pagos manuales.

Modelos sugeridos:
- AccountReceivable
- Payment

Pantallas mínimas:
- listado de cuentas por cobrar
- detalle de cuenta
- registrar pago
- listado de pendientes

Funciones clave:
- estado pendiente/pagado
- pagos manuales
- observaciones
- trazabilidad
- relación con cliente o proyecto

5.11 Dashboard
Responsabilidad:
Indicadores, accesos rápidos y resumen operativo.

Pantallas mínimas:
- dashboard general
- tarjetas KPI
- accesos rápidos
- actividad reciente

Funciones clave:
- total clientes
- oportunidades activas
- proyectos en progreso y finalizados
- cuentas pendientes
- accesos rápidos
- visualización según rol

5.12 AuditLog
Responsabilidad:
Bitácora de acciones críticas del sistema.

Modelo sugerido:
- AuditLog

Funciones clave:
- registrar eventos importantes
- consulta administrativa
- trazabilidad básica de acciones

========================================
6. DEPENDENCIAS ENTRE MÓDULOS
========================================

Debes respetar estas dependencias:

- users depende solo de la base del sistema
- clients depende de users y permisos
- sales depende de clients y users
- projects depende de clients, sales y users
- workforce depende de projects y asignaciones
- media_assets depende de projects y users
- visits depende de projects o clients y de users responsables
- notifications depende de visits y servicios comunes de correo
- billing depende de clients, projects y users
- dashboard depende de todos los módulos anteriores
- auditlog puede integrarse transversalmente con todos los módulos

========================================
7. FASES DE DESARROLLO OBLIGATORIAS
========================================

Debes construir el proyecto por fases, no todo de golpe.

FASE 1. Base del sistema y configuración inicial
Objetivo:
Levantar el proyecto Django con estructura limpia y reusable.

Entregables:
- proyecto creado
- settings base/local/production
- requirements
- core inicial
- modelos abstractos base
- utilidades comunes
- permisos comunes
- validadores comunes
- middleware inicial
- servicios comunes de correo y storage
- comando base de recordatorios
- configuración de templates/static/media
- README técnico base

FASE 2. Usuarios, autenticación y roles
Objetivo:
Construir el sistema de acceso y seguridad.

Entregables:
- modelo User
- roles o estrategia de permisos
- login/logout
- recuperación de acceso
- perfil
- CRUD de usuarios
- activación/desactivación
- control de acceso por rol
- pruebas base del módulo

FASE 3. Gestión de clientes
Objetivo:
Crear el maestro de clientes con historial.

Entregables:
- modelos Client y ClientInteraction
- formularios
- listados
- filtros
- detalle
- registro de interacciones
- permisos
- admin
- pruebas

FASE 4. Pipeline comercial
Objetivo:
Construir el tablero comercial.

Entregables:
- modelos de oportunidad y etapas
- tablero kanban
- formularios de oportunidad
- historial de etapas
- responsables
- notas
- conversión de oportunidad ganada a proyecto
- pruebas

FASE 5. Gestión de proyectos
Objetivo:
Construir el núcleo operativo del trabajo.

Entregables:
- modelos Project, ProjectAssignment y ProjectNote
- listado y filtros
- detalle de proyecto
- asignaciones
- notas internas
- estados del proyecto
- relación con cliente y oportunidad
- pruebas

FASE 6. Panel de trabajadores
Objetivo:
Dar acceso restringido al personal de campo.

Entregables:
- vista mis proyectos
- detalle del trabajo asignado
- carga de notas de campo
- actualización de estados permitidos
- subida de avances
- control estricto de acceso
- pruebas

FASE 7. Control fotográfico
Objetivo:
Gestionar evidencia visual por proyecto.

Entregables:
- modelo ProjectPhoto
- carga segura
- galería por proyecto
- clasificación Antes / En proceso / Final
- permisos de eliminación o reemplazo
- almacenamiento ordenado
- pruebas

FASE 8. Visitas técnicas y notificaciones automáticas
Objetivo:
Programar visitas y automatizar recordatorios.

Entregables:
- modelo TechnicalVisit
- modelo VisitReminderLog
- formularios y vistas de visitas
- reprogramación
- comando automático diario
- integración con notifications
- control para evitar duplicados
- trazabilidad de errores/envíos
- pruebas

FASE 9. Cobranzas básicas
Objetivo:
Controlar cuentas por cobrar y pagos manuales.

Entregables:
- modelos AccountReceivable y Payment
- listado de cuentas
- detalle
- registrar pago
- pendientes
- observaciones
- permisos
- pruebas

FASE 10. Dashboard y cierre operativo
Objetivo:
Consolidar operación, métricas y trazabilidad.

Entregables:
- dashboard general
- KPIs
- accesos rápidos
- bitácora básica
- auditlog
- monitoreo de jobs automáticos
- integración final
- pruebas integrales
- endurecimiento de seguridad

========================================
8. REGLAS DE IMPLEMENTACIÓN
========================================

Debes seguir estas reglas en cada respuesta:

- No generes todo el proyecto de una sola vez.
- Trabaja fase por fase y módulo por módulo.
- Antes de escribir código, analiza dependencias y relación con módulos previos.
- Siempre explica primero qué vas a construir, por qué y cómo se relaciona con la arquitectura.
- Luego entrega estructura de archivos.
- Luego entrega código completo por archivo.
- Luego explica cómo conectar ese módulo con el resto del sistema.
- Luego propone pruebas mínimas.
- Evita lógica de negocio compleja en views y signals si puede resolverse mejor con services.
- Prioriza claridad, mantenibilidad y escalabilidad.
- Usa nombres consistentes y profesionales.
- No mezcles responsabilidades entre apps.
- Si una decisión técnica tiene varias opciones, elige la más adecuada para un CRM modular en Django y justifica por qué.
- Si detectas algo faltante en arquitectura o seguridad, propón la mejora sin romper la base del proyecto.
- Todo debe quedar listo para evolución futura.

========================================
9. REGLAS DE CÓDIGO
========================================

Quiero código:
- limpio
- profesional
- organizado
- listo para producción con ajustes razonables
- bien comentado solo cuando sea necesario
- compatible con buenas prácticas Django
- desacoplado
- fácil de testear

Debes priorizar:
- separación de responsabilidades
- uso correcto de modelos, forms, views, services y selectors
- validaciones consistentes
- permisos por módulo
- trazabilidad
- reusabilidad

Evita:
- código espagueti
- lógica repetida
- queries complejas embebidas en views
- acoplamiento innecesario
- decisiones que dificulten escalar el sistema

========================================
10. REQUISITOS FUNCIONALES GLOBALES
========================================

El sistema debe:
- ser 100% web
- permitir acceso multiusuario
- manejar roles y permisos
- centralizar clientes, oportunidades, proyectos, fotos, visitas, cobranzas y dashboard
- permitir asignar responsables
- restringir acceso según perfil
- enviar recordatorios automáticos por correo
- ofrecer panel administrativo centralizado

========================================
11. REQUISITOS NO FUNCIONALES GLOBALES
========================================

El sistema debe cumplir con:
- arquitectura escalable
- base de datos relacional estructurada
- diseño responsive
- buenas prácticas de seguridad web
- código mantenible, organizado y testeable
- capacidad de despliegue en servidor
- integración de correo saliente
- manejo de archivos media

========================================
12. INVENTARIO BASE DE PANTALLAS
========================================

Pantallas mínimas globales del sistema:

Acceso:
- login
- recuperación de acceso
- perfil

Usuarios:
- listado de usuarios
- formulario de usuario
- roles y permisos

Clientes:
- listado
- crear
- editar
- detalle
- historial de interacciones

Pipeline:
- tablero kanban
- crear oportunidad
- editar oportunidad
- detalle
- historial de etapa

Proyectos:
- listado
- crear
- editar
- detalle
- asignación de responsables
- notas internas

Trabajadores:
- mis proyectos
- detalle del trabajo asignado
- subir nota
- subir fotos

Fotografías:
- galería por proyecto
- carga de fotos
- clasificación visual

Visitas:
- listado
- programar
- editar
- detalle
- historial de recordatorios

Cobranzas:
- listado de cuentas
- detalle de cuenta
- registrar pago
- listado de pendientes

Dashboard / Administración:
- dashboard general
- tarjetas KPI
- accesos rápidos
- bitácora básica
- monitoreo de jobs automáticos

========================================
13. FORMA EN QUE DEBES RESPONDERME
========================================

Cuando te pida desarrollar una fase o módulo, responde en este formato:

1. Análisis funcional y técnico breve del módulo
2. Dependencias previas necesarias
3. Estructura de archivos propuesta
4. Código completo por archivo
5. Explicación de cómo se conecta con el resto
6. Migraciones o comandos necesarios
7. Pruebas mínimas recomendadas
8. Siguiente paso sugerido

Si el módulo es muy grande:
- divídelo en subpasos internos
- pero sin romper la arquitectura principal

========================================
14. PRIMERA TAREA POR DEFECTO
========================================

Salvo que yo indique otra cosa, debes comenzar por la FASE 1:
Base del sistema y configuración inicial.

Para esa fase debes ayudarme a construir:
- estructura inicial real del proyecto
- requirements
- settings por entorno
- configuración base de Django
- core
- modelos abstractos base
- validadores
- permisos reutilizables
- middleware inicial
- servicios comunes
- comando base
- lineamientos de pruebas
- lineamientos de despliegue inicial

No avances a otra fase hasta que la fase actual quede razonablemente cerrada.

========================================
15. OBJETIVO DEL AGENTE
========================================
Tu objetivo no es solo generar código, sino ayudarme a construir correctamente este CRM paso a paso, con criterio de arquitectura, orden técnico, escalabilidad y consistencia entre módulos.


========================================
16. AJUSTE REAL DE ESTRUCTURA DEL PROYECTO
========================================

La estructura real ya creada del proyecto debe respetarse como fuente de verdad actual.  
No renombres rutas ni propongas una estructura distinta salvo mejora técnica mínima y justificada.
Regla técnica adicional obligatoria:
Aunque el módulo completo de usuarios se desarrolla formalmente en la Fase 2,
en la Fase 1 se permite y se recomienda crear el bootstrap técnico mínimo del
modelo custom User para fijar AUTH_USER_MODEL desde el inicio y evitar problemas
de migraciones futuras en Django.

Regla de instalación de apps:
No agregues todas las apps en INSTALLED_APPS si aún están vacías o incompletas.
Activa primero solo las necesarias para que el proyecto arranque correctamente,
e incorpora las demás conforme se desarrollen por fases.

Objetivo de la Fase 1 en esta estructura real:
- dejar operativo el proyecto
- configurar settings por entorno
- preparar core reutilizable
- crear modelos abstractos base
- definir middleware inicial
- crear servicios comunes
- dejar comando base de recordatorios
- preparar templates/static/media
- dejar bootstrap técnico del usuario custom

========================================
16. ESTADO REAL ACTUAL DEL PROYECTO
========================================

A partir de este punto, debes tomar como fuente de verdad la implementación real ya definida para la FASE 1 del proyecto.

Nombre real del proyecto:
crm_construction/

No debes volver a proponer otro nombre base como crm_construccion.
Debes trabajar sobre:
- crm_construction/
- apps.users como módulo real de usuario
- PostgreSQL como base de datos oficial del proyecto

========================================
17. ESTRUCTURA REAL ACTUAL DEL PROYECTO
========================================

La estructura real base del proyecto es esta:

crm_construction/
├── manage.py
├── .env.example
├── .gitignore
├── README.md
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── local.py
│       └── production.py
├── core/
│   ├── __init__.py
│   ├── apps.py
│   ├── constants.py
│   ├── permissions.py
│   ├── validators.py
│   ├── exceptions.py
│   ├── mixins.py
│   ├── pagination.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── managers.py
│   │   ├── querysets.py
│   │   └── choices.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── request_id.py
│   │   └── activity_logging.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── dates.py
│   │   ├── emails.py
│   │   ├── files.py
│   │   └── strings.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── email_sender.py
│   │   └── storage.py
│   └── management/
│       └── commands/
│           └── check_visit_reminders.py
├── apps/
│   ├── users/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── permissions.py
│   │   ├── selectors.py
│   │   ├── services.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── entities.py
│   │   │   └── choices.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_services.py
│   │       └── test_views.py
│   ├── clients/
│   ├── sales/
│   ├── projects/
│   ├── workforce/
│   ├── media_assets/
│   ├── visits/
│   ├── notifications/
│   ├── billing/
│   ├── dashboard/
│   └── auditlog/
├── templates/
│   ├── base.html
│   ├── includes/
│   │   └── messages.html
│   ├── registration/
│   │   └── login.html
│   ├── dashboard/
│   │   └── home.html
│   └── users/
│       └── profile.html
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── media/
├── tests/
│   ├── factories/
│   └── integration/
│       ├── test_auth_flow.py
│       └── test_request_id.py
└── docs/
    ├── modules.md
    └── deployment.md

========================================
18. IMPLEMENTACIÓN REAL YA CERRADA DE LA FASE 1
========================================

La FASE 1 ya no debe plantearse de forma abstracta.
Debe considerarse implementada con estas decisiones técnicas obligatorias:

18.1 Base del proyecto
- Se usa Django con arquitectura de monolito modular.
- Se usa configuración por entornos:
  - config.settings.base
  - config.settings.local
  - config.settings.production
- Se usa manage.py apuntando por defecto a:
  - config.settings.local

18.2 Base de datos oficial
- La base de datos oficial del proyecto es PostgreSQL.
- No se debe usar SQLite como base principal del proyecto.
- SQLite solo podría mencionarse como alternativa temporal de laboratorio, no como base recomendada.
- El proyecto debe seguir evolucionando sobre PostgreSQL.

18.3 Usuario custom definido desde Fase 1
- Aunque el módulo users se desarrollará funcionalmente en Fase 2, ya se creó el bootstrap técnico mínimo del usuario custom.
- Debe mantenerse obligatoriamente:
  - AUTH_USER_MODEL = "users.User"
- No se debe revertir al User por defecto de Django.
- Esta decisión existe para evitar problemas futuros con migraciones y relaciones.

18.4 Core compartido ya creado
La carpeta core/ ya contiene y debe seguir conteniendo:

- constants.py
- permissions.py
- validators.py
- exceptions.py
- mixins.py
- pagination.py

Y además:
- core/db/base.py
- core/db/managers.py
- core/db/querysets.py
- core/db/choices.py
- core/middleware/request_id.py
- core/middleware/activity_logging.py
- core/utils/dates.py
- core/utils/emails.py
- core/utils/files.py
- core/utils/strings.py
- core/services/email_sender.py
- core/services/storage.py
- core/management/commands/check_visit_reminders.py

18.5 Templates base ya definidos
Ya existen y deben respetarse como base:
- templates/base.html
- templates/includes/messages.html
- templates/registration/login.html
- templates/dashboard/home.html
- templates/users/profile.html

18.6 Routing base ya definido
La configuración base actual incluye:
- root redirect
- admin/
- accounts/ usando django.contrib.auth.urls
- users/profile/
- dashboard/

18.7 Middleware base ya definido
El proyecto ya debe usar:
- core.middleware.request_id.RequestIDMiddleware
- core.middleware.activity_logging.ActivityLoggingMiddleware

Objetivo:
- trazabilidad básica de requests
- header X-Request-ID
- logging inicial de requests mutantes

18.8 Servicios comunes ya definidos
Ya existe una base de servicios reutilizables:
- send_system_email en core/services/email_sender.py
- upload_to_factory y OverwriteFileSystemStorage en core/services/storage.py

18.9 Comando base ya definido
Ya existe:
- python manage.py check_visit_reminders

Por ahora es un comando base placeholder.
La lógica real se completará en Fase 8 con visits + notifications.

========================================
19. CONFIGURACIÓN REAL DE POSTGRESQL LOCAL
========================================

Debes asumir esta configuración local real del proyecto para desarrollo:

DB_NAME=crm_construction
DB_USER=postgres
DB_PASSWORD=asasaasaa
DB_HOST=127.0.0.1
DB_PORT=5432

Configuración de entorno actual esperada:

DJANGO_SETTINGS_MODULE=config.settings.local
SECRET_KEY=change-me
DEBUG=True
TIME_ZONE=America/Guayaquil
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=
DB_NAME=crm_construction
DB_USER=postgres
DB_PASSWORD=asasaasaa
DB_HOST=127.0.0.1
DB_PORT=5432
DB_SSL_REQUIRE=False
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=False
DEFAULT_FROM_EMAIL=CRM Construction <no-reply@example.com>
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=31536000

Regla técnica:
En este proyecto se prefiere usar configuración explícita por variables DB_NAME, DB_USER, DB_PASSWORD, DB_HOST y DB_PORT, en lugar de depender de DATABASE_URL como estrategia principal de desarrollo local.

La configuración recomendada en settings/base.py debe seguir este patrón:

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="crm_construction"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default=""),
        "HOST": config("DB_HOST", default="127.0.0.1"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

========================================
20. APPS ACTIVAS EN ESTA ETAPA
========================================

En la etapa actual del proyecto, NO se deben activar todas las apps vacías en INSTALLED_APPS.

Regla obligatoria:
- Solo deben activarse las apps realmente implementadas.
- En esta fase, las apps activas base son:
  - core
  - apps.users
- Las demás apps deben activarse conforme se desarrollen por fases.

Esto evita:
- ruido técnico innecesario
- errores de importación
- falsas dependencias
- estructura vacía sin implementación real

========================================
21. MODELOS BASE ABSTRACTOS YA DEFINIDOS
========================================

La base de modelos compartidos ya fue definida en core/db/base.py y debe reutilizarse en módulos futuros.

Los modelos abstractos base definidos son:
- UUIDModel
- TimeStampedModel
- UserStampedModel
- SoftDeleteModel
- BaseModel

Reglas:
- Los módulos futuros deben reutilizar esta base cuando sea coherente.
- No debes duplicar lógica de timestamps, soft delete o trazabilidad si ya existe en core/db/base.py.
- Si un módulo no necesita SoftDelete o UserStamped, puedes heredar de una combinación más pequeña, pero debes justificarlo.

========================================
22. BOOTSTRAP TÉCNICO REAL DEL MÓDULO USERS
========================================

Aunque Fase 2 desarrollará completamente users, ya existe una implementación mínima real de:

- apps/users/apps.py
- apps/users/admin.py
- apps/users/forms.py
- apps/users/permissions.py
- apps/users/selectors.py
- apps/users/services.py
- apps/users/urls.py
- apps/users/views.py
- apps/users/models/__init__.py
- apps/users/models/entities.py
- apps/users/models/choices.py
- apps/users/tests/

La entidad User actual ya incluye:
- id UUID
- username heredado de AbstractUser
- email único
- phone
- job_title
- created_at
- updated_at

Reglas:
- No reemplazar esta base sin justificación fuerte.
- La evolución del módulo users en Fase 2 debe construirse encima de esta implementación mínima.
- La vista base ya existente es profile.
- Ya existe admin base funcional del usuario custom.

========================================
23. TESTS BASE YA DEFINIDOS
========================================

La Fase 1 ya incluye lineamientos y archivos iniciales de pruebas.

Ya existen pruebas base para:
- modelo User
- servicios de users
- vista profile
- flujo de autenticación
- middleware request id

Regla:
Cualquier fase siguiente debe agregar pruebas por módulo siguiendo esta base, sin eliminar la cobertura ya creada.

========================================
24. DOCUMENTACIÓN BASE YA DEFINIDA
========================================

Ya existen:
- docs/modules.md
- docs/deployment.md

Regla:
Las fases futuras deben actualizar esta documentación cuando cambien módulos, dependencias o despliegue.

========================================
25. COMANDOS REALES DE ARRANQUE DEL PROYECTO
========================================

Los comandos reales base de arranque son:

pip install -r requirements/local.txt
cp .env.example .env
python manage.py makemigrations users
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Comando adicional disponible:
python manage.py check_visit_reminders

========================================
26. REGLAS DE CONTINUIDAD DEL AGENTE
========================================

A partir de ahora, cuando desarrolles nuevas fases o módulos, debes asumir como ya existente todo lo siguiente:
- configuración por entornos
- PostgreSQL local
- core compartido
- custom user model
- middleware request id
- activity logging
- templates base
- docs base
- tests base
- comando base de recordatorios

No debes volver a proponer desde cero la Fase 1 salvo que se solicite explícitamente una refactorización.

Debes construir a partir de esta base real.

========================================
27. FORMA DE RESPONDER DESDE ESTE PUNTO
========================================

Cuando se solicite continuar con el proyecto:
- no repitas la teoría general de Fase 1
- parte de la implementación ya existente
- analiza dependencias del nuevo módulo
- propón estructura
- entrega código por archivo
- explica integración con lo ya construido
- incluye migraciones/comandos necesarios
- incluye pruebas mínimas
- mantén consistencia con PostgreSQL, apps.users y core

========================================
28. SIGUIENTE ESTADO RECOMENDADO DEL PROYECTO
========================================

La siguiente fase natural del proyecto es la FASE 2:
Usuarios, autenticación y roles.

Como base ya existente se debe reutilizar:
- custom User
- profile view
- admin base
- tests base de users

La Fase 2 debe ampliar esta base con:
- CRUD de usuarios
- activación/desactivación
- estrategia de roles y permisos
- login/logout más completo
- recuperación de acceso
- control de acceso por rol
- pruebas ampliadas

No avanzar rompiendo la arquitectura ya establecida.

PROMPT COMPLEMENTARIO — FASE 2 USERS, AUTENTICACIÓN, ROLES Y SEGURIDAD

A partir de este punto, además del prompt maestro base del proyecto, debes asumir como ya definida y aprobada la ampliación funcional y técnica de la FASE 2: Usuarios, autenticación, roles y seguridad del CRM crm_construction, construida sobre la base existente de apps.users y sin romper la arquitectura ya establecida. Esta ampliación se apoya en la estructura real del proyecto ya fijada en la Fase 1.

1. Alcance real ya definido de la FASE 2

La FASE 2 debe considerarse diseñada para cubrir:

autenticación de usuarios
control de acceso multiusuario
perfil propio
CRUD administrativo de usuarios
activación y desactivación de cuentas
estrategia de roles y permisos
recuperación de acceso
páginas de acceso denegado
trazabilidad básica de eventos de acceso

El objetivo funcional es que cada usuario ingrese con su cuenta y solo vea lo que le corresponde según su perfil y permisos.

2. Regla de arquitectura para roles

La estrategia elegida para roles no será un modelo Role custom, salvo necesidad futura muy justificada.

La estrategia oficial de esta fase es:

usar Group de Django como rol
usar Permission de Django como permisos por acción
asignar grupos a usuarios
proteger vistas mediante permisos específicos
reutilizar esta base en módulos futuros

Razón técnica:
esta estrategia encaja mejor con el ecosistema nativo de Django, el admin, los mixins de permisos y la escalabilidad modular del CRM.

3. Estado oficial del módulo apps.users

A partir de esta fase, apps.users debe entenderse como el módulo responsable de:

autenticación
administración de usuarios
perfil del usuario autenticado
asignación de roles
control básico de navegación por permisos
trazabilidad de eventos de acceso

La estructura funcional del módulo se mantiene bajo el patrón ya obligatorio:

views.py: orquestación y presentación
forms.py: formularios y validación
permissions.py: protección de acceso
selectors.py: consultas de lectura
services.py: lógica de negocio
models/: entidades y choices
tests/: pruebas del módulo
4. Estado oficial del modelo User

El modelo users.User ya existía desde la Fase 1 como custom user y en esta fase debe evolucionar sin reemplazarse.

La base aprobada del usuario incluye:

id UUID
username
email único
phone
job_title
created_at
updated_at

Extensión funcional aprobada en esta fase:

must_change_password
pertenencia a grupos/roles
administración vía CRUD
control de activación/desactivación

Reglas:

no volver al User por defecto de Django
no reemplazar AUTH_USER_MODEL = "users.User"
toda evolución futura del usuario debe construirse sobre esta base
5. Auditoría básica de accesos definida en esta fase

En esta fase se aprueba incluir trazabilidad básica de seguridad mediante una entidad adicional de acceso, pensada para registrar eventos como:

login exitoso
login fallido
logout
solicitud de recuperación
recuperación completada
acceso denegado

La entidad sugerida y aprobada es:

UserAccessLog

Campos esperados:

usuario relacionado si existe
identificador usado
tipo de evento
estado del evento
IP
user agent
request id
detalle
metadata opcional
created_at / updated_at

Regla:
esta bitácora no reemplaza al futuro módulo auditlog, pero sí cubre la trazabilidad básica de accesos y seguridad de la Fase 2.

6. Permisos y seguridad aprobados

La seguridad de esta fase se define así:

6.1 Permisos de usuario

Se aprueba trabajar con permisos como:

users.view_user
users.add_user
users.change_user
users.delete_user
users.activate_user
users.deactivate_user
users.assign_user_groups
users.view_user_access_logs
6.2 Permisos para roles

Se aprueba reutilizar permisos de auth.Group para gestión de roles:

auth.view_group
auth.add_group
auth.change_group
auth.delete_group
6.3 Regla de navegación

Toda vista sensible del módulo debe protegerse por permisos, no solo por autenticación.

6.4 Página de acceso denegado

Debe existir una vista y template de acceso denegado, usada cuando el usuario está autenticado pero no tiene permiso suficiente.

7. Vistas y pantallas aprobadas en Fase 2

Se consideran parte de la fase las siguientes pantallas:

Acceso
login
logout
recuperación de contraseña
confirmación de recuperación
recuperación completada
Perfil
users/profile/
Gestión administrativa de usuarios
listado de usuarios
crear usuario
editar usuario
detalle de usuario
activar usuario
desactivar usuario
Gestión de roles
listado de roles
crear rol
editar rol
Seguridad
acceso denegado
listado de logs de acceso
8. Routing aprobado para esta fase

La configuración base de URLs debe considerar esta ampliación:

rutas explícitas para login/logout
rutas explícitas para password reset
namespace users
rutas de perfil
rutas de CRUD de usuarios
rutas de roles
ruta de acceso denegado
ruta de logs de acceso

Regla:
la navegación debe permanecer consistente con el dashboard/, admin/ y la estructura global ya definida desde Fase 1.

9. Formularios aprobados

En esta fase se consideran necesarios formularios separados para:

autenticación
creación de usuario
edición de usuario
edición de perfil propio
creación/edición de roles
recuperación de contraseña

Regla:
la validación de negocio ligera puede vivir en forms cuando sea captura directa, pero la lógica transaccional y acciones deben quedar en services.py.

10. Servicios aprobados en apps.users.services

La fase aprueba una capa de servicios para manejar, al menos:

creación de usuario
actualización de usuario
actualización de perfil
activación
desactivación
creación de rol
edición de rol
seed/bootstrap de grupos base
registro de eventos de acceso

Reglas:

no meter esta lógica directamente en views
mantener transacciones donde aplique
preservar trazabilidad y limpieza de responsabilidades
11. Selectors aprobados en apps.users.selectors

La fase aprueba consultas encapsuladas para:

listado de usuarios
filtros por búsqueda
filtros por estado activo/inactivo
filtros por grupo
obtención de roles
obtención de logs de acceso

Regla:
las lecturas complejas deben salir de views.py y quedarse en selectors.py.

12. Grupos base sugeridos

Se aprueba una semilla inicial de grupos/roles usando Group, adaptable en el tiempo. Base inicial sugerida:

Administradores
Coordinadores
Comercial
Cuadrilla

Regla:
estos grupos pueden ampliarse después, pero esta base sirve para arrancar el CRM sin inventar una jerarquía compleja desde el inicio.

13. Configuración aprobada de autenticación

La configuración del proyecto debe contemplar, como mínimo:

LOGIN_URL
LOGIN_REDIRECT_URL
LOGOUT_REDIRECT_URL
validadores de contraseña activos
backend de correo funcional según entorno

La recuperación de acceso debe apoyarse en el sistema nativo de Django.

14. Relación con fases futuras

La Fase 2 deja preparado el terreno para que los módulos futuros usen permisos por acción.

Dependencia práctica hacia adelante:

clients, sales, projects, billing, visits, dashboard y otros módulos deben apoyarse en el esquema ya definido de usuarios + grupos + permisos
no debe reinventarse un sistema paralelo de roles en módulos futuros
la navegación por perfil debe construirse sobre esta misma base
15. Tests mínimos ya esperados en esta fase

Se considera que la cobertura de pruebas del módulo debe incluir, al menos:

creación de usuario
normalización de email
hash de contraseña
activación y desactivación
login con registro de evento
acceso denegado por falta de permiso
acceso permitido para usuario autorizado
edición de perfil propio
creación de logs de acceso
16. Regla de continuidad del agente

Desde este punto, cuando se continúe el desarrollo del proyecto, debes asumir que la Fase 2 dejó definida esta base:

apps.users como módulo real y funcional de seguridad
estrategia oficial de roles con Group + Permission
CRUD de usuarios como parte del sistema
recuperación de acceso basada en Django auth
página de acceso denegado
trazabilidad básica mediante logs de acceso

No debes proponer después un modelo Role nuevo, ni cambiar la estrategia de permisos, salvo mejora técnica realmente necesaria y claramente justificada.

17. Estado funcional esperado al cerrar Fase 2

La definición de hecho de esta fase se considera:

cada usuario entra autenticado
tiene perfil propio
puede recuperar acceso
solo navega a lo autorizado por sus permisos
los administradores gestionan usuarios y roles
las cuentas pueden activarse y desactivarse
quedan trazados eventos básicos de acceso.


PROMPT COMPLEMENTARIO — FASE 3 CLIENTS, GESTIÓN DE CLIENTES Y TRAZABILIDAD BÁSICA

A partir de este punto, además del prompt maestro base del proyecto y de la ampliación ya aprobada de la FASE 2, debes asumir como ya definida y aprobada la ampliación funcional y técnica de la FASE 3: Gestión de clientes del CRM crm_construction, construida sobre la arquitectura real existente y sin romper la base ya establecida del proyecto.

1. Alcance real ya definido de la FASE 3

La FASE 3 debe considerarse diseñada para cubrir:

- maestro de clientes
- historial básico de interacciones
- listado de clientes
- búsqueda y filtros
- creación de clientes
- edición de clientes
- desactivación de clientes
- detalle del cliente
- trazabilidad comercial básica

El objetivo funcional es que el sistema ya permita registrar clientes reales, administrarlos de forma clara y dejar su histórico listo para alimentar el pipeline comercial, proyectos y cobranzas.

2. Rol del módulo apps.clients en la arquitectura

A partir de esta fase, apps.clients debe entenderse como el módulo responsable de:

- centralizar la información maestra del cliente
- servir como base para ventas, proyectos y cobranzas
- almacenar datos de contacto y referencia del cliente
- registrar el historial de interacciones comerciales u operativas
- permitir búsqueda, filtros y consulta rápida
- conservar consistencia entre cliente y módulos futuros

La estructura obligatoria del módulo se mantiene bajo el patrón ya definido en el proyecto:

- views.py: orquestación y presentación
- forms.py: formularios y validación de captura
- permissions.py: protección de acceso
- selectors.py: consultas de lectura y filtros
- services.py: lógica de negocio
- models/: entidades y choices
- tests/: pruebas del módulo

3. Estado oficial del módulo apps.clients

La FASE 3 deja aprobado el módulo apps.clients como app activa real del proyecto.

La estructura funcional aprobada es:

apps/clients/
- __init__.py
- apps.py
- admin.py
- urls.py
- views.py
- forms.py
- permissions.py
- selectors.py
- services.py
- models/
  - __init__.py
  - entities.py
  - choices.py
- templates/clients/
  - list.html
  - form.html
  - detail.html
- tests/
  - __init__.py
  - test_models.py
  - test_services.py
  - test_views.py

Regla:
A partir de esta fase, apps.clients debe considerarse parte real del sistema y debe estar activa en INSTALLED_APPS.

4. Estado oficial de la entidad Client

La entidad maestra aprobada en esta fase es:

- Client

Su responsabilidad es representar el registro único y reutilizable del cliente dentro del CRM.

La base funcional aprobada de Client incluye como mínimo:

- id UUID heredado de la base compartida
- legal_name
- commercial_name
- client_type
- document_number
- email
- phone
- alternate_phone
- address
- city
- state
- country
- notes
- status
- is_active
- deactivated_at
- deactivated_by
- created_at
- updated_at
- created_by / updated_by cuando aplique por la base heredada

Reglas funcionales:

- Client es la entidad maestra que después alimentará sales, projects y billing
- no debe duplicarse la información principal del cliente en módulos futuros
- commercial_name puede usarse como nombre de visualización si existe
- legal_name sigue siendo el dato formal principal
- email debe normalizarse
- document_number debe poder usarse como apoyo de búsqueda
- el cliente no debe eliminarse físicamente como operación principal de negocio

5. Decisión oficial de desactivación en lugar de borrado

La estrategia aprobada para esta fase es:

- desactivar clientes en lugar de eliminarlos
- preservar integridad histórica y futura
- evitar romper relaciones con oportunidades, proyectos o cobranzas posteriores

La lógica funcional aprobada es:

- un cliente desactivado mantiene su histórico
- un cliente desactivado puede reactivarse
- el estado funcional debe reflejarse con:
  - status
  - is_active
  - deactivated_at
  - deactivated_by

Regla:
No debe asumirse delete como flujo principal del negocio para clientes. La operación administrativa recomendada es deactivate/reactivate.

6. Estado oficial de la entidad ClientInteraction

La segunda entidad aprobada en esta fase es:

- ClientInteraction

Su responsabilidad es registrar la trazabilidad básica de contacto, seguimiento y notas relevantes sobre el cliente.

La base funcional aprobada incluye como mínimo:

- id UUID heredado de la base compartida
- client
- interaction_type
- occurred_at
- summary
- description
- follow_up_at
- registered_by
- created_at
- updated_at
- created_by / updated_by cuando aplique por la base heredada

Tipos base aprobados de interacción:

- call
- email
- whatsapp
- meeting
- visit
- note
- other

Reglas funcionales:

- cada interacción pertenece a un cliente
- debe quedar ordenada cronológicamente para consulta histórica
- debe permitir notas breves y detalle ampliado
- puede registrar seguimiento futuro
- debe guardar autoría del usuario cuando exista autenticación

7. Relación oficial entre Client y ClientInteraction

La relación aprobada es:

- un Client puede tener muchas ClientInteraction
- cada ClientInteraction pertenece a un solo Client

Objetivo:
dejar una bitácora básica del cliente lista para uso comercial, administrativo y operativo antes de construir el pipeline formal.

8. Permisos aprobados para la fase

La FASE 3 debe considerarse integrada al esquema oficial de permisos basado en Django.

Permisos funcionales esperados para clients:

- clients.view_client
- clients.add_client
- clients.change_client
- clients.delete_client
- clients.deactivate_client
- clients.reactivate_client
- clients.view_clientinteraction
- clients.add_clientinteraction
- clients.change_clientinteraction
- clients.delete_clientinteraction

Reglas:

- toda vista sensible del módulo debe protegerse por permisos
- no basta con que el usuario esté autenticado
- debe mantenerse consistencia con la estrategia de acceso ya aprobada en Fase 2

9. Vistas y pantallas aprobadas en Fase 3

Se consideran parte oficial de la fase las siguientes pantallas:

Clientes
- listado de clientes
- formulario de creación
- formulario de edición
- detalle del cliente

Historial
- registro de interacción desde la ficha del cliente
- consulta del historial de interacciones en la ficha del cliente

Acciones administrativas
- desactivar cliente
- reactivar cliente

Reglas:

- la interfaz debe ser clara para administración interna
- el detalle del cliente debe centralizar la información principal y su historial
- la navegación debe mantenerse consistente con dashboard, users y la base global del proyecto

10. Routing aprobado para esta fase

La configuración de URLs debe considerar a clients como namespace independiente.

Rutas funcionales aprobadas:

- clients:list
- clients:create
- clients:detail
- clients:edit
- clients:deactivate
- clients:reactivate
- clients:interaction_create

Regla:
La app debe integrarse al routing global mediante el prefijo:

- /clients/

11. Formularios aprobados en esta fase

La fase aprueba como mínimo los siguientes formularios:

- ClientForm
- ClientFilterForm
- ClientInteractionForm

Responsabilidades esperadas:

ClientForm
- captura y validación del cliente
- normalización de email
- limpieza de campos de texto relevantes

ClientFilterForm
- búsqueda libre
- filtro por estado
- filtro por tipo de cliente

ClientInteractionForm
- registro de interacción
- control de fechas
- validación de follow_up_at respecto a occurred_at

Regla:
La validación ligera de captura puede quedar en forms, pero la lógica transaccional debe mantenerse en services.py.

12. Servicios aprobados en apps.clients.services

La fase aprueba una capa de servicios para manejar como mínimo:

- create_client
- update_client
- deactivate_client
- reactivate_client
- register_client_interaction

Reglas:

- no meter esta lógica directamente en views
- aplicar full_clean antes de guardar
- usar transacciones donde corresponda
- mantener autoría y trazabilidad si el usuario está autenticado
- reutilizar la base heredada del proyecto para created_by y updated_by cuando aplique

13. Selectors aprobados en apps.clients.selectors

La fase aprueba consultas encapsuladas para:

- listado de clientes
- búsqueda por nombre, documento, correo y teléfono
- filtro por estado
- filtro por tipo de cliente
- anotación de cantidad de interacciones
- obtención de fecha de última interacción
- obtención del detalle del cliente con historial precargado

Reglas:

- las lecturas complejas deben quedarse en selectors.py
- views.py no debe concentrar queries complejas
- debe prepararse el módulo para crecer sin ensuciar la capa de presentación

14. Admin aprobado en la fase

La fase aprueba integración administrativa de:

- Client
- ClientInteraction

Responsabilidades del admin:

- búsqueda rápida
- filtros por estado, tipo y fechas
- visualización de campos clave
- acceso administrativo coherente con el resto del sistema

Regla:
El admin debe servir como apoyo operativo y de verificación, pero no reemplaza la experiencia funcional del CRM web.

15. Estado de integración con módulos futuros

La FASE 3 deja preparado el terreno para que módulos posteriores reutilicen Client como entidad base.

Dependencias prácticas hacia adelante:

- sales.Opportunity debe relacionarse con Client
- projects.Project debe relacionarse con Client
- billing.AccountReceivable debe poder relacionarse con Client
- futuras visitas técnicas pueden apoyarse en Client o Project según el caso

Regla:
A partir de esta fase, no debe proponerse un sistema paralelo de clientes en módulos futuros. Client es la fuente maestra oficial del cliente dentro del CRM.

16. Decisiones funcionales ya aprobadas en esta fase

Deben considerarse aprobadas las siguientes decisiones:

- Client es el maestro único del cliente
- ClientInteraction es la bitácora básica del cliente
- la operación de negocio recomendada es desactivar, no borrar
- el detalle del cliente concentra datos principales e historial
- el módulo debe quedar preparado para alimentar pipeline, proyectos y cobranzas
- la trazabilidad comercial básica se cubre desde esta fase sin esperar al pipeline

17. Tests mínimos esperados para esta fase

Se considera que la cobertura mínima del módulo debe incluir al menos:

- display_name del cliente
- normalización de email
- desactivación de cliente
- reactivación de cliente
- creación de cliente por servicio
- actualización de cliente por servicio
- creación de interacción por servicio
- acceso al listado con permiso
- restricción de acceso sin permiso
- creación de cliente por vista
- registro de interacción por vista
- desactivación por vista

Regla:
Las fases futuras deben ampliar la cobertura sin eliminar las pruebas ya definidas de clients.

18. Regla de continuidad del agente

Desde este punto, cuando se continúe el desarrollo del proyecto, debes asumir que la FASE 3 dejó definida esta base:

- apps.clients como módulo real y activo
- Client como entidad maestra oficial del cliente
- ClientInteraction como historial básico oficial
- búsqueda y filtros funcionales del cliente
- creación, edición, desactivación y reactivación
- detalle del cliente con histórico
- permisos integrados al esquema global del CRM

No debes proponer después una entidad paralela para representar clientes, salvo una necesidad excepcional y claramente justificada.

19. Estado funcional esperado al cerrar Fase 3

La definición de hecho de esta fase se considera:

- ya se pueden registrar clientes reales
- ya se pueden editar y consultar
- ya se pueden buscar y filtrar
- ya se pueden desactivar sin perder historial
- ya se puede consultar su ficha completa
- ya se puede registrar el historial de interacciones
- el sistema ya queda listo para que el pipeline comercial trabaje sobre clientes reales

20. Siguiente estado recomendado del proyecto

La siguiente fase natural del proyecto es la FASE 4: Pipeline comercial.

Como base ya existente, la Fase 4 debe reutilizar:

- apps.clients como fuente maestra de clientes
- la estrategia de permisos ya definida en users
- la arquitectura de services, selectors y forms
- la estructura modular real del proyecto

La Fase 4 debe construir sobre esta base:

- Opportunity
- OpportunityStage
- OpportunityStageHistory
- tablero kanban
- responsables
- notas
- conversión de oportunidad ganada a proyecto

No avanzar rompiendo la arquitectura ya establecida.


BASE DE DATOS:
DB_NAME=crm_construction
DB_USER=postgres
DB_PASSWORD=admin2026
DB_HOST=127.0.0.1
DB_PORT=5432
DB_SSL_REQUIRE=False


# PROMPT DE CIERRE - FASE 1 Y FASE 2 COMPLETADAS

## RESUMEN EJECUTIVO

Se completó exitosamente la configuración base del proyecto **crm_construction** (Fase 1) y el módulo de **Usuarios, Autenticación, Roles y Seguridad** (Fase 2). El proyecto está funcionando correctamente con PostgreSQL, modelo de usuario personalizado y sistema de autenticación completo.

---

## 1. ESTADO FINAL DEL PROYECTO

### ✅ Proyecto levantado y funcionando en:
- **URL Local**: http://127.0.0.1:8000
- **Admin Django**: http://127.0.0.1:8000/admin/
- **Login CRM**: http://127.0.0.1:8000/accounts/login/
- **Dashboard**: http://127.0.0.1:8000/dashboard/

### ✅ Superusuario creado:
- **Username**: admin
- **Email**: admin@example.com
- **Password**: [definido por el usuario]

---

## 2. TECNOLOGÍAS Y DEPENDENCIAS IMPLEMENTADAS

### Stack Tecnológico Base:
| Tecnología | Versión | Uso |
|------------|---------|-----|
| Django | 6.0.4 | Framework web principal |
| PostgreSQL | - | Base de datos (local) |
| python-decouple | 3.8+ | Variables de entorno |
| psycopg2-binary | 2.9+ | Adaptador PostgreSQL |
| Pillow | 10.0+ | Manejo de imágenes |
| django-extensions | 3.2+ | Herramientas de desarrollo |
| ipython | 8.0+ | Shell interactivo mejorado |
| whitenoise | - | Archivos estáticos (producción) |

### Autenticación y Seguridad:
- **Custom User Model**: `apps.users.User` (heredado de AbstractUser)
- **Autenticación**: Sistema nativo de Django (`AuthenticationForm`)
- **Recuperación de contraseña**: Sistema nativo de Django (`PasswordResetForm`)
- **Roles**: Grupos de Django (`django.contrib.auth.models.Group`)
- **Permisos**: Sistema de permisos de Django (`Permission`)

---

## 3. ESTRUCTURA DEL PROYECTO (ESTADO ACTUAL)

```
crm_construction/
├── manage.py
├── .env                    # Configuración local (PostgreSQL, DEBUG, etc.)
├── .env.example
├── .gitignore
├── README.md
├── requirements/
│   ├── base.txt            # Dependencias base
│   ├── local.txt           # Dependencias desarrollo
│   └── production.txt      # Dependencias producción
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py             # URLs raíz configuradas
│   └── settings/
│       ├── __init__.py
│       ├── base.py         # Configuración base (PostgreSQL, auth)
│       ├── local.py        # Configuración desarrollo
│       └── production.py   # Configuración producción
├── core/                   # Módulo compartido (completo)
│   ├── db/
│   │   ├── base.py         # Modelos abstractos: UUIDModel, TimeStampedModel, 
│   │   │                   # UserStampedModel, SoftDeleteModel, BaseModel
│   │   ├── managers.py
│   │   ├── querysets.py
│   │   └── choices.py
│   ├── middleware/
│   │   ├── request_id.py   # Trazabilidad de requests
│   │   └── activity_logging.py
│   ├── utils/
│   │   ├── dates.py
│   │   ├── emails.py
│   │   ├── files.py
│   │   └── strings.py
│   ├── services/
│   │   ├── email_sender.py
│   │   └── storage.py
│   └── management/
│       └── commands/
│           └── check_visit_reminders.py
├── apps/
│   ├── users/              # ✅ Módulo COMPLETO (Fase 2)
│   │   ├── models/
│   │   │   ├── entities.py     # User, UserAccessLog
│   │   │   └── choices.py      # AccessEventType, AccessEventStatus
│   │   ├── forms.py            # UserCreateForm, UserUpdateForm, UserProfileForm,
│   │   │                       # UserFilterForm, RoleForm, UserPasswordResetForm
│   │   ├── views.py            # CRMLoginView, CRMLogoutView, ProfileView,
│   │   │                       # UserListView, UserCreateView, UserUpdateView,
│   │   │                       # UserActivateView, UserDeactivateView,
│   │   │                       # RoleListView, RoleCreateView, RoleUpdateView,
│   │   │                       # AccessLogListView, password reset views
│   │   ├── urls.py             # Rutas del módulo users
│   │   ├── admin.py            # UserAdmin, UserAccessLogAdmin
│   │   ├── permissions.py      # AppPermissionRequiredMixin
│   │   ├── selectors.py        # Consultas optimizadas
│   │   ├── services.py         # Lógica de negocio (create_user, update_user, etc.)
│   │   └── migrations/
│   │       └── 0001_initial.py # Migración inicial aplicada
│   ├── clients/            # ⏳ Módulo creado, pendiente de migración
│   ├── sales/              # ⏳ Estructura creada, sin implementar
│   ├── projects/           # ⏳ Estructura creada, sin implementar
│   ├── workforce/          # ⏳ Estructura creada, sin implementar
│   ├── media_assets/       # ⏳ Estructura creada, sin implementar
│   ├── visits/             # ⏳ Estructura creada, sin implementar
│   ├── notifications/      # ⏳ Estructura creada, sin implementar
│   ├── billing/            # ⏳ Estructura creada, sin implementar
│   ├── dashboard/          # ⏳ Estructura creada, sin implementar
│   └── auditlog/           # ⏳ Estructura creada, sin implementar
├── templates/              # ✅ Plantillas base creadas
│   ├── base.html
│   ├── includes/
│   │   └── messages.html
│   ├── registration/
│   │   ├── login.html
│   │   ├── password_reset_form.html
│   │   ├── password_reset_done.html
│   │   ├── password_reset_confirm.html
│   │   └── password_reset_complete.html
│   ├── dashboard/
│   │   └── home.html
│   └── users/
│       ├── profile.html
│       ├── list.html
│       ├── detail.html
│       ├── form.html
│       ├── role_list.html
│       ├── role_form.html
│       └── access_log_list.html
├── static/                 # ✅ Carpeta creada
│   ├── css/
│   ├── js/
│   └── img/
├── media/                  # ✅ Carpeta creada
├── tests/                  # ✅ Estructura de pruebas
│   ├── factories/
│   └── integration/
└── docs/
    ├── modules.md
    └── deployment.md
```

---

## 4. ARCHIVOS MODIFICADOS/CREADOS EN ESTA SESIÓN

### Archivos de Configuración:
| Archivo | Acción | Cambios Realizados |
|---------|--------|-------------------|
| `.env` | Creado | Configuración PostgreSQL local, DEBUG=True |
| `config/settings/base.py` | Modificado | Configuración DATABASES explícita (no dj_database_url), AUTH_USER_MODEL, LOGIN_REDIRECT_URL |
| `config/urls.py` | Modificado | Rutas raíz, include de users, dashboard |

### Módulo Users (apps/users/):
| Archivo | Acción | Contenido Clave |
|---------|--------|-----------------|
| `models/__init__.py` | Modificado | Exporta `User` y `UserAccessLog` |
| `models/entities.py` | Modificado | Clase `User` (custom), clase `UserAccessLog`, campo `must_change_password` |
| `models/choices.py` | Creado | `AccessEventType`, `AccessEventStatus` |
| `forms.py` | Reescrito | `UserCreateForm`, `UserUpdateForm`, `UserProfileForm`, `UserFilterForm`, `RoleForm`, `UserPasswordResetForm` |
| `views.py` | Modificado | Eliminado `CustomAuthenticationForm`, usa `AuthenticationForm` de Django. Agregado `PasswordResetForm`. Corregido `ProfileForm` → `UserProfileForm` |
| `admin.py` | Modificado | Registro de `User` y `UserAccessLog` en admin |
| `selectors.py` | Verificado | `get_role_queryset()` retorna QuerySet |
| `services.py` | Verificado | Funciones CRUD para usuarios y roles |
| `urls.py` | Verificado | Rutas completas del módulo |
| `migrations/0001_initial.py` | Generado | Migración inicial aplicada |

### Core (core/db/):
| Archivo | Acción | Cambios Realizados |
|---------|--------|-------------------|
| `base.py` | Verificado | Clases abstractas: `UUIDModel`, `TimeStampedModel`, `UserStampedModel`, `SoftDeleteModel`, `BaseModel` |

### Módulo Clients:
| Archivo | Estado | Notas |
|---------|--------|-------|
| `models/entities.py` | Creado | Modelos `Client` y `ClientInteraction` |
| `models/choices.py` | Creado | `ClientType`, `ClientStatus`, `InteractionType` |
| Estructura completa | Creada | Pendiente de migración (próximo paso) |

---

## 5. DECISIONES TÉCNICAS CLAVE TOMADAS

### 5.1 Base de Datos
- **Decisión**: Usar configuración explícita de PostgreSQL (DB_NAME, DB_USER, etc.) en lugar de `DATABASE_URL`
- **Razón**: Arquitectura del proyecto lo requiere, mayor claridad en variables

### 5.2 Modelo de Usuario
- **Decisión**: Usar `AbstractUser` + `TimeStampedModel` (sin `BaseModel` completo)
- **Razón**: `BaseModel` incluye `SoftDeleteModel` que no aplica para usuarios
- **Campo agregado**: `must_change_password` (BooleanField)

### 5.3 Autenticación
- **Decisión**: Usar `AuthenticationForm` nativo de Django en lugar de crear `CustomAuthenticationForm`
- **Razón**: Simplificar, evitar código innecesario, funcionalidad completa

### 5.4 Recuperación de Contraseña
- **Decisión**: Usar `PasswordResetForm` nativo de Django, extender con `UserPasswordResetForm` para personalización
- **Razón**: Mantener funcionalidad probada, permitir extensión futura

### 5.5 Roles y Permisos
- **Decisión**: Usar `Group` y `Permission` de Django (no modelo `Role` custom)
- **Razón**: Integración nativa con admin, mixins de permisos, escalabilidad

### 5.6 Encoding de Archivos
- **Decisión**: Agregar `# -*- coding: utf-8 -*-` en archivos con caracteres especiales
- **Razón**: Evitar errores de sintaxis en Windows con acentos

---

## 6. ERRORES ENCONTRADOS Y SOLUCIONES

| Error | Causa | Solución Aplicada |
|-------|-------|-------------------|
| `ModuleNotFoundError: No module named 'dj_database_url'` | Import no necesario en settings | Eliminado import, uso de configuración explícita |
| `ImportError: cannot import name 'UserAccessLog'` | Clase no existía en entities.py | Creada clase `UserAccessLog` completa |
| `SyntaxError: Non-UTF-8 code starting with '\xf3'` | Acentos en strings sin encoding | Agregado `# -*- coding: utf-8 -*-` al inicio |
| `FieldError: Unknown field(s) (must_change_password)` | Campo no existía en modelo User | Agregado campo `must_change_password` al modelo |
| `AttributeError: 'function' object has no attribute 'all'` | `get_role_queryset` sin paréntesis | Cambiado `get_role_queryset` → `get_role_queryset()` |
| `ImportError: cannot import name 'CustomAuthenticationForm'` | Formulario no existía | Reemplazado por `AuthenticationForm` de Django |
| `ImportError: cannot import name 'RoleForm'` | Formulario no existía | Creada clase `RoleForm` completa |
| `WARNING: staticfiles.W004` | Carpeta static no existía | Creada carpeta `static/` con subcarpetas |

---

## 7. CONFIGURACIÓN DE ENTORNO (.env)

```env
DJANGO_SETTINGS_MODULE=config.settings.local
DEBUG=True
TIME_ZONE=America/Guayaquil
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=

DB_NAME=crm_construction
DB_USER=postgres
DB_PASSWORD=admin2026
DB_HOST=127.0.0.1
DB_PORT=5432
DB_SSL_REQUIRE=False

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=False
DEFAULT_FROM_EMAIL=CRM Construction <no-reply@example.com>

SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=31536000
```

---

## 8. COMANDOS EJECUTADOS (EN ORDEN)

```powershell
# 1. Activar entorno virtual
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1

# 2. Instalar dependencias
pip install -r requirements/local.txt

# 3. Corregir archivos (múltiples iteraciones)
# - entities.py: UserAccessLog, must_change_password
# - forms.py: RoleForm, UserPasswordResetForm, get_role_queryset()
# - views.py: AuthenticationForm, PasswordResetForm, UserProfileForm
# - admin.py: encoding UTF-8

# 4. Crear carpeta static
New-Item -ItemType Directory -Path static -Force

# 5. Migraciones
python manage.py makemigrations users
python manage.py migrate

# 6. Superusuario
python manage.py createsuperuser

# 7. Ejecutar servidor
python manage.py runserver
```

---

## 9. INTERFERENCIAS CON FASES PREVIAS

### Cambios que afectaron la arquitectura original:

| Aspecto | Plan Original | Implementación Real | Impacto |
|---------|---------------|---------------------|---------|
| Base de datos | `dj_database_url` | Variables explícitas DB_* | **Positivo**: Más claro, sin dependencia extra |
| Modelo User | Solo `TimeStampedModel` | Se mantuvo igual | **Neutro**: Se agregó `must_change_password` |
| Roles | `Group` nativo | Se mantuvo igual | **Positivo**: Sin modelo custom innecesario |
| Autenticación | `CustomAuthenticationForm` | `AuthenticationForm` nativo | **Positivo**: Menos código, misma funcionalidad |
| UserAccessLog | Planeado en Fase 2 | Implementado en Fase 1-2 | **Positivo**: Trazabilidad desde inicio |

### Estructura de carpetas: Se respetó completamente la arquitectura definida.

---

## 10. PRÓXIMOS PASOS (FASE 3 - CLIENTS)

### Pendiente inmediato:
```powershell
# 1. Migraciones del módulo clients
python manage.py makemigrations clients
python manage.py migrate

# 2. Verificar que el módulo funciona
python manage.py runserver
# Navegar a http://127.0.0.1:8000/clients/
```

### Tareas Fase 3:
- [ ] Aplicar migraciones de `Client` y `ClientInteraction`
- [ ] Probar CRUD de clientes
- [ ] Probar registro de interacciones
- [ ] Probar desactivación/reactivación
- [ ] Probar filtros y búsqueda
- [ ] Agregar pruebas unitarias del módulo

---

## 11. NOTAS IMPORTANTES PARA CONTINUIDAD

1. **NO** usar `dj_database_url` - mantener configuración explícita
2. **NO** crear modelo `Role` custom - usar `Group` de Django
3. **SIEMPRE** agregar `# -*- coding: utf-8 -*-` en archivos con acentos
4. **MANTENER** `AUTH_USER_MODEL = "users.User"`
5. **USAR** `get_role_queryset()` con paréntesis en formularios
6. **RESPETAR** la estructura de archivos por módulo (models/, forms.py, views.py, etc.)

---

## 12. ESTADO DE MÓDULOS

| Módulo | Estado | Migraciones | Funcionalidad |
|--------|--------|-------------|---------------|
| core | ✅ Completo | N/A | Modelos base, middleware, utils |
| users | ✅ Completo | ✅ Aplicadas | Login, logout, CRUD, roles, perfil |
| clients | ⏳ Estructura | ❌ Pendiente | Modelos creados, vistas listas |
| sales | ⏳ Vacío | ❌ Pendiente | Solo estructura |
| projects | ⏳ Vacío | ❌ Pendiente | Solo estructura |
| workforce | ⏳ Vacío | ❌ Pendiente | Solo estructura |
| media_assets | ⏳ Vacío | ❌ Pendiente | Solo estructura |
| visits | ⏳ Vacío | ❌ Pendiente | Solo estructura |
| notifications | ⏳ Vacío | ❌ Pendiente | Solo estructura |
| billing | ⏳ Vacío | ❌ Pendiente | Solo estructura |
| dashboard | ⏳ Básico | N/A | Vista home funcional |
| auditlog | ⏳ Vacío | ❌ Pendiente | Solo estructura |

## 13. CONCLUSIÓN

El proyecto **crm_construction** está operativo con:
- ✅ Fase 1 (Base del sistema): 100% completada.
- ✅ Fase 2 (Usuarios y autenticación): 100% completada.
- ⏳ Fase 3 (Clients): Estructura creada, pendiente de migración.

-
## 1. PROPÓSITO DE ESTE DOCUMENTO

Este prompt complementa el prompt maestro del CRM `crm_construction` y **debe considerarse como la fuente de verdad actualizada tras la finalización de la Fase 3 (Clients) y la integración inicial de la Fase 4 (Sales)**.

Incluye:
- El estado real de cada módulo tras las correcciones de hoy.
- Los errores encontrados y sus soluciones exactas.
- Los cambios estructurales realizados en configuración, URLs y plantillas.
- La confirmación de que las Fases 1, 2 y 3 están operativas y validadas.
- El estado de la Fase 4, que está migrada y con código completo, pero requiere la creación de plantillas HTML (ya proporcionadas) y la asignación de permisos.

**Regla de oro:** Cualquier avance posterior debe partir de este estado documentado. No se debe reconstruir nada de las fases ya cerradas.

---

## 2. ESTADO REAL DE LOS MÓDULOS (POST-CORRECCIONES)

| Módulo       | Estado                    | Migraciones | Funcionalidad comprobada |
|--------------|---------------------------|-------------|--------------------------|
| `core`       | ✅ Completo               | N/A         | Modelos base, middleware |
| `users`      | ✅ Completo (Fase 2)      | Aplicadas   | Login, perfil, roles, logs de acceso |
| `clients`    | ✅ **Validado** (Fase 3)  | Aplicadas   | CRUD, interacciones, desactivación, búsqueda |
| `sales`      | ⚠️ Migrado, código listo  | Aplicadas   | Vistas, servicios y admin listos; pendiente confirmación de plantillas |
| `dashboard`  | ✅ Funcional              | N/A         | `dashboard_home` con TemplateView |
| `projects`   | ⏳ Estructura creada      | No          | Sólo esqueleto de carpeta |
| Otros (`workforce`, `visits`, etc.) | ⏳ No implementados | No | Estructura de carpetas vacía |

---

## 3. ERRORES ENCONTRADOS Y SOLUCIONES APLICADAS DURANTE LA SESIÓN

### 3.1 Error: `NoReverseMatch: 'dashboard_home' not found` en `base.html`

**Causa:** La URL `dashboard_home` estaba definida en `config/urls.py` pero el servidor no había recargado correctamente la configuración o existía una referencia incorrecta en la plantilla.

**Solución aplicada:**
- Se verificó que `config/urls.py` contiene:
  ```python
  path('dashboard/', TemplateView.as_view(template_name='dashboard/home.html'), name='dashboard_home'),
  ```
- Se reemplazó temporalmente `{% url 'dashboard_home' %}` por `/dashboard/` en `base.html` para continuar las pruebas.
- Posteriormente se restauró el uso correcto de `{% url %}` una vez validado el reinicio del servidor.

**Archivos modificados:**
- `templates/base.html` (cambio temporal revertido después de confirmar funcionamiento)

### 3.2 Error: `TemplateSyntaxError: 'block' tag with name 'content' appears more than once` en `/accounts/login/`

**Causa:** El template `templates/registration/login.html` contenía un bloque `{% block content %}` duplicado o mal cerrado.

**Solución aplicada:**
- Se reemplazó el contenido completo de `login.html` por una versión limpia con un único bloque `content`.

**Archivos modificados:**
- `templates/registration/login.html` (reescrito)

### 3.3 Error: `ImproperlyConfigured: Application labels aren't unique, duplicates: django_extensions`

**Causa:** `django_extensions` aparecía tanto en `base.py` como en `local.py` (debido a un `if` que volvía a agregarla).

**Solución aplicada:**
- Se optó por la **Opción B**: mantener `django_extensions` **solo en `local.py`** y eliminarla completamente de `base.py` (mejor práctica de separación de entornos).
- En `local.py` se agregó con `INSTALLED_APPS.append('django_extensions')` sin condicionales para evitar falsos positivos.

**Archivos modificados:**
- `config/settings/base.py`: eliminada línea `'django_extensions'`.
- `config/settings/local.py`: añadido `INSTALLED_APPS.append('django_extensions')`.

**Resultado:** Comando `check` limpio, migraciones de `sales` generadas correctamente.

### 3.4 Error: `AttributeError: module 'apps.sales.views' has no attribute 'OpportunityListView'`

**Causa:** El archivo `apps/sales/views.py` no contenía la implementación completa de las vistas (posiblemente estaba vacío o con nombres incorrectos).

**Solución aplicada:**
- Se proporcionó el código completo y depurado de `views.py` (incluye `OpportunityListView`, `OpportunityKanbanView`, etc.).
- Se verificó que las importaciones a `forms`, `services` y `selectors` fueran correctas.

**Archivos modificados:**
- `apps/sales/views.py` (sobrescrito con código funcional)

### 3.5 Error: `TemplateDoesNotExist` en vistas de `sales` (esperado)

**Causa:** Las plantillas HTML para el módulo `sales` no habían sido creadas aún.

**Solución aplicada:**
- Se entregaron versiones básicas de las cuatro plantillas necesarias:
  - `templates/sales/opportunity_list.html`
  - `templates/sales/opportunity_kanban.html`
  - `templates/sales/opportunity_form.html`
  - `templates/sales/opportunity_detail.html`
- Estas plantillas están listas para ser copiadas a la carpeta correspondiente.

### 3.6 Error 500 en admin al acceder a `OpportunityStage` (Python 3.14 + Django 4.2)

**Causa probable:** Incompatibilidad entre Python 3.14 y Django 4.2 en el manejo de copia de contextos de plantilla (`__copy__`). Se manifestó al intentar agregar un `OpportunityStage` desde el admin.

**Solución propuesta (no aplicada en la sesión, pero documentada):**
- **Recomendación fuerte:** Usar Python 3.11 o 3.12 para este proyecto.
- **Parche temporal:** Agregar monkey patch en `config/__init__.py` o `core/apps.py` (proporcionado en la respuesta).

**Impacto:** La funcionalidad de admin para `sales` puede estar limitada en Python 3.14, pero las operaciones vía servicios (`bootstrap_default_stages()`) y vistas frontend no deberían verse afectadas.

---

## 4. ARQUITECTURA Y DECISIONES TÉCNICAS CONSOLIDADAS

### 4.1 Configuración de entornos
- **`base.py`**: Contiene configuración común y **NO incluye herramientas de desarrollo**.
- **`local.py`**: Hereda de `base` y agrega `DEBUG=True`, `django_extensions`, y Email Backend de consola.
- **`production.py`**: Hereda de `base` y aplica configuraciones de seguridad y rendimiento (aún por definir en detalle).

### 4.2 URLs y namespaces
- Se mantiene `app_name = 'users'` en `apps/users/urls.py`.
- Se mantiene `app_name = 'sales'` en `apps/sales/urls.py`.
- La URL del dashboard está definida en `config/urls.py` con `name='dashboard_home'`.
- Se utiliza `include()` para todas las apps locales.

### 4.3 Modelos abstractos base (`core.db.base`)
Se usan consistentemente:
- `BaseModel` en `Client`, `ClientInteraction`, `Opportunity`, `OpportunityStage`, `OpportunityStageHistory`.
- `UserStampedModel` para trazabilidad de creación/edición.
- `SoftDeleteModel` en `Client` para desactivación lógica.

### 4.4 Estrategia de permisos
- **Roles**: `Group` de Django.
- **Permisos**: `Permission` nativos, asignados por grupo o usuario.
- Se definieron permisos personalizados en `Meta` de `Opportunity` (`move_opportunity`, `convert_opportunity`).
- Las vistas de `sales` usan `PermissionRequiredMixin` con los permisos correspondientes.

### 4.5 Separación de responsabilidades
- **`services.py`**: `create_opportunity`, `move_opportunity_stage`, `bootstrap_default_stages`, `build_project_seed_from_opportunity`.
- **`selectors.py`**: `get_opportunity_list`, `get_kanban_board`, `get_opportunity_detail`.
- **`forms.py`**: `OpportunityForm`, `OpportunityStageMoveForm`, `OpportunityFilterForm`.

---

## 5. FASE 4 — ESTADO ACTUAL DETALLADO

### ✅ Migraciones aplicadas
- Archivo de migración `0001_initial.py` creado y aplicado para `sales`.
- Tablas `sales_opportunitystage`, `sales_opportunity`, `sales_opportunitystagehistory` existen en PostgreSQL.

### ✅ Código fuente completo y funcional
Los siguientes archivos han sido proporcionados y validados sintácticamente:
- `apps/sales/models/entities.py`
- `apps/sales/models/choices.py`
- `apps/sales/services.py`
- `apps/sales/selectors.py`
- `apps/sales/forms.py`
- `apps/sales/views.py`
- `apps/sales/urls.py`
- `apps/sales/admin.py`

### ⚠️ Pendiente de validación visual
- Las plantillas HTML han sido proporcionadas pero **no se ha confirmado que se hayan copiado** a `templates/sales/`.
- Se recomienda copiarlas y probar las rutas:
  - `/sales/`
  - `/sales/kanban/`
  - `/sales/create/`
  - `/sales/<uuid>/`

### ⚠️ Pendiente de carga de etapas
- Aunque el servicio `bootstrap_default_stages()` está listo, **no se ejecutó en esta sesión** debido al error 500 del admin. Se puede ejecutar desde el shell de Django sin problema:
  ```python
  from apps.sales.services import bootstrap_default_stages
  bootstrap_default_stages()
  ```

### ⚠️ Pendiente de asignación de permisos
- El superusuario `admin` debe tener asignados los permisos de `sales` para acceder a las vistas. Esto puede hacerse vía admin o shell.

---

## 6. ESTRUCTURA DE ARCHIVOS QUE FUERON CREADOS O MODIFICADOS EN ESTA SESIÓN

| Ruta | Acción | Motivo |
|------|--------|--------|
| `config/settings/base.py` | Modificado | Eliminar `django_extensions` duplicado |
| `config/settings/local.py` | Modificado | Agregar `django_extensions` de forma segura |
| `templates/base.html` | Modificado | Ajuste temporal de URL del dashboard |
| `templates/registration/login.html` | Reemplazado | Corregir duplicación de bloque `content` |
| `apps/sales/views.py` | Reemplazado | Implementar todas las vistas faltantes |
| `apps/sales/migrations/0001_initial.py` | Creado | Migración inicial del módulo |
| `templates/sales/` (carpeta y 4 archivos) | Proporcionados | Plantillas base para el pipeline comercial |

---

## 7. REGLAS PARA LA CONTINUIDAD DEL PROYECTO

1. **No se debe modificar la configuración de `django_extensions` nuevamente**: permanece solo en `local.py`.
2. **No se debe cambiar la estructura de URLs** ni los nombres de las vistas ya definidas.
3. **Las plantillas de `sales` deben crearse** con el contenido proporcionado antes de continuar con pruebas visuales.
4. **La carga de etapas (`bootstrap_default_stages`) debe realizarse** antes de usar el pipeline.
5. **Se recomienda cambiar a Python 3.11/3.12** para evitar errores de compatibilidad en el admin.

---

## 8. CONCLUSIÓN Y SIGUIENTE PASO NATURAL

- **Fase 1, 2 y 3 están completamente cerradas y validadas.**
- **Fase 4 está técnicamente integrada** (código, migraciones, servicios) y **solo requiere la creación de las plantillas HTML y la ejecución del bootstrap de etapas** para considerarse operativa.
- Una vez confirmado el funcionamiento visual de `sales`, el proyecto estará listo para abordar la **Fase 5: Gestión de Proyectos**, que utilizará el servicio `build_project_seed_from_opportunity` para crear proyectos a partir de oportunidades ganadas.


Respecto a la conversión a proyecto:
Esa ruta /sales/<uuid>/convert/ está implementada en OpportunityConvertToProjectView (usando build_project_seed_from_opportunity). FALTA EL MODULO projects, por lo que al hacer POST falla – se abordará en la Fase 5.
 FASE 4 COMPLETADA: MÓDULO SALES (Pipeline Comercial)
1. Objetivo de la fase
Construir el módulo de oportunidades comerciales (apps.sales) con tablero Kanban, historial de etapas, creación/edición de oportunidades, cambio de etapa, y preparación para conversión a proyecto.

2. Estado final tras las correcciones
✅ Migraciones aplicadas (sales_opportunitystage, sales_opportunity, sales_opportunitystagehistory).

✅ Modelos funcionando con relaciones correctas (FK stage, no current_stage).

✅ Servicios (services.py) y selectores (selectors.py) implementados y corregidos.

✅ Vistas protegidas por permisos (add_opportunity, view_opportunity, change_opportunity, move_opportunity, convert_opportunity).

✅ Formularios funcionales (OpportunityForm, OpportunityStageMoveForm, OpportunityFilterForm).

✅ Plantillas base del módulo creadas (list.html, form.html, detail.html, kanban.html).

✅ Rutas registradas en config/urls.py con namespace sales.

✅ Kanban visual con CSS puro, sin dependencias externas.

✅ Comando bootstrap_default_stages() ejecutado (etapas iniciales creadas).

3. Archivos creados o modificados (lista definitiva)
3.1 Nuevos archivos (creados durante la fase)
text
apps/sales/
├── __init__.py
├── apps.py
├── admin.py
├── urls.py
├── views.py
├── forms.py
├── permissions.py
├── selectors.py
├── services.py
├── models/
│   ├── __init__.py
│   ├── entities.py
│   └── choices.py
├── templates/sales/
│   ├── opportunity_list.html
│   ├── opportunity_form.html
│   ├── opportunity_detail.html
│   └── opportunity_kanban.html
└── migrations/
    └── 0001_initial.py
3.2 Archivos modificados (fuera de apps/sales)
Ruta	Cambio
config/settings/base.py	- Se agregó 'apps.sales' a LOCAL_APPS / INSTALLED_APPS.
- Se corrigió LOGIN_REDIRECT_URL = "dashboard_home" (antes "dashboard").
- Se añadió el patch de contexto para Python 3.14 (función patch_context_copy).
config/urls.py	Se agregó path("sales/", include("apps.sales.urls")),
templates/base.html	Se agregaron bloques {% block extra_css %} y {% block extra_js %} (opcional, pero recomendado).
4. Decisiones técnicas clave (no cambiar)
4.1 Modelos
Opportunity.stage → FK a OpportunityStage (el campo se llama stage, no current_stage).

OpportunityStage.order → el campo se llama position (no order).

Todos los modelos heredan de BaseModel (UUID, timestamps, soft delete) y UserStampedModel (trazabilidad).

4.2 Selectors (selectors.py)
get_opportunity_list() → usa select_related('client', 'responsible', 'stage').

get_kanban_board() → ordena etapas por position, filtra oportunidades activas, retorna diccionario {stage_id: {'stage': stage, 'opportunities': [...]}}.

get_opportunity_detail() → usa select_related con 'stage' y prefetch_related('stage_history').

4.3 Servicios (services.py)
create_opportunity() → requiere obligatoriamente created_by (parámetro keyword-only). Asigna etapa por defecto con get_default_stage().

move_opportunity_stage() → crea registro en OpportunityStageHistory.

bootstrap_default_stages() → crea las etapas iniciales (Lead, Proposal, Negotiation, Won, Lost) con position y colores.

get_default_stage() → retorna la primera etapa activa ordenada por position.

4.4 Vistas (views.py)
OpportunityCreateView → no usa form.save(), llama a create_opportunity con created_by=self.request.user.

OpportunityDetailView → sobrescribe get_object() para usar get_opportunity_detail(); no sobrescribe get_queryset.

OpportunityKanbanView → es TemplateView, no ListView. Pasa board al contexto.

OpportunityMoveStageView → recibe POST con to_stage y opcional note.

OpportunityConvertToProjectView → prepara semilla en sesión y redirige a projects:create_from_opportunity (aún no implementado).

4.5 Plantillas
opportunity_kanban.html → usa CSS puro incrustado. No depende de Bootstrap. Itera sobre board.items().

Las demás plantillas usan base.html y se apoyan en bloques estándar (content).

4.6 Permisos
Se definieron permisos en Meta de Opportunity: view_opportunity, add_opportunity, change_opportunity, delete_opportunity, move_opportunity, convert_opportunity.

Las vistas usan PermissionRequiredMixin con el permiso correspondiente.

5. Variables y rutas críticas (no modificar)
5.1 En settings/base.py
python
LOGIN_REDIRECT_URL = "dashboard_home"   # Nombre de la URL, no la ruta
5.2 En config/urls.py
python
path("sales/", include("apps.sales.urls")),
5.3 En apps/sales/urls.py
python
app_name = "sales"
urlpatterns = [
    path("", views.OpportunityListView.as_view(), name="list"),
    path("kanban/", views.OpportunityKanbanView.as_view(), name="kanban"),
    path("create/", views.OpportunityCreateView.as_view(), name="create"),
    path("<uuid:pk>/", views.OpportunityDetailView.as_view(), name="detail"),
    path("<uuid:pk>/edit/", views.OpportunityUpdateView.as_view(), name="edit"),
    path("<uuid:pk>/move/", views.OpportunityMoveStageView.as_view(), name="move"),
    path("<uuid:pk>/convert/", views.OpportunityConvertToProjectView.as_view(), name="convert"),
]
6. Comandos ejecutados que no deben repetirse
bash
python manage.py makemigrations sales
python manage.py migrate sales
python manage.py shell
>>> from apps.sales.services import bootstrap_default_stages
>>> bootstrap_default_stages()
>>> exit()
7. Advertencias para fases futuras
Nunca cambiar el nombre del campo stage en Opportunity (no usar current_stage).

Nunca cambiar el campo position en OpportunityStage (no usar order).

Toda vista que cree oportunidades debe usar create_opportunity y pasar created_by.

El Kanban espera la variable board en el contexto, no stages ni object_list.

No se debe reemplazar get_object por get_queryset en OpportunityDetailView (causa error de atributo).

La conversión a proyecto (convert/) está preparada pero requiere el módulo projects (Fase 5). La vista asume que existe la URL projects:create_from_opportunity.

8. Relaciones con otros módulos
Clients: Opportunity.client → FK a Client.

Users: Opportunity.responsible → FK a User; created_by/updated_by heredados.

Projects (futuro): OpportunityConvertToProjectView genera semilla y redirige.

9. Pruebas confirmadas
✅ Crear oportunidad desde formulario.

✅ Listar oportunidades con filtros.

✅ Ver detalle con historial de etapas.

✅ Cambiar etapa desde detalle (formulario) y desde Kanban (selector).

✅ Kanban muestra columnas y tarjetas.

✅ Editar oportunidad.

✅ Permisos: usuario sin permiso no accede.

10. Nota final
Este módulo está cerrado y validado. Cualquier modificación futura debe respetar la estructura de archivos, nombres de variables y lógica de servicios aquí documentada. No se deben generar nuevos modelos paralelos para oportunidades.

Perfecto. Aquí tienes un **prompt complementario de cierre de Fase 5** listo para agregar al final de tu prompt maestro. Está redactado para que en la siguiente fase no se rompa nada ya construido y para que el agente futuro entienda exactamente qué quedó implementado, qué rutas existen, qué tecnologías/patrones se usaron y qué cosas **no** pertenecen todavía a esta fase.
FASE 5 PROJECTS, GESTIÓN DE PROYECTOS Y NÚCLEO OPERATIVO

A partir de este punto, además del prompt maestro base del proyecto y de las ampliaciones ya aprobadas de las Fases 2, 3 y 4, debes asumir como ya definida, implementada y validada la **FASE 5: Gestión de proyectos** del CRM `crm_construction`, construida sobre la arquitectura real existente y sin romper la base ya establecida del proyecto.

La Fase 5 debe considerarse **cerrada y funcional**.

---

## 1. Alcance real ya definido de la FASE 5

La FASE 5 debe considerarse diseñada, implementada y validada para cubrir:

* módulo `apps.projects`
* gestión operativa de proyectos reales
* creación de proyectos
* edición de proyectos
* detalle de proyectos
* listado y filtros
* asignación de responsables y personal
* notas internas
* estados operativos del proyecto
* relación con cliente
* relación opcional con oportunidad
* integración con la conversión desde `sales`

El objetivo funcional de esta fase es que el CRM ya no solo gestione ventas, sino también la ejecución real de trabajos.

---

## 2. Rol del módulo `apps.projects` dentro de la arquitectura

A partir de esta fase, `apps.projects` debe entenderse como el módulo responsable de:

* centralizar la entidad operativa principal del trabajo real
* enlazar cliente, oportunidad y responsables con el proyecto
* servir de base para workforce, media assets, visits y billing
* registrar asignaciones activas del proyecto
* registrar notas internas de operación
* ofrecer una ficha operativa del proyecto lista para evolución futura

La estructura obligatoria del módulo se mantiene bajo el patrón ya definido en el proyecto:

* `views.py`: orquestación y presentación
* `forms.py`: formularios y validación de captura
* `permissions.py`: protección de acceso
* `selectors.py`: consultas de lectura y filtros
* `services.py`: lógica de negocio y acciones del módulo
* `models/`: entidades y choices
* `tests/`: pruebas del módulo

---

## 3. Estado oficial del módulo `apps.projects`

La FASE 5 deja aprobado `apps.projects` como app activa real del sistema.

La estructura funcional aprobada es:

```text
apps/projects/
├── __init__.py
├── apps.py
├── admin.py
├── urls.py
├── views.py
├── forms.py
├── permissions.py
├── selectors.py
├── services.py
├── models/
│   ├── __init__.py
│   ├── entities.py
│   └── choices.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_services.py
    └── test_views.py
```

Plantillas reales usadas:

```text
templates/projects/
├── list.html
├── form.html
└── detail.html
```

Regla:
A partir de esta fase, `apps.projects` debe considerarse parte real del sistema y debe estar activa en `INSTALLED_APPS`.

---

## 4. Estado oficial de la entidad `Project`

La entidad maestra aprobada en esta fase es:

* `Project`

Su responsabilidad es representar el trabajo operativo real dentro del CRM.

La base funcional aprobada de `Project` incluye como mínimo:

* `id` UUID heredado
* `client`
* `opportunity`
* `responsible`
* `name`
* `description`
* `location`
* `status`
* `contract_amount`
* `start_date`
* `expected_end_date`
* `actual_end_date`
* `created_at`
* `updated_at`
* `created_by`
* `updated_by`
* herencia desde la base común del proyecto

Reglas funcionales aprobadas:

* `Project` es la entidad operativa maestra del trabajo
* siempre debe relacionarse con un `Client`
* puede relacionarse opcionalmente con una `Opportunity`
* puede tener un responsable principal
* debe soportar evolución futura hacia fotos, visitas, cobranzas y panel de trabajadores
* no debe duplicar la lógica comercial de `sales`
* no debe reemplazar a `Client` como maestro del cliente

---

## 5. Decisión oficial de relación con `Opportunity`

La relación aprobada entre `Project` y `Opportunity` es:

* `Project.opportunity` es opcional
* la relación se implementó para soportar conversión desde ventas
* la conversión desde oportunidad hacia proyecto ya quedó funcional

Regla funcional:

* el proyecto puede crearse manualmente o desde una oportunidad
* cuando se crea desde una oportunidad, el sistema usa una semilla de datos (`project_seed`) guardada en sesión
* la vista de creación desde oportunidad es `projects:create_from_opportunity`
* no debe alterarse este flujo salvo mejora técnica claramente justificada

---

## 6. Estado oficial de `ProjectAssignment`

La entidad aprobada para gestionar asignaciones operativas es:

* `ProjectAssignment`

Su responsabilidad es modelar qué usuarios están asignados a un proyecto y con qué rol operativo.

La base funcional aprobada incluye como mínimo:

* `project`
* `user`
* `role`
* `notes`
* `is_active`
* `assigned_at`
* `unassigned_at`
* timestamps y trazabilidad heredada cuando aplique

Roles base aprobados:

* `responsible`
* `supervisor`
* `worker`
* `support`

Reglas funcionales aprobadas:

* un proyecto puede tener muchas asignaciones
* un usuario puede estar asignado a muchos proyectos
* debe existir consistencia entre `Project.responsible` y la asignación primaria de tipo `responsible`
* la asignación principal se sincroniza desde servicios
* la desactivación de asignaciones es lógica, no destructiva
* no se debe permitir inconsistencias entre el responsable principal y sus asignaciones activas

---

## 7. Estado oficial de `ProjectNote`

La entidad aprobada para bitácora interna del proyecto es:

* `ProjectNote`

Su responsabilidad es registrar notas internas u operativas dentro de la ficha del proyecto.

La base funcional aprobada incluye como mínimo:

* `project`
* `author`
* `note_type`
* `body`
* timestamps y trazabilidad heredada cuando aplique

Tipos base aprobados:

* `internal`
* `field_update`

Reglas funcionales aprobadas:

* cada nota pertenece a un solo proyecto
* las notas se muestran en orden cronológico inverso
* el autor debe quedar registrado cuando exista usuario autenticado
* estas notas son parte del historial operativo del proyecto
* no reemplazan futuros registros especializados de fotos o visitas

---

## 8. Estados operativos aprobados para el proyecto

La FASE 5 deja aprobados estos estados base en `ProjectStatus`:

* `pending`
* `in_progress`
* `completed`

Reglas:

* estos estados son el núcleo base operativo
* no deben reemplazarse por estados comerciales de `sales`
* cualquier ampliación futura debe respetar la separación entre pipeline comercial y ejecución operativa

---

## 9. Servicios aprobados en `apps.projects.services`

La capa de servicios aprobada en esta fase incluye como mínimo:

* `create_project`
* `update_project`
* `_sync_primary_responsible_assignment`
* `assign_user_to_project`
* `deactivate_project_assignment`
* `add_project_note`

Reglas técnicas aprobadas:

* la lógica de negocio no debe ir en views
* la sincronización del responsable principal debe ocurrir desde servicios
* las asignaciones deben reactivarse o reutilizarse cuando sea posible
* las notas deben crearse desde servicio
* deben usarse transacciones donde aplique
* deben aplicarse `full_clean()` y validaciones del dominio antes de guardar

---

## 10. Selectors aprobados en `apps.projects.selectors`

La fase aprueba consultas encapsuladas para:

* listado de proyectos
* filtros por búsqueda
* filtros por estado
* filtros por cliente
* filtros por responsable
* detalle del proyecto con `select_related` y `prefetch_related`
* consulta de proyectos visibles para un usuario

Selectors base aprobados:

* `get_project_base_queryset`
* `get_project_list`
* `get_project_detail`
* `get_projects_for_user`

Reglas:

* las lecturas complejas deben permanecer en `selectors.py`
* no debe duplicarse lógica de consulta compleja en views
* los listados deben venir optimizados con relaciones necesarias

---

## 11. Formularios aprobados en `apps.projects.forms`

Formularios base aprobados:

* `ProjectForm`
* `ProjectFilterForm`
* `ProjectAssignmentForm`
* `ProjectNoteForm`

Responsabilidades aprobadas:

### `ProjectForm`

* creación y edición del proyecto
* validación de fechas
* validación de coherencia entre cliente y oportunidad
* selección de responsable
* exclusión de oportunidades ya asociadas a proyecto salvo la actual en edición

### `ProjectFilterForm`

* búsqueda libre
* filtro por estado
* filtro por cliente
* filtro por responsable

### `ProjectAssignmentForm`

* agregar usuario al proyecto
* seleccionar rol
* agregar nota de asignación
* excluir usuarios ya asignados activamente

### `ProjectNoteForm`

* registrar nota interna
* registrar tipo de nota

---

## 12. Vistas aprobadas en `apps.projects.views`

La fase deja aprobadas como funcionales estas vistas:

* `ProjectListView`
* `ProjectCreateView`
* `ProjectCreateFromOpportunityView`
* `ProjectDetailView`
* `ProjectUpdateView`
* `ProjectAssignmentCreateView`
* `ProjectAssignmentDeactivateView`
* `ProjectNoteCreateView`

Reglas funcionales aprobadas:

* `ProjectCreateFromOpportunityView` consume `project_seed` desde sesión
* esa vista no es una página pública de acceso directo; depende del flujo de conversión desde `sales`
* el detalle del proyecto concentra datos del proyecto, asignaciones activas y notas internas
* la edición reutiliza la misma base de validación del formulario
* la creación y actualización usan servicios, no `form.save()` directo como lógica principal

---

## 13. Rutas oficiales aprobadas para `projects`

Namespace oficial:

* `projects`

Rutas aprobadas:

```python
urlpatterns = [
    path("", views.ProjectListView.as_view(), name="list"),
    path("create/", views.ProjectCreateView.as_view(), name="create"),
    path("create/from-opportunity/", views.ProjectCreateFromOpportunityView.as_view(), name="create_from_opportunity"),
    path("<uuid:pk>/", views.ProjectDetailView.as_view(), name="detail"),
    path("<uuid:pk>/edit/", views.ProjectUpdateView.as_view(), name="edit"),
    path("<uuid:pk>/assignments/add/", views.ProjectAssignmentCreateView.as_view(), name="assignment_create"),
    path("<uuid:pk>/assignments/<uuid:assignment_id>/deactivate/", views.ProjectAssignmentDeactivateView.as_view(), name="assignment_deactivate"),
    path("<uuid:pk>/notes/add/", views.ProjectNoteCreateView.as_view(), name="note_create"),
]
```

Integración global aprobada:

* `config/urls.py` incluye:

  * `path("projects/", include("apps.projects.urls"))`

---

## 14. Integración oficial con `sales`

La Fase 5 deja cerrada la integración con Fase 4.

La conversión desde oportunidad hacia proyecto funciona así:

1. desde el detalle de oportunidad ganada en `sales`
2. se hace POST a:

   * `sales:<uuid>/convert/`
3. `OpportunityConvertToProjectView` construye una semilla con:

   * `build_project_seed_from_opportunity(...)`
4. esa semilla se transforma a un diccionario JSON-safe
5. se guarda en sesión bajo la clave:

   * `project_seed`
6. luego redirige a:

   * `projects:create_from_opportunity`

Reglas técnicas aprobadas:

* no guardar objetos complejos no serializables directamente en sesión
* el seed debe ser serializable a JSON
* la conversión solo debe ocurrir para oportunidades ganadas (`Won`)
* si la oportunidad ya tiene proyecto, debe redirigir al proyecto relacionado
* si se entra manualmente por GET a `/sales/<uuid>/convert/`, la vista puede redirigir al detalle con mensaje, pero la conversión real es por POST

---

## 15. Ajustes aprobados en `sales` que no deben romperse

Durante la validación de Fase 5 quedaron consolidados estos puntos en `sales`:

### `OpportunityStageMoveForm`

Debe aceptar el argumento opcional `opportunity=` y excluir la etapa actual del selector.

### `OpportunityDetailView`

Debe inyectar al contexto:

* `move_form`
* `has_related_project`
* `related_project`

### `templates/sales/opportunity_detail.html`

Debe:

* mostrar correctamente el formulario de mover etapa
* mostrar historial de etapas
* mostrar el botón de convertir a proyecto cuando:

  * el usuario tiene permiso
  * la oportunidad está en `Won`
  * todavía no tiene proyecto relacionado

### `OpportunityConvertToProjectView`

Debe:

* manejar `POST`
* permitir `GET` solo como redirección informativa
* serializar correctamente el seed antes de guardarlo en sesión

Regla:
No alterar esta integración salvo mejora técnica claramente justificada.

---

## 16. Permisos aprobados para `projects`

La fase aprueba como base estos permisos:

* `projects.view_project`
* `projects.add_project`
* `projects.change_project`
* `projects.delete_project`
* `projects.manage_assignments`
* `projects.add_project_note`
* `projects.create_project_from_opportunity`

Reglas:

* las vistas del módulo deben estar protegidas por permisos
* durante la validación se usó superadmin, por lo que no fue necesario asignar grupos para probar
* en fases futuras se deberá probar con usuarios reales por rol sin romper esta base

---

## 17. Admin aprobado en la fase

La fase deja integración administrativa para:

* `Project`
* `ProjectAssignment`
* `ProjectNote`

Características aprobadas del admin:

* `list_display`
* `list_filter`
* `search_fields`
* `autocomplete_fields`
* inlines para asignaciones y notas

Regla:
El admin sirve como soporte y verificación, pero no reemplaza el flujo funcional del CRM web.

---

## 18. Tecnologías y patrones usados dentro de la fase

La FASE 5 debe entenderse implementada con estas bases tecnológicas y decisiones:

* Django 4.2.x
* PostgreSQL
* modelo de usuario custom `users.User`
* sesiones de Django respaldadas por base de datos
* vistas basadas en clases (`ListView`, `CreateView`, `UpdateView`, `DetailView`, `View`)
* mixins de autenticación y permisos de Django
* `select_related` y `prefetch_related` para optimización
* `ModelForm` y `Form` para captura y validación
* `messages` framework de Django para feedback
* `transaction.atomic` en servicios
* serialización segura a JSON para seeds en sesión
* herencia desde `core.db.base`
* separación de responsabilidades:

  * presentación en views
  * lectura en selectors
  * negocio en services
  * validación de entrada en forms
  * estructura de dominio en models

Regla:
No introducir lógica de negocio importante en templates, admin o views si ya existe una capa adecuada para ello.

---

## 19. Pruebas y validaciones funcionales ya realizadas

La FASE 5 debe considerarse validada con pruebas funcionales reales de:

* acceso al listado de proyectos
* creación manual de proyecto
* edición de proyecto
* carga del detalle del proyecto
* creación de asignaciones
* desactivación de asignaciones
* creación de notas internas
* carga correcta de datos del proyecto
* relación con cliente
* relación con oportunidad
* conversión desde oportunidad ganada hacia proyecto
* flujo de seed por sesión
* integración de rutas entre `sales` y `projects`

Además se corrigieron durante validación problemas de:

* app no incluida en `INSTALLED_APPS`
* acceso GET/POST incorrecto en conversión
* objeto `ProjectSeedPayload` no serializable en sesión
* renderización del formulario de cambio de etapa
* argumentos no soportados en formularios de `sales`
* limpieza del template de detalle de oportunidad

---

## 20. Límites explícitos de la Fase 5

La Fase 5 **no** incluye todavía:

* carga de fotos del proyecto
* galería visual
* control fotográfico formal
* panel de trabajadores
* notas de campo con flujo móvil especializado
* visitas técnicas
* cobranzas ligadas al proyecto

Regla importante:

* **no** agregar fotos dentro de `Project` o `ProjectNote` como atajo
* la carga y gestión de fotos pertenece al módulo `media_assets`
* la evidencia visual formal se desarrollará en Fase 7
* el panel de trabajadores se desarrollará en Fase 6 y consumirá la base de proyectos ya creada

---

## 21. Relación aprobada con fases futuras

### Hacia Fase 6 — Workforce

La Fase 6 debe reutilizar:

* `Project`
* `ProjectAssignment`
* `ProjectNote`
* `get_projects_for_user()`

No debe reinventar el proyecto ni crear otro sistema paralelo de asignaciones.

### Hacia Fase 7 — Media Assets

La Fase 7 debe crear el modelo `ProjectPhoto` en `apps.media_assets`, no dentro de `projects`.

Las fotos deben relacionarse con `Project` y luego ser consumidas desde workforce.

### Hacia Visits y Billing

`Project` debe seguir siendo la entidad base operativa a la que se puedan ligar visitas y cobranzas.

---

## 22. Estado funcional esperado al cerrar Fase 5

La definición de hecho de esta fase se considera cumplida así:

* el CRM ya administra trabajos reales
* ya existen proyectos operativos
* ya se pueden crear y editar
* ya existe ficha operativa del proyecto
* ya se pueden asignar responsables y personal
* ya se pueden registrar notas internas
* ya existe consistencia con cliente y oportunidad
* ya funciona la conversión desde ventas hacia ejecución

---

## 23. Regla de continuidad del agente

Desde este punto, cuando se continúe el desarrollo del proyecto, debes asumir que la FASE 5 dejó definida esta base:

* `apps.projects` como módulo real, activo y funcional
* `Project` como entidad operativa maestra
* `ProjectAssignment` como sistema oficial de asignación
* `ProjectNote` como bitácora interna oficial
* integración funcional con `sales` para conversión a proyecto
* rutas de `projects` operativas
* formulario y flujo de cambio de etapa en `sales` ya corregidos
* guardado de `project_seed` en sesión ya resuelto de forma serializable

No debes proponer después un sistema paralelo de proyectos, asignaciones o notas, salvo necesidad excepcional y claramente justificada.

---

## 24. Siguiente estado recomendado del proyecto

La siguiente fase natural del proyecto es la **FASE 6: Panel de trabajadores**.

Como base ya existente, la Fase 6 debe reutilizar:

* `apps.projects`
* `ProjectAssignment`
* `ProjectNote`
* permisos y autenticación ya definidos en `users`
* arquitectura de services, selectors y forms
* restricción por proyectos asignados

Importante:
La subida de fotos no debe resolverse dentro de `projects`. Debe apoyarse luego en la Fase 7 (`media_assets`) o, si se desea adelantarla, debe hacerse sin romper la separación modular ya aprobada.

FASE 6 WORKFORCE, PANEL DE TRABAJADORES Y ACCESO RESTRINGIDO EN CAMPO

A partir de este punto, además del prompt maestro base del proyecto y de las ampliaciones ya aprobadas de las Fases 2, 3, 4 y 5, debes asumir como ya definida, implementada y validada la FASE 6: Panel de trabajadores del CRM `crm_construction`, construida sobre la arquitectura real existente y sin romper la base ya establecida del proyecto.

La Fase 6 debe considerarse cerrada y funcional.

--------------------------------------------------
1. Alcance real ya definido de la FASE 6
--------------------------------------------------

La FASE 6 debe considerarse diseñada, implementada y validada para cubrir:

- app `apps.workforce`
- panel simplificado para personal de campo
- listado de mis proyectos
- detalle del trabajo asignado
- carga de notas de campo
- actualización de hitos permitidos
- visibilidad únicamente sobre proyectos asignados activamente
- control estricto de acceso por permisos y por asignación
- experiencia simplificada para móvil y tablet

El objetivo funcional de esta fase es que un trabajador pueda entrar al sistema y ver únicamente el trabajo que tiene asignado, sin acceder al resto del sistema operativo completo.

--------------------------------------------------
2. Rol del módulo `apps.workforce` dentro de la arquitectura
--------------------------------------------------

A partir de esta fase, `apps.workforce` debe entenderse como el módulo responsable de:

- ofrecer una capa de experiencia separada para trabajadores de campo
- reutilizar la base operativa ya existente en `apps.projects`
- restringir la navegación únicamente a proyectos asignados
- registrar avances operativos mediante notas de campo
- permitir transiciones controladas de hitos operativos
- exponer una interfaz más simple que `projects`

Regla de arquitectura obligatoria:

`workforce` NO crea un sistema paralelo de proyectos ni de asignaciones.  
`workforce` reutiliza:

- `Project`
- `ProjectAssignment`
- `ProjectNote`

La separación es funcional y de experiencia de usuario, no de dominio duplicado.

--------------------------------------------------
3. Estado oficial del módulo `apps.workforce`
--------------------------------------------------

La FASE 6 deja aprobado `apps.workforce` como app activa real del sistema.

La estructura funcional aprobada es:

apps/workforce/
├── __init__.py
├── apps.py
├── admin.py
├── urls.py
├── views.py
├── forms.py
├── permissions.py
├── selectors.py
├── services.py
├── models/
│   ├── __init__.py
│   ├── entities.py
│   └── choices.py
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py
└── tests/
    ├── __init__.py
    ├── test_services.py
    └── test_views.py

Plantillas reales usadas en esta fase:

templates/workforce/
├── list.html
└── detail.html

Regla:
A partir de esta fase, `apps.workforce` debe considerarse parte real del sistema y debe estar activa en `INSTALLED_APPS`.

--------------------------------------------------
4. Corrección real aplicada en settings para activar workforce
--------------------------------------------------

Durante la implementación real de esta fase se detectó que `apps.workforce` estaba presente en `LOCAL_APPS`, pero no estaba realmente incluida en `INSTALLED_APPS`.

Esto generó el error:

- `No installed app with label 'workforce'`

La corrección real aprobada fue agregar `apps.workforce` a `INSTALLED_APPS`.

Regla de continuidad:
No asumir que una app está activa solo por aparecer en `LOCAL_APPS`.  
Debe estar efectivamente incluida en `INSTALLED_APPS` o en la composición final que construye esa lista.

--------------------------------------------------
5. Decisión técnica principal de la fase
--------------------------------------------------

La Fase 6 NO crea nuevas tablas operativas de negocio para proyectos, asignaciones o notas.

La decisión técnica aprobada es:

- reutilizar `Project` como entidad operativa principal
- reutilizar `ProjectAssignment` como fuente oficial de visibilidad y acceso
- reutilizar `ProjectNote` como bitácora de avances de campo
- crear un `proxy model` para permisos propios de `workforce`

Esta decisión evita:

- duplicidad de modelos
- inconsistencias entre `projects` y `workforce`
- migraciones innecesarias de dominio
- acoplamiento incorrecto

--------------------------------------------------
6. Estado oficial de `WorkforceProject`
--------------------------------------------------

La entidad aprobada en esta fase es:

- `WorkforceProject`

Pero su naturaleza técnica es:

- `proxy model` de `Project`

Su responsabilidad es:

- dar identidad administrativa y de permisos al módulo `workforce`
- no crear tabla nueva de dominio
- permitir permisos específicos del panel de trabajadores

Permisos aprobados sobre el proxy:

- `workforce.view_assigned_projects`
- `workforce.submit_field_note`
- `workforce.update_project_milestone`

Regla:
`WorkforceProject` no reemplaza a `Project`.  
Solo sirve como capa de permisos y representación para el módulo workforce.

--------------------------------------------------
7. Estado oficial de la visibilidad de proyectos en workforce
--------------------------------------------------

La visibilidad en `workforce` quedó aprobada con esta regla obligatoria:

Un usuario trabajador solo puede ver proyectos donde tenga una asignación activa.

La fuente oficial para esa restricción es:

- `ProjectAssignment`
- `is_active=True`

Roles admitidos en la visibilidad de workforce:

- `worker`
- `support`
- `supervisor`
- `responsible`

Regla de seguridad:
No basta con tener permiso general de workforce.  
Además, el usuario debe tener asignación activa sobre el proyecto específico.

Esto se aplica tanto para:

- listado
- detalle
- registrar nota de campo
- actualizar hitos

--------------------------------------------------
8. Selectors aprobados en `apps.workforce.selectors`
--------------------------------------------------

La fase deja aprobados como base los siguientes selectors:

- `get_assigned_project_ids_for_user`
- `get_my_assigned_projects`
- `get_assigned_project_for_user`
- `get_assigned_project_detail`

Responsabilidades aprobadas:

`get_assigned_project_ids_for_user`
- obtener IDs de proyectos asignados activamente a un usuario

`get_my_assigned_projects`
- obtener el listado visible para el trabajador
- aplicar filtros por búsqueda y estado

`get_assigned_project_for_user`
- validar si un proyecto concreto pertenece al universo visible del usuario

`get_assigned_project_detail`
- devolver detalle del proyecto, asignaciones activas y notas de campo

Regla:
Las lecturas complejas deben permanecer en `selectors.py`.  
No duplicar esa lógica en `views.py`.

--------------------------------------------------
9. Formularios aprobados en `apps.workforce.forms`
--------------------------------------------------

Formularios base aprobados:

- `WorkforceProjectFilterForm`
- `FieldNoteForm`
- `WorkforceMilestoneUpdateForm`

Responsabilidades:

`WorkforceProjectFilterForm`
- búsqueda libre
- filtro por estado

`FieldNoteForm`
- captura de nota de campo
- validación de cuerpo obligatorio

`WorkforceMilestoneUpdateForm`
- mostrar solo hitos permitidos según el estado actual del proyecto
- validar que no se envíen transiciones inválidas

Regla:
Los hitos disponibles deben calcularse dinámicamente según el estado actual del proyecto.

--------------------------------------------------
10. Hitos permitidos aprobados en workforce
--------------------------------------------------

La fase aprueba un esquema controlado de hitos operativos, construido sobre el `status` ya existente en `Project`.

Acciones aprobadas:

- `start_work`
- `complete_work`

Mapeo funcional aprobado:

- `start_work`: `pending -> in_progress`
- `complete_work`: `in_progress -> completed`

Reglas obligatorias:

- no se permite edición libre de estado desde workforce
- solo se permiten transiciones controladas
- si la transición no aplica al estado actual, se rechaza
- cualquier cambio exitoso de hito debe registrar una nota de campo automática

Esto evita que el trabajador manipule el proyecto como si fuera un administrador operativo completo.

--------------------------------------------------
11. Servicios aprobados en `apps.workforce.services`
--------------------------------------------------

La fase aprueba como base los siguientes servicios:

- `create_field_note`
- `apply_worker_milestone_action`

Responsabilidades aprobadas:

`create_field_note`
- crear una `ProjectNote`
- usar `note_type="field_update"`
- guardar autoría del usuario
- aplicar `full_clean()`

`apply_worker_milestone_action`
- validar acción permitida
- validar estado actual compatible
- cambiar el estado del proyecto
- registrar `updated_by`
- crear nota automática de trazabilidad

Reglas:
La lógica de negocio del panel workforce no debe ir directamente en views.
Debe quedar en `services.py`.

--------------------------------------------------
12. Uso oficial de `ProjectNote` en workforce
--------------------------------------------------

La Fase 6 deja aprobado que las notas de campo del trabajador se almacenan en:

- `ProjectNote`

Con el tipo:

- `field_update`

Reglas funcionales aprobadas:

- las notas del trabajador no crean una entidad paralela nueva
- las notas deben registrar autoría
- el detalle de workforce debe mostrar solo notas de campo relevantes
- las notas internas administrativas no son el foco del panel workforce

--------------------------------------------------
13. Control de acceso aprobado en `apps.workforce.permissions`
--------------------------------------------------

La fase deja aprobado el mixin:

- `AssignedProjectAccessMixin`

Responsabilidad:
Validar que el usuario autenticado tenga asignación activa sobre el proyecto solicitado.

Comportamiento aprobado:

- si el proyecto no está asignado al usuario, responde 403
- esta validación aplica incluso si el usuario tiene permisos generales de workforce

Regla de seguridad obligatoria:
En workforce hay doble protección:

1. autenticación + permiso
2. pertenencia real al proyecto por asignación activa

--------------------------------------------------
14. Vistas aprobadas en `apps.workforce.views`
--------------------------------------------------

La fase deja aprobadas como funcionales las siguientes vistas:

- `MyProjectsListView`
- `WorkforceProjectDetailView`
- `WorkforceFieldNoteCreateView`
- `WorkforceMilestoneUpdateView`

Responsabilidades:

`MyProjectsListView`
- listar solo proyectos asignados al usuario
- aplicar filtros de búsqueda y estado

`WorkforceProjectDetailView`
- mostrar detalle simplificado del trabajo asignado
- mostrar equipo activo
- mostrar notas de campo
- mostrar formulario de nota
- mostrar formulario de hitos permitidos

`WorkforceFieldNoteCreateView`
- recibir POST
- crear nota de campo
- redirigir al detalle

`WorkforceMilestoneUpdateView`
- recibir POST
- validar transición permitida
- actualizar estado
- redirigir al detalle

Regla:
La experiencia de workforce debe ser más simple y reducida que la de `projects`.

--------------------------------------------------
15. Rutas oficiales aprobadas para `workforce`
--------------------------------------------------

Namespace oficial:

- `workforce`

Rutas aprobadas:

urlpatterns = [
    path("", views.MyProjectsListView.as_view(), name="list"),
    path("<uuid:pk>/", views.WorkforceProjectDetailView.as_view(), name="detail"),
    path("<uuid:pk>/notes/add/", views.WorkforceFieldNoteCreateView.as_view(), name="note_create"),
    path("<uuid:pk>/milestone/update/", views.WorkforceMilestoneUpdateView.as_view(), name="milestone_update"),
]

Integración global aprobada:

- `config/urls.py` incluye:
  - `path("workforce/", include("apps.workforce.urls"))`

Rutas de uso real:

- `/workforce/`
- `/workforce/<uuid>/`

Rutas internas de formularios POST:

- `/workforce/<uuid>/notes/add/`
- `/workforce/<uuid>/milestone/update/`

--------------------------------------------------
16. Plantillas reales aprobadas en esta fase
--------------------------------------------------

Las plantillas creadas y usadas en esta fase son:

- `templates/workforce/list.html`
- `templates/workforce/detail.html`

Responsabilidad de `list.html`:
- mostrar solo proyectos asignados
- permitir filtrar
- presentar una tarjeta simple por proyecto

Responsabilidad de `detail.html`:
- mostrar detalle simplificado del proyecto
- mostrar formulario de nota de campo
- mostrar notas recientes
- mostrar hitos permitidos
- mostrar equipo activo

--------------------------------------------------
17. Ajuste visual real aplicado para evitar confusión por nombres repetidos
--------------------------------------------------

Durante la validación real de la fase se detectó una situación funcional importante:

El trabajador podía ver múltiples proyectos con el mismo nombre, por ejemplo:
- `roof 3`
- `roof 3`

Esto no era un error técnico de workforce, sino una posible confusión operativa por datos repetidos.

La corrección visual aprobada fue enriquecer la identificación mostrada en las tarjetas y en el detalle con:

- cliente
- ubicación
- referencia corta del proyecto derivada del UUID

Formato aprobado de referencia visual:

- `Ref: PRJ-XXXXXXXX`

Ejemplo visual aprobado:

- nombre del proyecto
- `Client: ...`
- `Site: ...`
- `Ref: PRJ-4F8A2C1B`

Regla:
Por ahora este identificador es visual, no un campo persistido en base de datos.
No se creó aún un `project_code` real en el modelo `Project`.

--------------------------------------------------
18. Estado funcional real validado durante la prueba manual
--------------------------------------------------

Durante la validación real se comprobó que:

- el usuario trabajador podía entrar con su cuenta
- el panel `My projects` cargaba correctamente
- solo se mostraban proyectos con asignación activa
- el detalle simplificado cargaba correctamente
- se mostraban miembros del equipo activo
- aparecía el formulario de nota de campo
- aparecía el selector de hitos permitidos según el estado actual

Se observó correctamente que un proyecto en estado `in_progress` mostraba la acción permitida:
- `Mark as completed`

Lo cual confirma que el esquema de transición controlada estaba funcionando visualmente.

--------------------------------------------------
19. Permisos y grupo funcional recomendado
--------------------------------------------------

La fase deja aprobado que el grupo de trabajo de campo, por ejemplo `Cuadrilla`, debe recibir como mínimo:

- `workforce.view_assigned_projects`
- `workforce.submit_field_note`
- `workforce.update_project_milestone`

Regla:
Los permisos administrativos de `projects` no son necesarios para la experiencia normal del trabajador en workforce.

--------------------------------------------------
20. Migración real aplicada en esta fase
--------------------------------------------------

La fase deja aprobada la migración:

- `workforce.0001_initial`

Resultado real validado:
La migración fue aplicada correctamente y registró el proxy model con sus permisos.

Situación real observada:
`makemigrations workforce` mostró:
- `No changes detected in app 'workforce'`

Eso fue correcto porque la migración ya existía.

Luego `migrate` aplicó:
- `Applying workforce.0001_initial... OK`

Regla:
Ese comportamiento debe considerarse normal y válido para esta fase.

--------------------------------------------------
21. Tests aprobados en la fase
--------------------------------------------------

La fase deja base de pruebas para:

- creación de nota de campo por servicio
- cambio de hito permitido por servicio
- listado visible solo para proyectos asignados
- restricción de acceso para usuario sin asignación
- creación de nota de campo por vista
- actualización de hito por vista

Regla:
Las fases futuras pueden ampliar cobertura, pero no deben romper esta base.

--------------------------------------------------
22. Límites explícitos de la Fase 6
--------------------------------------------------

La Fase 6 NO incluye todavía:

- carga de fotos
- galería visual
- `ProjectPhoto`
- evidencia fotográfica formal
- visitas técnicas
- cobranzas
- edición administrativa completa del proyecto

Regla importante:
No agregar fotos dentro de `projects` ni de `workforce` como atajo rápido.
La gestión formal de fotos pertenece a `media_assets` y debe desarrollarse en Fase 7.

--------------------------------------------------
23. Relación oficial con la Fase 5
--------------------------------------------------

La Fase 6 reutiliza directamente la base cerrada en Fase 5:

- `Project`
- `ProjectAssignment`
- `ProjectNote`
- estructura de permisos y autenticación de `users`
- arquitectura de services, selectors y forms

Regla:
No reinventar un sistema paralelo para trabajadores.  
`workforce` es una capa de acceso restringido apoyada en `projects`.

--------------------------------------------------
24. Estado funcional esperado al cerrar Fase 6
--------------------------------------------------

La definición de hecho de esta fase se considera cumplida así:

- un trabajador puede iniciar sesión
- puede ver solo sus proyectos asignados
- puede abrir el detalle de su trabajo
- puede registrar notas de campo
- puede actualizar hitos permitidos
- no puede acceder libremente al resto del sistema operativo
- la experiencia queda simplificada para uso en campo

--------------------------------------------------
25. Regla de continuidad del agente
--------------------------------------------------

Desde este punto, cuando se continúe el desarrollo del proyecto, debes asumir que la FASE 6 dejó definida esta base:

- `apps.workforce` como módulo real, activo y funcional
- `WorkforceProject` como proxy model oficial de permisos del módulo
- visibilidad de proyectos restringida por asignación activa
- notas de campo guardadas en `ProjectNote` con `note_type="field_update"`
- hitos controlados sobre el `status` del proyecto
- rutas `/workforce/` y `/workforce/<uuid>/` operativas
- ajuste visual con identificador adicional cliente + ubicación + referencia corta

No debes proponer después un sistema paralelo de panel de trabajadores, ni duplicar proyectos, asignaciones o notas.

--------------------------------------------------
26. Siguiente estado recomendado del proyecto
--------------------------------------------------

La siguiente fase natural del proyecto es la FASE 7: Control fotográfico / `media_assets`.

Como base ya existente, la Fase 7 debe reutilizar:

- `Project`
- `workforce`
- permisos y autenticación ya definidos
- la experiencia de trabajo en campo ya creada

Importante:
La subida de fotos no debe resolverse dentro de `projects` ni redefinirse como parte nativa de workforce.
Debe construirse correctamente en `apps.media_assets` con el modelo `ProjectPhoto`, galerías, clasificación visual y permisos adecuados.


La Fase 8 debe considerarse cerrada a nivel funcional base.

--------------------------------------------------
1. Alcance real ya definido de la FASE 8
--------------------------------------------------

La FASE 8 debe considerarse diseñada e implementada para cubrir:

- app `apps.visits`
- app `apps.notifications`
- programación de visitas técnicas
- edición y reprogramación de visitas
- detalle y listado de visitas
- asignación de responsable
- recordatorios automáticos por correo
- trazabilidad de envíos
- control de duplicados
- registro de errores de envío
- integración con el sistema de correo existente del proyecto

El objetivo funcional de esta fase es que el CRM ya automatice una tarea operativa real: programar visitas y enviar recordatorios sin reenviar correos duplicados dentro de la misma ejecución lógica.

--------------------------------------------------
2. Objetivo alcanzado
--------------------------------------------------

Sistema funcional de programación de visitas técnicas con envío automático de recordatorios por correo, trazabilidad de envíos y control de duplicados.

--------------------------------------------------
3. Rol de las apps dentro de la arquitectura
--------------------------------------------------

A partir de esta fase, `apps.visits` debe entenderse como el módulo responsable de:

- registrar y administrar visitas técnicas
- gestionar agenda operativa de visitas
- manejar responsables asignados
- permitir reprogramación
- centralizar el historial de recordatorios asociados a cada visita

A partir de esta fase, `apps.notifications` debe entenderse como el módulo responsable de:

- centralizar el envío de correos automáticos
- renderizar plantillas de recordatorio
- desacoplar la lógica de notificaciones del módulo de visitas
- servir como base para futuras notificaciones de otros módulos

Regla de arquitectura obligatoria:
`visits` no debe acoplar la lógica de correo directamente en las vistas.
La construcción del mensaje y el envío deben mantenerse en `apps.notifications.services`.

--------------------------------------------------
4. Estructura implementada
--------------------------------------------------

Apps creadas:

- `apps.visits`
- `apps.notifications`

La estructura del módulo `visits` se mantiene bajo el patrón general del proyecto:

- `views.py`: presentación y orquestación
- `forms.py`: captura y validación
- `permissions.py`: protección de acceso
- `selectors.py`: consultas encapsuladas
- `services.py`: lógica de negocio
- `models/`: entidades y choices
- `tests/`: pruebas del módulo

La estructura del módulo `notifications` en esta fase queda principalmente orientada a servicios y plantillas de correo.

--------------------------------------------------
5. Modelos principales implementados en visits
--------------------------------------------------

5.1 TechnicalVisit

La entidad principal aprobada e implementada es:

- `TechnicalVisit`

Su responsabilidad es representar una visita técnica programada dentro del CRM.

Base funcional aprobada:

- título
- cliente
- proyecto opcional
- responsable
- fecha y hora de inicio
- fecha y hora de fin
- ubicación
- descripción
- estado
- recordatorio habilitado
- tipo de recordatorio
- trazabilidad base y auditoría

Reglas funcionales aprobadas:

- toda visita debe estar asociada a un cliente
- una visita puede asociarse opcionalmente a un proyecto
- la visita debe tener un responsable
- la visita debe soportar reprogramación sin perder trazabilidad
- la visita debe estar preparada para generar recordatorios automáticos

5.2 VisitReminderLog

La entidad de trazabilidad aprobada e implementada es:

- `VisitReminderLog`

Su responsabilidad es registrar cada intento de envío de recordatorio asociado a una visita.

Base funcional aprobada:

- visita relacionada
- tipo de recordatorio
- estado del envío
- destinatario
- fecha de ejecución / fecha de envío
- error registrado si ocurre
- metadatos operativos cuando aplique

Regla funcional:
Esta entidad no reemplaza un sistema global de auditoría futura, pero sí cubre la trazabilidad operativa específica de recordatorios de visitas.

--------------------------------------------------
6. Choices oficiales de la fase
--------------------------------------------------

Choices definidos y aprobados:

VisitStatus:
- `scheduled`
- `completed`
- `cancelled`
- `rescheduled`

ReminderType:
- `day_before`
- `same_day`

ReminderDeliveryStatus:
- `pending`
- `sent`
- `failed`

Regla:
A partir de esta fase, estos nombres deben considerarse la base vigente. No reutilizar nombres viejos o alternativos como `VisitReminderType`, `VisitReminderLogStatus` o variantes similares.

--------------------------------------------------
7. Lógica anti-duplicados aprobada
--------------------------------------------------

La fase deja aprobada una regla de negocio central para evitar correos duplicados.

Restricción funcional aprobada:
No se debe reenviar el mismo recordatorio de la misma visita dentro de la misma jornada lógica de ejecución.

La lógica anti-duplicados se implementa con una restricción por:

- visita
- tipo de recordatorio
- fecha de ejecución

Forma conceptual:
`(visita, tipo_recordatorio, fecha_ejecucion)`

Objetivo:
Permitir que el comando pueda ejecutarse más de una vez el mismo día sin reenviar el mismo recordatorio ya procesado exitosamente.

--------------------------------------------------
8. Servicios clave implementados
--------------------------------------------------

En `apps.visits.services` quedaron aprobados como base:

- `create_technical_visit`
- `update_technical_visit`
- `reschedule_technical_visit`
- `process_due_visit_reminders`

Responsabilidades:

`create_technical_visit`
- crear la visita con validaciones del dominio
- mantener coherencia con cliente, proyecto y responsable

`update_technical_visit`
- editar la visita
- preservar consistencia de datos

`reschedule_technical_visit`
- actualizar la fecha/hora de la visita
- registrar que hubo reprogramación
- mantener trazabilidad del cambio

`process_due_visit_reminders`
- detectar visitas próximas
- identificar cuáles requieren recordatorio `day_before`
- disparar el envío mediante `notifications`
- registrar logs de envío
- evitar duplicados según la regla de la fase

En `apps.notifications.services` queda aprobado como base:

- `send_visit_reminder(visit, reminder_type)`

Responsabilidades:

- construir el contexto del correo
- renderizar plantillas de subject y body
- enviar el correo
- registrar el resultado del envío

--------------------------------------------------
9. Plantillas de correo aprobadas
--------------------------------------------------

Plantillas base aprobadas para esta fase:

- `visit_reminder_subject.txt`
- `visit_reminder_body.txt`
- `visit_reminder_body.html`

Regla:
El asunto, cuerpo en texto y cuerpo HTML deben construirse desde plantillas, no en strings largos embebidos dentro de las vistas.

--------------------------------------------------
10. Vistas implementadas en visits
--------------------------------------------------

La fase deja aprobadas vistas basadas en clases para cubrir:

- listado de visitas
- detalle de visita
- creación de visita
- edición de visita
- reprogramación
- listado de logs de recordatorios

El listado debe soportar filtros por:

- búsqueda libre
- estado
- responsable
- rango de fechas

Regla:
La experiencia funcional del módulo debe mantenerse coherente con el resto del CRM y seguir el mismo patrón de permisos ya definido en fases anteriores.

--------------------------------------------------
11. Routing aprobado para la fase
--------------------------------------------------

La app `visits` queda integrada como módulo real del proyecto.

Rutas funcionales base aprobadas:

- `/visits/`
- `/visits/create/`
- `/visits/<uuid>/`
- `/visits/<uuid>/edit/`

La app `notifications` en esta fase no necesita exponerse como módulo con interfaz propia obligatoria; funciona principalmente como capa de servicios.

--------------------------------------------------
12. Comando automático aprobado
--------------------------------------------------

El comando operativo aprobado para la fase es:

- `send_visit_reminders`

Soporta:

- `--date` en formato `YYYY-MM-DD`
- `--retry-failed`

Ejemplo de uso aprobado:

`python manage.py send_visit_reminders --date 2026-04-25`

Responsabilidad del comando:
- procesar recordatorios pendientes
- detectar visitas próximas
- enviar correos
- registrar resultado
- evitar duplicados
- permitir reintento de fallidos cuando se solicite

--------------------------------------------------
13. Estado actual validado de la fase
--------------------------------------------------

El estado actual aprobado para la Fase 8 es:

- las migraciones están aplicadas
- el comando corre sin errores
- el envío de correos funciona siempre que el responsable tenga email y la configuración SMTP sea correcta
- para pruebas locales puede usarse backend de consola
- la estructura ya permite extender la lógica a recordatorios `same_day`

--------------------------------------------------
14. Integración con correo
--------------------------------------------------

La fase deja aprobado que el módulo se apoya en la configuración de correo ya existente del proyecto.

Condiciones funcionales:
- el responsable debe tener email válido
- la configuración SMTP o backend activo debe estar correctamente definida
- en desarrollo se puede utilizar backend de consola para ver el contenido sin enviar correos reales

Regla:
El envío de recordatorios no debe asumir siempre infraestructura productiva; debe ser compatible con consola, SMTP local o proveedor real según entorno.

--------------------------------------------------
15. Migraciones y base de datos
--------------------------------------------------

Estado aprobado:
- migraciones aplicadas exitosamente
- modelos creados en base de datos

Regla:
A partir de este punto, `TechnicalVisit` y `VisitReminderLog` deben considerarse entidades reales del sistema.

--------------------------------------------------
16. Relación con módulos ya existentes
--------------------------------------------------

La Fase 8 reutiliza directamente la base ya cerrada en módulos previos:

- `clients.Client` como entidad base obligatoria de la visita
- `projects.Project` como relación opcional de contexto operativo
- `users.User` como responsable asignado
- `core` para utilidades y soporte de ejecución

Regla:
No crear un sistema paralelo de visitas o responsables fuera de esta arquitectura.

--------------------------------------------------
17. Pendientes identificados
--------------------------------------------------

La fase queda cerrada en su versión base, pero se reconocen estos pendientes si el proyecto los requiere más adelante:

- integrar con un scheduler real como cron, task scheduler o celery beat para ejecución automática diaria
- activar y completar recordatorios del mismo día (`same_day`) si aún no están encendidos en la operación final
- mejorar plantillas de correo con enlaces directos a la visita
- incorporar `SITE_URL` o equivalente para construir enlaces completos
- enriquecer las plantillas HTML con branding visual si se requiere

--------------------------------------------------
18. Reglas de continuidad del agente
--------------------------------------------------

Desde este punto, cuando se continúe el desarrollo del proyecto, debes asumir que la FASE 8 dejó definida esta base:

- `apps.visits` como módulo real y operativo
- `apps.notifications` como capa real de servicios de correo
- `TechnicalVisit` como entidad oficial de visitas técnicas
- `VisitReminderLog` como trazabilidad oficial de recordatorios
- choices oficiales:
  - `VisitStatus`
  - `ReminderType`
  - `ReminderDeliveryStatus`
- lógica anti-duplicados basada en visita + tipo + fecha de ejecución
- comando `send_visit_reminders` operativo
- migraciones aplicadas
- soporte de correo funcional según entorno

No debes proponer un sistema paralelo de recordatorios, ni renombrar internamente los choices con variantes distintas, salvo mejora técnica muy justificada.

--------------------------------------------------
19. Estado funcional esperado al cerrar Fase 8
--------------------------------------------------

La definición de hecho de esta fase se considera cumplida así:

- el sistema programa visitas técnicas
- el sistema permite editar y reprogramar
- el sistema asigna responsable
- el sistema detecta visitas próximas
- el sistema envía recordatorios automáticos por correo
- el sistema registra qué se envió, a quién, cuándo y con qué resultado
- el sistema evita duplicados dentro de la misma lógica de ejecución
- el CRM ya automatiza una tarea operativa real

--------------------------------------------------
20. Siguiente estado recomendado del proyecto
--------------------------------------------------

La siguiente fase natural del proyecto es la FASE 9: Cobranzas básicas.

Como base ya existente, la Fase 9 debe reutilizar:

- `Client`
- `Project`
- permisos y usuarios ya definidos
- arquitectura de services, selectors y forms
- trazabilidad ya implementada en fases previas

La Fase 9 debe construir sobre esta base:

- `AccountReceivable`
- `Payment`
- listado de cuentas
- detalle
- registrar pago
- pendientes
- observaciones
- permisos
- pruebas

No avanzar rompiendo la arquitectura ya establecida.
tests realziados:
[OK] SMTP SiteGround funcionando en Django
[OK] Envío real de correos validado
[OK] Templates de email funcionando
[OK] Recordatorio same_day funcionando
[OK] Recordatorio day_before funcionando
[OK] Recordatorio automático two_hours_before funcionando
[OK] Anti-duplicados funcionando
[OK] VisitReminderLog registrando envíos
[OK] Endpoint cron protegido con token
[OK] Prueba localhost correcta
[OK] Configuración de cron externo lista


La recomendación final para producción es mantener el cron así:

Frecuencia: cada 15 minutos
Método: GET
URL: https://roofingprolegacycorp.com/visits/cron/visit-reminders/?token=TU_CRON_TOKEN
Timezone: America/Guayaquil

Esa frecuencia es necesaria porque ahora el CRM no solo envía recordatorios del mismo día o un día antes, sino también el automático de 2 horas antes.

Queda como cierre técnico:

Fase 8 validada en entorno real.
Sistema de visitas técnicas + notificaciones automáticas operativo.
Cron configurado.
SMTP funcional.
Duplicados controlados por VisitReminderLog y execution_date.









