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

## M. Marca y correo (2026-10-12)

- Marca visible "Aprueba tu examen" (antes TUGRADO en la interfaz; el código y el repo conservan el nombre interno). Como el nombre podría leerse como promesa, se mantiene el aviso de que las evaluaciones son orientativas y no garantizan la aprobación (AGENTS.md).
- Correo con Resend (región São Paulo): registros DKIM `resend._domainkey`, SPF `send` y `rsend` (CNAME) y DMARC `_dmarc` (p=none) creados en el DNS de Vercel. Se resuelve el pendiente 2.
- Un fallo del proveedor de correo no interrumpe el registro ni revela si la cuenta existe; se registra sin destinatario y el estudiante puede pedir el reenvío.

## N. Ingreso con Google (2026-10-13)

- Pedido del usuario: ingresar con Google. Decisiones (recomendadas y aceptadas): se vincula automáticamente con la cuenta existente si Google declara el correo verificado, y se mantiene el registro con correo y contraseña.
- Flujo OpenID Connect con código de autorización, PKCE, `state` y `nonce`; el `id_token` se valida con las claves públicas de Google (firma, emisor, audiencia y vencimiento).
- Se añadieron FR-001b, AC-040 y la entidad `UserIdentity`.

## O. Prueba gratis obligatoria y acceso de cortesía (2026-10-13)

- Pedido del usuario: al crear la cuenta hay que ingresar la tarjeta (prueba gratis de 7 días en Mercado Pago) para entrar; sin eso no se ve el panel. Cambia la decisión de la séptima ronda, en la que el panel era visible sin suscripción.
- Las cuentas que autorice el equipo (pruebas, desarrollo) pueden entrar sin pagar: acceso de cortesía otorgado desde el CLI con motivo y responsable, revocable sin borrar el registro.
- Por validar en el entorno de prueba de Mercado Pago: que la prueba gratis pida el medio de pago y no cobre durante los 7 días.
- Se añadieron FR-032, AC-041 y la entidad `AccessGrant`; se ajustaron FR-030 y AC-038.

## P. Correo de la cuenta de Mercado Pago (2026-10-13)

- En las pruebas, Mercado Pago rechazó crear la suscripción: el correo del pagador (`payer_email`) debe corresponder a la cuenta que paga, y los usuarios de prueba solo pueden pagar a vendedores de prueba.
- Decisión del usuario (entre pedir el correo o migrar a suscripciones con plan): la pantalla de suscripción pide el correo de la cuenta de Mercado Pago, con el de la app por omisión. Se guarda en `Subscription.payer_email`.
- Confirmado con la API de prueba: la prueba gratis de 7 días se acepta (`free_trial` en días; primer cobro desplazado 7 días).
- Al quedar activa la suscripción se envía un correo de confirmación a la cuenta (no al correo de Mercado Pago): con prueba gratis indica la fecha del primer cobro y que cancelar antes evita el cobro; Mercado Pago envía además su propio comprobante.
- La pantalla de suscripción consulta a Mercado Pago si hay un pago pendiente, para activarlo aunque el webhook no llegue.

## Q. Mapa de estudio y Apruvi (2026-10-13)

- Pedido del usuario: reemplazar la ruta genérica del panel por un mapa de estudio tipo juego 2D, con una mascota propia, "Apruvi", que habla en cada nivel, avanza por el mapa y respira con naturalidad.
- Los niveles siguen el recorrido de las specs (materias, plan, práctica, simulación oral, refuerzo adaptativo, simulacro, examen). Solo el primero, la cuenta, aparece completado; los demás dicen "Próximamente" hasta que existan. Los mensajes de Apruvi no prometen aprobar el examen.
- Las animaciones se desactivan con `prefers-reduced-motion`.

## R. Rachas (2026-10-13)

- Pedido del usuario: rachas con fueguito, celebración por conectarse a diario y un correo de ánimo tras un par de días sin entrar.
- Hecho: registro diario idempotente (`ActivityDay`), racha actual y mejor racha, los últimos 7 días y celebración con Apruvi en la primera visita del día (FR-033, AC-042). "Días seguidos estudiando" pasó a la tarjeta "Tu racha".
- Pendiente: el correo de ánimo. Necesita una tarea programada y una forma de darse de baja; el mensaje anima sin prometer la aprobación.

- Correo de ánimo (FR-034, AC-043). Decisiones del usuario: Vercel Cron, que es gratis, y un solo correo cuando el estudiante lleva 2 días sin entrar, con enlace de baja y `List-Unsubscribe`. Se ejecuta a las 13:00 UTC (10:00 en Chile en horario de verano).

## S. Vistas previas con datos de ejemplo (2026-10-13)

- Pedido del usuario: mientras no estén las preguntas reales, "todo lo de datos" va como mockup.
- `/practica`, `/simulacion` y `/plan` son vistas previas solo de frontend, sin backend ni persistencia, con un aviso visible de datos de ejemplo. Se llega a ellas desde el mapa de estudio ("Probar (vista previa)").
- La práctica usa 5 preguntas de ejemplo sobre normas verificables (Código Civil arts. 2, 6–7, 26 y 74; Constitución art. 25), con su fuente. No es contenido revisado ni publicado (FR-013/014 siguen pendientes).
- La simulación no usa el micrófono ni IA (pendiente 3). Sí aplica las reglas decididas: modo de retroalimentación fijado al comenzar, tiempo de procesamiento sin descuento y escala 0–100 ponderada a 1,0–7,0 con un decimal.
- El plan muestra la regla de prioridad decidida (peso × brecha), los estados de las tareas y el plan original conservado como línea base.
- Siguen abiertas: dificultad, materias o cedulario, número de alternativas y proveedores de IA.

## T. Banco de preguntas (2026-10-13)

- Decisión del usuario: dificultad de 1 a 3. El importador acepta entre 2 y 5 alternativas mientras no se fije un número.
- Implementado: `Question` y `QuestionVersion` inmutable (draft → in_review → approved → published → retired), `AnswerOption`, `ContentReview`, auditoría en `content_event` y `PracticeAttempt`. Editar crea la versión siguiente. Publicar retira la versión publicada anterior. Quien crea una versión no la aprueba ni la publica (AC-029).
- Importación desde la plantilla Excel, todo o nada con errores por fila (AC-044). Panel `/admin/preguntas`.
- `/practica` usa las preguntas publicadas y vuelve a las de ejemplo solo si no hay ninguna.
- Aún no se modelan la jurisdicción ni el programa de estudio; quedan para cuando estén las materias reales. La edición desde el panel tampoco existe todavía: solo está el endpoint.

## U. Herramientas de administrador: simular estudiante (2026-10-14)

- Pedido del usuario: una herramienta tipo "cheat code" para que los administradores recorran el journey de un estudiante con cualquier porcentaje de avance.
- Botón flotante solo para administradores en el panel. Ajusta el avance del mapa, los días de racha y tiene atajos (Nuevo, A mitad de camino, Listo para el examen).
- Es solo visual: se guarda en el navegador del administrador, no toca la base de datos y ningún estudiante lo ve. Mientras está activa, el panel muestra "Modo simulación" y las estadísticas dicen "Dato simulado".

## V. La prueba gratis cobraba al autorizar (2026-10-23)

- Reporte del usuario: en producción, Mercado Pago cobró los $9.990 apenas se autorizó la suscripción, pese a anunciar 7 días gratis. La prueba de §P (`free_trial` en días, primer cobro desplazado) se hizo con la API de prueba y no se repite en producción en suscripciones sin plan asociado.
- Corrección: ya no se envía `free_trial`. El primer cobro se fija con `auto_recurring.start_date` = creación del pago pendiente + `BILLING_TRIAL_DAYS`. Un pago pendiente de más de una hora no se reutiliza: se cancela y se crea otro, para que la prueba se cuente completa desde que el estudiante paga.
- Por validar en producción: que el primer cobro ocurra en `start_date` y no al autorizar. A quienes ya se les cobró durante la prueba hay que revisarlos en el panel de Mercado Pago (reembolso a decidir por el equipo).

## W. Banco de preguntas en Excel de ida y vuelta (2026-10-24)

- Pedido del usuario: que el administrador pueda agregar y sacar preguntas descargando una planilla base, completándola y volviéndola a subir.
- `/admin/preguntas` descarga la plantilla vacía (`GET /admin/questions/template`) o el banco actual (`GET /admin/questions/export`: última versión de cada pregunta no retirada, con su id y estado). La planilla suma las columnas opcionales `id`, `estado` (informativa) y `retirar`; la plantilla antigua sigue sirviendo.
- Al subir: fila sin id = pregunta nueva; con id y cambios = versión siguiente en borrador (la publicada sigue visible hasta publicar la nueva); con «sí» en `retirar` = se retiran todas sus versiones vigentes; sin cambios = nada. Todo o nada, con errores por fila (AC-044 actualizado).
- Decisión de diseño: quitar una fila de la planilla no retira la pregunta, para que un descuido no saque contenido; para sacarla hay que marcar `retirar`. Retirar ahora procede desde cualquier estado (antes solo desde `published`) y queda en `content_event`.

## X. Ruta de estudio tipo Duolingo y guía del temario (2026-10-24)

- Pedido del usuario: con las preguntas y la guía de lo que entra en el examen, armar un recorrido tipo Duolingo.
- `/temario` (pública): las 19 cédulas UC (2 obligatorias, 16 electivas, 1 suspendida) con sus partes y temas y enlace a cada PDF oficial. Es un índice; aclara que otras universidades tienen su propio cedulario.
- `/ruta`: una unidad por materia y lecciones de 5 o más preguntas (subtemas consecutivos), en el orden en que se importó la planilla (las filas importadas reciben horas correlativas para conservarlo). Desbloqueo secuencial por unidad, estrellas (3/2/1 según el último intento) y XP (10 por respuesta correcta). Nuevos `GET /practice/path` y `GET /practice/lessons/{id}`; criterios en FR-006 y AC-045.
- El nivel «Practica con alternativas» del mapa del panel pasó a «Tu ruta de estudio» y lleva a `/ruta`.
- Acciones masivas en `/admin/preguntas` (`POST /admin/questions/bulk`): enviar a revisión, aprobar o publicar todas las del filtro; cada una con sus reglas (quien creó no aprueba ni publica) y se informan las que no avanzan.
- Decisión de diseño: el orden y el desbloqueo son pedagógicos, no un permiso: el backend entrega cualquier lección a quien tenga acceso al estudio.

## Y. CRUD de preguntas en el panel, refactor del banco y panel en celular (2026-10-24)

- Pedido del usuario: que el administrador pueda crear, editar y sacar preguntas una a una, de forma ordenada y sin rehacer todo; que funcione en celular; y un refactor legible con pruebas que verifiquen lo necesario.
- Panel `/admin/preguntas`: «Nueva pregunta» (formulario), «Editar» (guarda la versión siguiente en borrador), «Descartar esta versión», «Retirar la pregunta completa» (ambos con confirmación), historial de versiones, búsqueda por enunciado o subtema, filtro por materia y estado, y «Cargar más». En celular el detalle se abre a pantalla completa. Nuevos `POST /admin/questions`, `POST /admin/questions/{id}/retire-question` y `GET /admin/questions/subjects`; el detalle incluye `history`; la lista acepta `q`, `subject` y `offset`. Retirar una versión procede desde cualquier estado vigente (AC-046).
- Refactor: `app/api/content.py` se dividió en `questions.py` (administración) y `practice.py` (estudiante); `importer.py` y `workbook.py` se unieron en `spreadsheet.py` (formato) y la aplicación al banco pasó a `sync.py`; las lecturas a `queries.py`; la validación del contenido quedó en un solo lugar (`question.py`), común al formulario y a la planilla. Los métodos del servicio ya no confirman la transacción: lo hace quien los llama, así la planilla se aplica completa o no se aplica.
- Pruebas reorganizadas por tema (formato, flujo editorial, planilla contra el banco, práctica), con nombres que dicen la regla y sin pruebas que solo validan el framework. Se comprobó que fallan al romper a propósito tres reglas (quien crea aprueba, ids desconocidos, umbral de estrellas).
- Celular: el encabezado con sesión mostraba el logo completo además del ícono y desplazaba la página; ahora en pantallas chicas muestra solo el ícono. El e2e del admin revisa 390 px en el panel, la ruta y una lección.

## Z. Seguridad de Next.js y carreras en el panel (2026-10-24)

- Next.js 16.4.0 tenía 3 vulnerabilidades conocidas (2 críticas, 1 alta; afectan a 16.0.0–16.4.0, corregidas en 16.4.1). Se actualizó a 16.4.3 junto con `eslint-config-next`; `pnpm audit --prod` queda sin vulnerabilidades y el aviso que cortaba `next build` y `next dev` desapareció.
- La suite e2e completa encontró dos carreras reales en `/admin/preguntas`: una respuesta antigua del detalle (o de la lista) que llegaba tarde tapaba la más reciente (por ejemplo, «Aprobada» después de publicar, o la lista de «Todas» con el filtro «Borrador» marcado). Ahora solo se muestra la respuesta de la última petición, y los botones del detalle se deshabilitan mientras una acción está en curso.
- `student.spec.ts` buscaba la vista previa de la práctica en el mapa, que desde §X lleva a la ruta real; se actualizó.
- Playwright corre con 2 navegadores en paralelo: con uno por núcleo, todas las pruebas contra un solo servidor local superaban los 30 s por carga.

## AA. Cobro con Flow (2026-10-25)

- Pedido del usuario: cobrar con Webpay y dejarlo listo para cuando tenga las claves; luego precisó Flow, porque ofrece suscripciones.
- Webpay Plus solo hace pagos únicos y la suscripción con Webpay requiere Oneclick con cobros programados por la app; Flow, en cambio, cobra la suscripción por su cuenta. Se integró Flow como proveedor (`BILLING_PROVIDER=flow`), detrás de la misma interfaz que Mercado Pago, que sigue disponible por configuración.
- Flujo: `customer/create` → registro de tarjeta (`customer/register`) → al volver, si la tarjeta quedó registrada, `subscription/create` al plan con los días de prueba de la app. Acceso con suscripción activa o en prueba y sin cobros vencidos (`morose = 1` deja la suscripción `paused`). Cancelar es inmediato (pendiente 5). Sincronización al volver, con el aviso del plan (`/billing/webhooks/flow`, cuyo contenido no se usa como dato) y con una tarea diaria de Vercel Cron (`/billing/sync/run`).
- La página de suscripción nombra al proveedor configurado y solo pide el correo del pagador con Mercado Pago.
- Por validar en el sandbox (README, pendiente 6): `last4CardDigits` de `customer/get` tras registrar la tarjeta, que la prueba no cobra y el contenido del aviso. Los textos legales (términos y privacidad) aún nombran a Mercado Pago: hay que actualizarlos al activar Flow en producción.


## AB. Plan diario tipo Duolingo (2026-10-25)

- Pedido del usuario: tomar el plan de Duolingo y adaptarlo al examen de grado, simple, entretenido y valioso; luego precisó que fuera razonable y sin lo innecesario. La universidad no se elige: todas estudian lo mismo.
- Se implementó lo esencial (FR-035, AC-047): fecha del examen con cuenta regresiva, meta diaria (10, 20, 30 o calculada), repaso espaciado de errores (1, 3, 7 y 14 días) como primera tarea del día y preparación por cédula. Nueva tabla `study_profile`; endpoints `GET /study/today`, `PUT /study/profile` y `GET /practice/review`; la ruta agrega `total` y `mastered` por unidad. El repaso se deriva de `practice_attempt`: no guarda estado propio.
- Descartado por ahora, por no aportar lo suficiente frente a su complejidad: protector de racha, desafíos diarios, prueba para saltar unidades y ligas.
- La interrogación oral con IA sigue esperando la decisión de proveedores de IA (pendiente del README).
- `/temario` ya no pide revisar «el cedulario de tu universidad».
- Confirmado por el usuario (2026-10-25): las electivas también son las mismas para todos. No hay selección de electiva; la ruta muestra todas las materias publicadas.

## AC. Prueba gratis de 14 días y plan en Flow (2026-10-25)

- Decisión del usuario: la prueba gratis pasa de 7 a 14 días (`BILLING_TRIAL_DAYS=14`). La pone la app al crear cada suscripción; el plan de Flow no tiene días de prueba propios, para no sumarlos.
- Creado en la cuenta de producción de Flow el plan `APRUEBA-MENSUAL` ($9.990 CLP mensual, duración indefinida, 3 reintentos de cobro, URL de confirmación `/billing/webhooks/flow`). Falta cargar `FLOW_API_KEY`, `FLOW_SECRET_KEY` y `FLOW_PLAN_ID` en Render y activar `BILLING_PROVIDER=flow`.

## AD. Planes, precios y proveedores de IA (2026-10-25)

- El usuario delegó la decisión. Resultado en `docs/planes.md`: se lanza solo el plan Procurador ($7.000, lo que existe hoy) y Litigante ($9.990) y Toga ($14.990) se habilitan con la interrogación oral, con cupos mensuales de interrogaciones en lugar de la cuota única de 5 al día y 100 al mes.
- Proveedores: Claude Sonnet 5.5 para evaluar y OpenAI para transcripción y embeddings; sin voz sintetizada en el MVP. Umbral para lanzar: nota a 0,5 puntos o menos de la del abogado en el 80 % de 30 respuestas reales.
- Pendiente para aplicar el precio de lanzamiento: crear el plan `PROCURADOR-MENSUAL` en Flow y fijar `BILLING_MONTHLY_PRICE_CLP=7000` y `FLOW_PLAN_ID` en Render. Las especificaciones de cuotas y FR-029 se actualizan cuando se implementen los planes.
