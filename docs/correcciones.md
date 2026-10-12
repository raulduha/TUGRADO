# Registro de correcciones a las especificaciones

Fecha: 2026-10-12. Alcance: README, AGENTS, specs/01 a 06 y harness/quality-gates.

## A. Correcciones de consistencia entre documentos

1. **Falta `specs/04`.** El README aclara que el paquete solo incluye los documentos afectados por las decisiones confirmadas.
2. **Contradicción en pendientes con valor (extensiones y ventana de recuperación).** Se decía que no podían ser ilimitados ni codificarse. Ahora son parámetros de configuración obligatorios, sin valor por defecto; producción no despliega si faltan. Archivos: README, AGENTS, FR-011, FR-012, AC-014, Gate 3, 03, 06.
3. **Listas de pendientes distintas.** Se creó una lista única en el README (puntos 1 a 23) y `03-architecture.md` §10 remite a ella.
4. **Pendientes técnicos ausentes de la lista única.** Se agregaron los puntos 19 a 23: base de datos y migraciones, autenticación, almacenamiento y colas, hosting y observabilidad, índice RAG.
5. **Rol "editor" inexistente.** Se eliminó de FR-013. Los permisos granulares dentro de `administrator` quedan como pendiente 11.
6. **Aprobar y publicar usados como sinónimos.** FR-014 los separa. `QuestionVersion` tiene estados `draft`, `in_review`, `approved`, `published`, `retired`. La revisión aplica también a rúbricas, fuentes y documentos RAG.
7. **Rúbrica sin vínculo a la pregunta.** FR-007 y el dominio la referencian desde `QuestionVersion`.
8. **Sin tipo de pregunta ni sesión de práctica.** Se agregó el tipo (`multiple_choice`, `oral`) y la entidad `PracticeAttempt`.
9. **Reportes limitados a preguntas.** `QuestionReport` pasó a `ContentReport`, con vínculo a pregunta, explicación o evaluación (FR-016).
10. **Correcciones sin reglas claras.** FR-018: los agregados se derivan del resultado vigente y el original se conserva; sin reporte previo no hay corrección (pendiente 12).
11. **Estado de pausa sin retorno.** `SimulationSession` guarda `resume_state` para volver, por ejemplo, a `awaiting_current_question_completion`.
12. **Audio en curso al desconectarse.** FR-012 y la arquitectura aclaran que el audio temporal no se restaura (tratamiento pendiente 9).
13. **Alternativa textual sin criterio.** FR-025 la exige y se creó AC-027.
14. **Alertas de riesgo y tareas atrasadas sin criterio.** AC-019 las incorpora.
15. **AC-025 redundante.** Quedó como complemento específico de AC-004 y AC-012 para contenido generado por IA.
16. **Gates dependientes de políticas no definidas.** AC-010 y Gate 5 se pueden ejecutar sin la política de retención: se verifica que el audio no se persiste y que los plazos son configurables.

## B. Decisiones registradas (ronda de preguntas del 2026-10-12)

**Tiempo y sesión:** máximo 1 extensión por pregunta; ventana de oferta de 15 s que cuenta en el tiempo total; recuperación de 30 minutos; latido cada 10 s con caída a los 30 s (pausa retroactiva); estado final `completed` (`expired` para sesiones no reanudadas a tiempo); extensiones permitidas tras el tiempo total; el tiempo de procesamiento no se descuenta (el reloj se detiene al recibir la respuesta); grabación interrumpida se vuelve a grabar; pausa voluntaria solo entre preguntas, 30 s, una vez por simulación.

**Contenido y permisos:** un solo tipo de pregunta por simulación; separación de autor y aprobador; correcciones solo con reporte vinculado; documentos PDF, DOCX y TXT de hasta 25 MB; escala de evaluación de 1 a 7.

**Datos:** retención de 12 meses; audio temporal eliminado al terminar la transcripción (tope de 1 hora); cuotas configurables sin valor fijo; prioridad del plan = peso de la materia × brecha de desempeño.

**Infraestructura:** PostgreSQL + SQLAlchemy + Alembic; pgvector; autenticación propia (correo y contraseña); almacenamiento y cola gestionados en la nube; OpenTelemetry; Docker en local; proveedores de IA tras prueba de concepto.

Se añadieron AC-028 a AC-031 y reglas en los gates 2, 3 y 5.

## C. Segunda ronda de decisiones

- `abandoned`: cierre voluntario sin terminar.
- Hosting: frontend en Vercel; base de datos en Neon; archivos en Vercel Blob; cola como tabla en PostgreSQL.
- Contraseñas: mínimo 12 caracteres, Argon2id, correo verificado, recuperación con enlace de un solo uso de 30 minutos.
- Escala 1 a 7: conversión lineal ponderada con un decimal.
- Eliminación a solicitud: autoservicio, en un máximo de 30 días, con registro de auditoría sin contenido.
- Cuotas iniciales: 5 simulaciones orales por día y 100 por mes por usuario, alerta al 80 %.
- Criterio para elegir proveedores de IA: menor costo con calidad aceptable.
- Se añadieron AC-032 a AC-035.

## D. Pendientes que siguen abiertos

1. Hosting de producción del backend (Railway o Render; hoy solo local con Docker).
2. Proveedor de correo de producción (en desarrollo, consola).
3. Candidatos y proveedores de IA, y el umbral de calidad de la prueba de concepto.

## E. Observaciones de entorno (no son cambios en las specs)

- El paquete original estaba en `Downloads\grado-derecho-specs`, fuera del repo, y se copió a `TUGRADO`. Una versión anterior de este registro mencionaba una fusión a `main` en el commit `ce32231`, pero ese commit no existe en el repositorio. Las specs se incorporan en la rama `specs/base`.
- No había rutas de usuario dentro de los documentos.
- Entorno verificado el 2026-10-12: Docker 28.0.4 con Compose v2.34 en ejecución, Python 3.12 disponible vía uv, Node 24 con npm y pnpm. No hay bloqueos para ejecutar el backend y PostgreSQL en local.

## F. Tercera ronda de decisiones

- Backend en Python 3.12, gestionado con uv; imagen Docker `python:3.12-slim`.

## G. Cuarta ronda de decisiones (reglas de tiempo de la sesión)

- Extensión: el nuevo límite de la pregunta es la hora de concesión + 60 s (no el límite original + 60 s).
- Procesamiento: al recibir la respuesta se detienen el reloj de la pregunta y el total; el total se reanuda cuando termina o falla la transcripción y evaluación. Entre preguntas el reloj total corre.
- Recuperación: la ventana de 30 minutos se cuenta desde el último latido recibido.
- `docs/index.html` no refleja las secciones F y G; debe regenerarse desde las specs.

## H. Interpretaciones confirmadas (2026-10-12)

- La sesión pasa a `completed` cuando termina la evaluación de la última respuesta (o vence la pregunta), no al recibir la respuesta.
- No se puede iniciar otra pregunta mientras la anterior se procesa.

## I. Quinta ronda de decisiones (autenticación, 2026-10-12)

- Sesión: cookie HttpOnly/Secure/SameSite=Lax con token opaco; sesión guardada en PostgreSQL (hash) y revocable. El frontend reenvía `/api` al backend (mismo origen) y el backend valida `Origin` en operaciones que modifican datos.
- Duración: 7 días sin actividad o 30 días desde el inicio.
- Registro abierto de estudiantes; administradores creados con un comando de consola.
- Enlace de verificación de correo: un solo uso, 24 horas.
- Bloqueo temporal: 15 minutos tras 10 intentos fallidos en 15 minutos.
- Se añadió AC-036.

## J. Sexta ronda (frontend y comentarios, 2026-10-12)

- La interfaz usa un tema claro y cálido para todos, sin cambiar a oscuro según el sistema (pedido del usuario: "amigable").
- El panel muestra la ruta del estudiante con su estado real y tarjetas de progreso con estados vacíos hasta que existan datos; no se muestran cifras inventadas.
- Nueva casilla de comentarios de usuarios (FR-028, AC-037, entidad `UserFeedback`).

## K. Séptima ronda (suscripción, 2026-10-12)

- Suscripción mensual con Mercado Pago, $9.990 CLP, 7 días de prueba, todo el estudio bloqueado sin suscripción; administradores exentos.
- Integración: "Suscripciones sin plan asociado" con pago pendiente (`init_point`), porque la variante con plan exige tokenizar la tarjeta en el sitio.
- Firma de webhooks: HMAC-SHA256 de `id:{data.id};request-id:{x-request-id};ts:{ts};`, igual que el SDK oficial de Python.
- Pendientes nuevos (README 5 a 7): acceso tras cancelar, credenciales y URL pública de webhooks, obligaciones tributarias y de consumidor.
- Por validar en el entorno de prueba de Mercado Pago: si `free_trial` en días se acepta en suscripciones sin plan, si el correo del pagador debe coincidir con su cuenta de Mercado Pago, y la configuración de webhooks para suscripciones (la documentación es contradictoria).
- Se añadieron FR-029 a FR-031, AC-038, AC-039, las entidades `Subscription` y `BillingEvent`, y el Gate 11b.

## L. Despliegue (2026-10-12)

- Frontend en Vercel (`vercel.json` con un solo servicio, `frontend`); backend en Render con Docker. Se resuelve el pendiente 1.
- Dominio apruebatuexamen.cl, comprado en NIC Chile.
