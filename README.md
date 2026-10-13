# Actualización de especificaciones — App de preparación del examen de grado

Este paquete consolida las decisiones confirmadas más recientes en los documentos de especificación afectados.

## Decisiones confirmadas

**Producto y reglas de negocio**

- Jurisdicción configurable; cada materia tiene sus propios subtemas.
- Roles mínimos: estudiante y administrador. Quien crea o modifica una versión de contenido no puede aprobarla ni publicarla; debe hacerlo otro administrador.
- Retroalimentación oral elegida por el estudiante antes de iniciar: después de cada pregunta o al final.
- La simulación tiene tiempo total y tiempo individual por pregunta. Una simulación contiene un solo tipo de pregunta (oral o alternativas); la práctica de alternativas es independiente.
- Al expirar el tiempo total, no se puede iniciar otra pregunta; la pregunta activa puede terminar dentro de su límite individual y puede solicitar extensiones válidas. Al terminar, la sesión queda `completed`. La pregunta termina al completarse la evaluación de su respuesta, y no se inicia otra mientras la anterior se procesa.
- Al expirar el tiempo individual, el estudiante dispone de 15 segundos para solicitar una extensión de 60 segundos; ese lapso consume tiempo total. El máximo es 1 extensión por pregunta. El nuevo límite de la pregunta es la hora de concesión + 60 s, de modo que el estudiante dispone siempre de 60 s completos.
- El tiempo de transcripción y evaluación no se descuenta al estudiante: el reloj de la pregunta y el reloj total se detienen cuando el backend recibe la respuesta; el total se reanuda cuando termina (o falla) la transcripción y evaluación.
- La desconexión se detecta con un latido del cliente cada 10 segundos; sin latido durante 30 segundos, el backend pausa el reloj de forma retroactiva desde el último latido. La sesión puede reanudarse desde el último estado guardado, con el tiempo restante, dentro de 30 minutos. Si no se reanuda en ese plazo, queda `expired`. La ventana de 30 minutos se cuenta desde el último latido recibido.
- Si hay una grabación en curso o sin transcribir al desconectarse, se descarta el audio temporal y el estudiante vuelve a grabar con el tiempo restante de la pregunta.
- Pausa voluntaria: solo entre preguntas (sin pregunta activa), de hasta 30 segundos y una vez por simulación. Al vencer, el reloj se reanuda automáticamente.
- Un administrador solo puede corregir un resultado a partir de un reporte vinculado. La corrección conserva el original.
- El estudiante puede reportar preguntas o evaluaciones; un administrador revisa el reporte. Toda corrección debe mantener trazabilidad.
- El plan de estudio conserva un plan original y permite recalcularlo adaptativamente. La prioridad se calcula con una regla determinista: peso de la materia en el programa × brecha de desempeño reciente.
- Voz por turnos en el MVP, con arquitectura preparada para voz en tiempo real en una etapa posterior.
- La evaluación oral usa una escala de 1 a 7. No es una calificación académica oficial.
- Se conservan transcripciones y resultados durante 12 meses; el audio original no se conserva. El audio temporal se elimina al terminar la transcripción, con un tope de seguridad de 1 hora para restos.
- Documentos importables: PDF, DOCX y TXT, de hasta 25 MB.
- RAG recupera fuentes jurídicas y material académico aprobado; el contenido generado por IA requiere revisión humana antes de publicarse.
- Cuotas de IA iniciales, configurables y reajustables con datos reales de costo: 5 simulaciones orales por día y 100 por mes por usuario, con alerta al 80 % y un error claro al alcanzar el límite.
- `abandoned`: la sesión pasa a este estado cuando el estudiante la cierra voluntariamente sin terminar. Las respuestas ya evaluadas se conservan y las pendientes no puntúan.
- Cuentas: contraseña de mínimo 12 caracteres con hash Argon2id, sin reglas de composición y con bloqueo de contraseñas comunes; correo verificado antes de usar la cuenta; recuperación con enlace de un solo uso que caduca a los 30 minutos.
- Escala 1 a 7: cada criterio se puntúa de 0 a 100, se pondera según la rúbrica y el total se convierte linealmente a 1,0–7,0 con un decimal.
- Eliminación a solicitud: el estudiante la pide desde su perfil y se borran transcripciones y resultados en un máximo de 30 días, conservando solo un registro de auditoría sin contenido.
- La interfaz debe ser responsive desde la primera versión.
- Suscripción mensual con Mercado Pago ("Suscripciones sin plan asociado" con pago pendiente): $9.990 CLP al mes, con 7 días de prueba gratis. El estudiante paga en la página de Mercado Pago; la aplicación nunca recibe ni guarda datos de tarjeta. Sin suscripción activa, el estudiante solo puede usar su cuenta, ver el panel, suscribirse y enviar comentarios; todo el estudio (práctica, simulación y plan) requiere suscripción. Los administradores no requieren suscripción. Precio y días de prueba son configuración.

**Stack e infraestructura**

- Frontend: Next.js + TypeScript. Backend: FastAPI + Python 3.12, gestionado con uv (imagen Docker `python:3.12-slim`).
- Base de datos: PostgreSQL, con SQLAlchemy y Alembic.
- Índice RAG: pgvector sobre PostgreSQL, a validar con una prueba de concepto.
- Autenticación propia con correo y contraseña, implementada en el backend, más ingreso con Google (OpenID Connect); un correo verificado por Google se vincula automáticamente a la cuenta existente. Sesión en cookie HttpOnly con token opaco guardado (como hash) en PostgreSQL y revocable; 7 días de inactividad o 30 días máximo. Registro abierto de estudiantes; administradores creados por consola. Verificación de correo con enlace de un solo uso de 24 h. Bloqueo temporal de 15 min tras 10 intentos fallidos en 15 min.
- Hosting del frontend: Vercel. Base de datos: Neon (PostgreSQL con pgvector).
- Almacenamiento temporal de importaciones: Vercel Blob. Cola de tareas: tabla en PostgreSQL (Neon) detrás de una interfaz.
- Backend FastAPI en Render (Docker); frontend en Vercel. Dominio: apruebatuexamen.cl (comprado en NIC Chile; DNS delegado a Vercel). El frontend reenvía `/api` al backend de Render.
- Correo (verificación y recuperación de cuenta): Resend, remitente `no-reply@apruebatuexamen.cl` (DKIM, SPF y DMARC en el DNS de Vercel). En desarrollo se imprime en consola; en producción el envío real es obligatorio.
- Marca visible: "Aprueba tu examen" (dominio apruebatuexamen.cl). El nombre no constituye una garantía: se mantiene visible que las evaluaciones son orientativas y no garantizan la aprobación.
- Observabilidad: OpenTelemetry, sin datos personales ni audio en logs.
- Entorno local de desarrollo: Docker para PostgreSQL y backend.
- Proveedores de IA (modelo de lenguaje, transcripción, embeddings y síntesis de voz): se eligen tras una prueba de concepto. Criterio: menor costo, siempre que la calidad en respuestas jurídicas sea aceptable y se revise la retención de datos del proveedor. Mientras tanto se usan implementaciones falsas detrás de interfaces.

## Archivos

- `specs/01-functional-requirements.md`: requisitos funcionales y reglas de negocio.
- `specs/02-domain-model.md`: entidades, estados y relaciones relevantes.
- `specs/03-architecture.md`: componentes, voz, RAG, costos y recuperación de sesión.
- `specs/05-acceptance-criteria.md`: criterios verificables de aceptación.
- `specs/06-voice-study-planning-rag.md`: especificación de voz, planificación, RAG y responsive.
- `AGENTS.md`: instrucciones para agentes de desarrollo.
- `harness/quality-gates.md`: controles de calidad que deben pasar antes de aceptar una tarea.
- `docs/correcciones.md`: registro de correcciones y decisiones.
- `docs/despliegue.md`: cómo están armados desarrollo y producción, variables de entorno y despliegue.

Nota de numeración: este paquete no incluye `specs/04-*.md` porque solo contiene los documentos afectados. Si existe un `04`, debe revisarse contra estas decisiones.

## Pendientes explícitos

Lista única de decisiones abiertas. No se deben inventar valores para ellas.

1. ~~Hosting de producción del backend~~ Resuelto: Render.
2. ~~Proveedor de correo de producción~~ Resuelto: Resend.
3. Candidatos y proveedores concretos de IA (modelo de lenguaje, transcripción, embeddings y síntesis de voz) y el umbral de calidad aceptable que usará la prueba de concepto.
4. Estado de un `QuestionAttempt` cuando falla la transcripción o la evaluación, y si el estudiante puede reintentar. El modelo no define un estado para ese caso. Lo único confirmado es que el reloj total se reanuda al fallar el procesamiento y que una falla técnica no se convierte en nota.
5. Acceso tras cancelar la suscripción: si se mantiene hasta el fin del periodo pagado o termina de inmediato. Mientras no se decida, el acceso existe solo mientras Mercado Pago informa la suscripción como `authorized`.
6. Credenciales de Mercado Pago (cuenta vendedora, credenciales de prueba y de producción) y URL pública para recibir webhooks.
7. Obligaciones tributarias y de consumidor del cobro (boleta electrónica, derecho a retracto, reembolsos): requieren revisión con un asesor antes de cobrar.

Los parámetros ya decididos (extensiones, ventana de recuperación, latido, pausa, retención, cuotas) se implementan como configuración con el valor confirmado, no como constantes en el código.
