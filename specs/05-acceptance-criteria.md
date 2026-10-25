# Criterios de aceptación

Los criterios siguientes son verificables y deben convertirse en pruebas automatizadas cuando sea posible.

## AC-001 — Autenticación y autorización
Las operaciones protegidas requieren una identidad autenticada y permisos válidos. Las comprobaciones se ejecutan en el backend.

## AC-002 — Navegación académica
El estudiante puede navegar jurisdicción, programa, materia y subtemas disponibles sin asumir una cantidad fija de subtemas por materia.

## AC-003 — Pregunta de alternativas
Al responder una pregunta aprobada, el estudiante recibe el resultado y la explicación correspondiente. La selección debe respetar el alcance de estudio elegido.

## AC-004 — Importación y revisión de contenido
El contenido generado o importado no puede publicarse ni usarse en sesiones ordinarias antes de la aprobación humana de la versión exacta.

## AC-005 — Inicio de simulación
Antes de iniciar, la configuración queda validada y congelada para la sesión, incluyendo el modo de retroalimentación, alcance y límites de tiempo.

## AC-006 — Tiempo total
Al agotarse el tiempo total, no se puede iniciar otra pregunta. La pregunta activa puede completarse dentro de su límite individual y de las extensiones válidas; luego la sesión se cierra.

## AC-007 — Respuesta oral
Una respuesta oral válida se transcribe y vincula al intento correcto. Los fallos de transcripción o proveedor no se presentan automáticamente como respuestas académicamente incorrectas.

## AC-008 — Evaluación asistida por IA
La evaluación utiliza una versión identificable de la pregunta, respuesta de referencia y rúbrica. La respuesta del estudiante se evalúa por su contenido jurídico y no solo por coincidencia literal.

## AC-009 — Historial
El estudiante puede consultar sus resultados e historial autorizado. El estudiante no puede modificar directamente puntuaciones.

## AC-010 — Seguridad y privacidad
No se conserva el audio original de manera persistente por defecto. El sistema conserva transcripciones y resultados conforme a una política de retención aprobada; los logs no deben incluir datos innecesarios. El audio temporal se elimina al terminar la transcripción (tope de 1 hora para restos) y transcripciones y resultados se eliminan a los 12 meses.

## AC-011 — Integridad de estados
Las transiciones de sesión se validan en el backend. Las solicitudes tardías o duplicadas no reabren sesiones ni crean respuestas o evaluaciones duplicadas.

## AC-012 — Publicación por versión
La aprobación corresponde a una versión exacta. Un cambio sustantivo requiere nueva versión y nueva revisión.

## AC-013 — Modo de retroalimentación
Si el estudiante selecciona `after_each_question`, se muestra retroalimentación al cerrar cada pregunta evaluada. Si selecciona `at_simulation_end`, no se muestran puntuaciones, correcciones ni explicaciones académicas antes del cierre. La configuración queda guardada en la sesión.

## AC-014 — Extensión de 60 segundos
Cuando expira el tiempo individual, la interfaz ofrece durante 15 segundos solicitar 60 segundos adicionales; ese lapso consume tiempo total y, si vence sin solicitud, la pregunta pasa a `timed_out`. Si el backend concede la extensión, el límite de la pregunta se actualiza exactamente según la regla y se registra un evento. Si la solicitud es inválida, duplicada o no autorizada, no debe ampliar el tiempo. Una segunda extensión en la misma pregunta se rechaza (máximo 1). La extensión puede solicitarse también cuando el tiempo total ya se agotó, mientras la pregunta esté activa.

## AC-015 — Pausa por desconexión
Cuando el backend reconoce una desconexión que activa la regla de pausa, el tiempo deja de consumirse. Al reanudar, se recupera el último estado persistido y el tiempo restante. La reconexión no duplica respuestas, evaluaciones ni extensiones. Sin latido durante 30 s (latido cada 10 s) se reconoce la desconexión y el reloj se pausa retroactivamente desde el último latido. La sesión se puede reanudar dentro de 30 minutos; después queda `expired`. Una grabación en curso se descarta y el estudiante vuelve a grabar con el tiempo restante de la pregunta.

## AC-016 — Reporte de pregunta o evaluación
El estudiante puede enviar un reporte desde una pregunta o evaluación. El reporte queda vinculado a la versión pertinente y puede ser revisado por un administrador autorizado.

## AC-017 — Corrección administrativa
Una corrección de resultado conserva el original, el resultado corregido, el motivo, el responsable, la fecha y el reporte asociado. El estudiante no puede efectuar esa corrección directamente.

## AC-018 — Selección específica de materia
El estudiante puede elegir una o más materias y subtemas. Todas las preguntas de la sesión deben pertenecer al alcance seleccionado y estar aprobadas.

## AC-019 — Plan original de estudio
Con fecha de examen, programa y disponibilidad, el sistema genera un plan con actividades fechadas, carga estimada y cobertura del programa. Los datos y supuestos relevantes deben ser visibles. El plan muestra tareas completadas, pendientes y atrasadas, y alertas de riesgo cuando la carga pendiente no parezca compatible con el tiempo restante. No promete aprobación.

## AC-020 — Actualización adaptativa del plan
Cuando cambian los resultados o el progreso, el sistema puede generar una revisión adaptativa. El plan original se mantiene visible y las modificaciones quedan identificadas con fecha y causa.

## AC-021 — RAG y trazabilidad de fuentes
Cuando una evaluación o explicación utiliza RAG, se conservan referencias a las fuentes o fragmentos recuperados. Si la evidencia es insuficiente, el sistema debe declarar la limitación y no inventar citas.

## AC-022 — Voz por turnos en el MVP
El estudiante puede completar el flujo de pregunta, respuesta hablada, transcripción y evaluación por turnos. La arquitectura no acopla la lógica de dominio a un proveedor de voz específico.

## AC-023 — Límites de costo
El sistema evita reprocesar documentos y evaluaciones sin necesidad, registra consumo medible cuando esté disponible y aplica límites configurados. No se permite que solicitudes duplicadas generen costos repetidos evitables.

## AC-024 — Responsive
Los flujos principales de estudio, voz, temporizadores, resultados, selección de materias, calendario y reportes son utilizables en móvil, tablet y escritorio.

## AC-025 — Revisión humana de contenido generado por IA
Una propuesta de pregunta, alternativa, respuesta de referencia o explicación generada por IA se registra como borrador, queda marcada como generada por IA y no se publica hasta que un administrador autorizado apruebe la versión exacta. Complementa AC-004 y AC-012.

## AC-026 — Errores y confianza
Los fallos técnicos, transcripciones insuficientes y evaluaciones con evidencia limitada se identifican como tales y no se convierten silenciosamente en un puntaje definitivo.

## AC-027 — Alternativa textual y accesibilidad
El estudiante puede completar el flujo de respuesta mediante texto, sin depender de voz ni de micrófono. Los flujos principales son operables con teclado y cumplen contraste suficiente.

## AC-028 — Pausa voluntaria
Solo se acepta entre preguntas, sin pregunta activa. Dura hasta 30 segundos y se permite una vez por simulación; una segunda solicitud se rechaza. Al vencer, el reloj se reanuda automáticamente y el evento queda registrado.

## AC-029 — Separación de autor y aprobador
El usuario que creó o modificó una versión no puede aprobarla ni publicarla. La operación se rechaza en el backend.

## AC-030 — Tipo único por simulación y corrección con reporte
Una simulación no admite mezclar tipos de pregunta. Una corrección de resultado sin reporte vinculado se rechaza.

## AC-031 — Tiempo de procesamiento
El reloj de la pregunta y el total se detienen cuando el backend recibe la respuesta, y el total se reanuda al terminar (o fallar) el procesamiento; la latencia de transcripción y evaluación no reduce el tiempo del estudiante.

## AC-032 — Cuentas y contraseñas
Se rechazan contraseñas de menos de 12 caracteres o comunes. Una cuenta no verificada no puede usar la aplicación. El enlace de recuperación es de un solo uso y caduca a los 30 minutos.

## AC-033 — Eliminación a solicitud
El estudiante puede solicitar la eliminación de sus transcripciones y resultados; se ejecuta en un máximo de 30 días y queda un registro de auditoría sin contenido.

## AC-034 — Conversión a escala 1 a 7
El puntaje ponderado de 0 a 100 se convierte linealmente a 1,0–7,0 con un decimal, de forma determinista y reproducible.

## AC-035 — Cuotas
Al alcanzar el 80 % de la cuota se muestra una alerta; al llegar al límite (5 por día o 100 por mes) se rechaza con un error claro.

## AC-036 — Sesión de usuario y registro
Un estudiante puede registrarse con correo y contraseña; la cuenta no puede usarse hasta verificar el correo con un enlace de un solo uso que caduca a las 24 horas. La sesión caduca tras 7 días sin actividad o 30 días desde el inicio, y cerrar sesión la revoca en el backend. Tras 10 intentos fallidos en 15 minutos, la cuenta rechaza nuevos intentos durante 15 minutos. Las respuestas de registro, inicio de sesión y recuperación no revelan si un correo está registrado, salvo el aviso de bloqueo temporal.

## AC-037 — Comentarios de usuarios
Con sesión iniciada, el usuario puede enviar un comentario con tipo y mensaje de 1 a 2.000 caracteres desde el panel, y recibe una confirmación. Sin sesión, la operación se rechaza. Solo un administrador puede listar los comentarios; un estudiante no puede leer los de nadie.

## AC-038 — Suscripción
Un estudiante sin suscripción puede iniciar una y es redirigido a Mercado Pago; la aplicación no recibe datos de tarjeta. Una solicitud repetida no crea suscripciones duplicadas. Solo una suscripción `authorized` da acceso al estudio; los administradores tienen acceso sin suscripción. Un estudiante sin acceso que inicia sesión es llevado a la suscripción y no ve el panel.

## AC-039 — Notificaciones de pago
Una notificación sin firma válida se rechaza y no cambia el estado. Una notificación válida no se usa como dato: el backend consulta el estado en Mercado Pago y lo registra. Las notificaciones repetidas no duplican cambios. El simulador de pagos no puede activarse en producción.

## AC-040 — Ingreso con Google
Un usuario puede ingresar con Google; si su correo verificado ya tiene cuenta, entra a esa misma cuenta, y si no, se crea una cuenta de estudiante. Se rechazan las respuestas con `state` o `nonce` que no coinciden, códigos inválidos y correos no verificados por Google. El registro con correo y contraseña sigue disponible.

## AC-041 — Acceso de cortesía
Una cuenta con acceso de cortesía vigente entra al panel y al estudio sin suscripción. Otorgarlo exige una cuenta existente, motivo y responsable; repetirlo no crea un segundo acceso. Al revocarlo la cuenta pierde el acceso y el registro se conserva con su fecha de revocación.

## AC-042 — Rachas
La primera visita del día suma un día a la racha y muestra una celebración una sola vez; volver el mismo día no suma ni repite la celebración. Un día sin entrar reinicia la racha actual y se conserva la mejor. Los días se cuentan en hora de Chile.

## AC-043 — Recordatorio por correo
Un estudiante con acceso que lleva 2 días sin entrar recibe un solo recordatorio; no recibe otro hasta volver a entrar y ausentarse de nuevo. Quien se da de baja no recibe más, y el enlace de baja sirve más de una vez. No reciben recordatorios quienes no tienen acceso. La tarea rechaza llamadas sin la clave correcta.

## AC-044 — Importación del banco de preguntas
Un administrador descarga la plantilla vacía o el banco actual (una fila por pregunta, con su id y estado), lo modifica y lo vuelve a subir. Si alguna fila es inválida, o trae un id que no existe, no se aplica ninguna y se informa cada fila con su error. Si todas son válidas: cada fila sin id crea una pregunta con su versión 1 en borrador; cada fila con id cuyo contenido cambió crea la versión siguiente en borrador, sin modificar ni despublicar las anteriores; cada fila marcada para retirar retira todas las versiones vigentes de esa pregunta, sin borrarlas; las filas sin cambios no hacen nada. Quitar una fila de la planilla no retira la pregunta. Una pregunta solo aparece en la práctica cuando otro administrador la aprueba y la publica, y la práctica no envía la respuesta correcta antes de que el estudiante responda.

## AC-045 — Ruta de estudio
El estudiante con acceso ve una unidad por materia con lecciones de al menos cinco preguntas publicadas (subtemas consecutivos), en el orden en que se cargaron al banco. Solo entran preguntas publicadas. Una lección queda completa al responder todas sus preguntas; sus estrellas son 3 si acertó todas en su último intento, 2 si acertó al menos el 80 % y 1 en otro caso, y cada respuesta correcta suma 10 XP. La lección siguiente de la unidad se desbloquea al completar la anterior. Al jugar una lección, la respuesta correcta llega del backend solo después de responder (como en AC-044).

## AC-046 — Administración de preguntas desde el panel
Un administrador crea una pregunta desde un formulario y queda como versión 1 en borrador. El formulario y la planilla aplican las mismas reglas de contenido. Editar cualquier versión crea la versión siguiente en borrador sin modificar las anteriores; si había una publicada, sigue en la práctica hasta que otro administrador publique la nueva. Descartar una versión (en cualquier estado) la deja retirada sin afectar a las demás; retirar la pregunta retira todas sus versiones vigentes. Nada se borra y cada versión muestra el historial de la pregunta. El panel permite buscar por enunciado o subtema, filtrar por materia y estado, y paginar; en celular el detalle se abre a pantalla completa sin desplazamiento horizontal.

