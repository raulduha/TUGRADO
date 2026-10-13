# Requisitos funcionales y reglas de negocio

## 1. Usuarios y permisos

### FR-001 — Autenticación y perfil
Cada usuario debe acceder mediante una cuenta autenticada. El backend valida la identidad y autorización para toda operación protegida. Las cuentas usan correo y contraseña de mínimo 12 caracteres (Argon2id, sin reglas de composición, con bloqueo de contraseñas comunes), correo verificado antes del primer uso y recuperación mediante enlace de un solo uso que caduca a los 30 minutos. La sesión se mantiene con una cookie HttpOnly, Secure y SameSite=Lax que contiene un token opaco; el backend guarda la sesión (solo el hash del token) y puede revocarla. Caduca tras 7 días sin actividad o 30 días desde el inicio. Los estudiantes se registran solos; los administradores se crean con un comando de consola. El enlace de verificación de correo es de un solo uso y caduca a las 24 horas. Tras 10 intentos fallidos de inicio de sesión en 15 minutos, la cuenta se bloquea temporalmente 15 minutos. Todos estos valores son configuración.

### FR-001b — Ingreso con Google
Además del correo y contraseña, el usuario puede ingresar con su cuenta de Google (OpenID Connect, flujo de código de autorización con PKCE, `state` y `nonce`). Solo se aceptan correos que Google declara verificados. Si el correo ya tiene una cuenta, se vincula automáticamente; si no, se crea una cuenta de estudiante con el correo verificado y sin contraseña (puede definir una con la recuperación de contraseña). La sesión resultante es la misma que con correo y contraseña.

### FR-002 — Roles
El sistema debe incluir, como mínimo, los roles `student` y `administrator`.

- `student`: puede estudiar contenido aprobado, configurar sesiones, responder preguntas, revisar sus resultados, gestionar su plan de estudio y reportar contenido o evaluaciones.
- `administrator`: puede gestionar usuarios, estructura académica, fuentes, preguntas, versiones, revisiones, publicación y reportes de estudiantes; puede corregir resultados únicamente mediante un flujo auditado.

No existe un rol `editor` en el MVP. Dentro de `administrator` rige la separación entre autor y aprobador (ver FR-014).

El backend debe verificar permisos. Ocultar controles en el frontend no constituye autorización suficiente.

## 2. Estructura académica y selección

### FR-003 — Jurisdicción y programa
La jurisdicción debe ser configurable. El contenido y la estructura académica deben estar asociados a una jurisdicción y, cuando corresponda, a un programa o versión de programa.

### FR-004 — Materias y subtemas
Cada materia puede tener su propia cantidad y estructura de subtemas. No se debe codificar una cantidad fija de materias o subtemas.

### FR-005 — Selección de alcance
Antes de una sesión, el estudiante puede elegir una materia, uno o más subtemas, varias materias o el programa completo. La selección debe limitar las preguntas a contenido aprobado y perteneciente al alcance elegido.

## 3. Práctica

### FR-006 — Preguntas de alternativas
El estudiante puede responder preguntas de alternativas y recibir retroalimentación inmediata en este modo. Si la respuesta es incorrecta, el sistema muestra la alternativa correcta y una explicación aprobada.

### FR-007 — Simulación oral
El estudiante responde oralmente a preguntas, recibe transcripción y evaluación asistida por IA según una respuesta de referencia y una rúbrica versionadas. Cada versión de pregunta oral referencia la versión de rúbrica con la que se evalúa. La evaluación usa una escala de 1 a 7 (cada criterio de 0 a 100, ponderado según la rúbrica y convertido linealmente a 1,0–7,0 con un decimal) y no es una calificación académica oficial. Una simulación contiene un solo tipo de pregunta.

### FR-008 — Modo de retroalimentación
Antes de comenzar una simulación oral, el estudiante elige una opción:

- `after_each_question`: mostrar retroalimentación después de cada pregunta.
- `at_simulation_end`: mostrar la retroalimentación académica al finalizar la simulación.

La selección se guarda en la configuración de esa sesión y no se modifica retroactivamente. En el modo final, no se deben revelar puntajes, correcciones ni explicaciones académicas antes del cierre. Los mensajes técnicos necesarios para completar la sesión sí pueden mostrarse.

## 4. Tiempo, expiración y recuperación

### FR-009 — Límites de tiempo
La simulación admite un límite total y un límite individual por pregunta. El backend es la fuente de verdad del tiempo y del estado de la sesión.

### FR-010 — Expiración del tiempo total
Al agotarse el tiempo total, el sistema bloquea el inicio de nuevas preguntas. Si existe una pregunta activa, el estudiante puede terminarla dentro del límite individual vigente, incluidas las extensiones autorizadas. Al finalizar o expirar esa pregunta, la sesión se cierra y no puede reabrirse mediante solicitudes tardías o duplicadas.

Al terminar normalmente la pregunta activa, la sesión queda `completed`. Una pregunta termina cuando se completa la evaluación de su respuesta (o vence); la sesión pasa a `completed` en ese momento. No se puede iniciar otra pregunta mientras la anterior se procesa. Durante la pregunta activa pueden solicitarse extensiones válidas aunque el tiempo total ya se haya agotado, dentro del máximo configurado. El tiempo de transcripción y evaluación no se descuenta al estudiante: el reloj de la pregunta y el reloj total se detienen cuando el backend recibe la respuesta; el total se reanuda cuando termina (o falla) la transcripción y evaluación. Fuera de ese procesamiento, el reloj total corre también entre preguntas.

### FR-011 — Extensión individual
Cuando se agota el tiempo individual de una pregunta, la interfaz ofrece solicitar una extensión de **60 segundos** durante una ventana de **15 segundos**. Ese lapso consume tiempo total. Si no se solicita dentro de la ventana, la pregunta pasa a `timed_out`. El nuevo límite de la pregunta es la hora de concesión + 60 s, de modo que el estudiante dispone siempre de 60 s completos. La extensión solo se concede mediante una decisión validada por el backend. Debe registrarse el evento. El máximo es **1 extensión por pregunta**, configurado como parámetro (`max_extensions_per_question = 1`), no como constante en el código.

### FR-012 — Desconexión y recuperación
Si la conexión se pierde o la sesión se interrumpe, el tiempo debe pausarse según el estado de desconexión reconocido por el backend. El estudiante puede reanudar desde el último estado persistido, conservando el tiempo restante, la pregunta activa y las respuestas ya guardadas.

El sistema debe evitar duplicar respuestas, evaluaciones o extensiones. La pausa por desconexión no debe convertirse en un mecanismo de pausa voluntaria ilimitada. Detección: el cliente envía un latido cada 10 segundos. Si el backend no recibe latido durante 30 segundos, reconoce la desconexión y pausa el reloj de forma retroactiva desde el último latido recibido. Ventana de recuperación: 30 minutos (`recovery_window = 30 min`, configurable). Si la sesión no se reanuda en ese plazo, queda `expired`. La ventana de 30 minutos se cuenta desde el último latido recibido.

Las únicas respuestas que se restauran son las ya persistidas. Si había una grabación en curso o sin transcribir, se descarta el audio temporal y el estudiante vuelve a grabar con el tiempo restante de la pregunta.

### FR-012b — Pausa voluntaria
El estudiante puede pausar una simulación solo entre preguntas, es decir, sin pregunta activa. La pausa dura hasta 30 segundos y se permite una vez por simulación. Al vencer, el reloj se reanuda automáticamente. El backend valida y registra la pausa y su reanudación.

## 5. Contenidos y revisión

### FR-013 — Creación e importación
El administrador autorizado puede crear contenido manualmente e importar documentos para extracción asistida por IA. La IA puede proponer preguntas, alternativas, respuestas de referencia, explicaciones y metadatos.

### FR-014 — Revisión y publicación
Todo contenido generado o importado debe pasar por revisión humana antes de publicarse. La aprobación corresponde a una versión exacta. Cualquier cambio sustantivo crea una nueva versión que requiere revisión antes de publicarse.

Quien crea o modifica una versión no puede aprobarla ni publicarla: debe hacerlo otro administrador. Aprobación y publicación son actos distintos: una versión aprobada puede publicarse (quedar disponible para sesiones ordinarias) mediante una acción auditada de un administrador. La revisión aplica a versiones de preguntas, alternativas, respuestas de referencia, explicaciones, rúbricas, fuentes y documentos que alimentan RAG.

### FR-015 — Fuentes jurídicas
El contenido debe mantener trazabilidad hacia sus fuentes. Cuando sea aplicable, se deben registrar jurisdicción, tipo de fuente, identificador/cita, fecha de publicación, vigencia o periodo de validez y versión. No se debe presentar una fuente como vigente sin antecedentes suficientes.

## 6. Reportes y correcciones

### FR-016 — Reportar pregunta o evaluación
Desde una pregunta, explicación o evaluación, el estudiante puede enviar un reporte con el motivo por el que considera que existe un error. El reporte conserva la versión de pregunta, el intento/sesión y la evaluación relacionados cuando correspondan, fecha, descripción y estado de revisión.

### FR-017 — Resolución administrativa
El administrador puede revisar el reporte, registrar comentarios y resolverlo como `resolved` o `rejected`, manteniendo historial. Si se modifica contenido publicado, debe crearse una nueva versión y seguirse el flujo de revisión y publicación.

### FR-018 — Corrección de resultados
Si se autoriza corregir una evaluación individual, el sistema conserva el resultado original y registra el resultado corregido, motivo, administrador responsable, fecha y vínculo al reporte de origen. El estudiante no puede modificar directamente su puntuación.

Los puntajes agregados de una sesión se derivan del resultado vigente de cada evaluación, y el original sigue consultable por los administradores. Toda corrección requiere un reporte vinculado; no hay correcciones de oficio.

## 7. Plan de estudio

### FR-019 — Plan original
El estudiante puede generar un plan hasta la fecha de su examen, considerando programa exigido, disponibilidad semanal, tiempo restante, progreso conocido y áreas que debe reforzar. El plan original debe quedar guardado como línea base.

### FR-020 — Plan adaptativo
Los resultados de preguntas y simulaciones pueden actualizar las recomendaciones y la distribución futura de actividades. El sistema conserva el plan original y muestra las modificaciones adaptativas, su fecha y una explicación breve de los factores que las motivaron.

El plan debe mostrar tareas completadas, pendientes y atrasadas, cobertura estimada del programa y alertas de riesgo cuando la carga pendiente no parezca compatible con el tiempo restante. No debe garantizar aprobación.

## 8. Voz, RAG y costos

### FR-021 — Voz por turnos en el MVP
El MVP admite la secuencia pregunta oral → respuesta hablada → transcripción → evaluación → retroalimentación según configuración. La arquitectura debe aislar los proveedores de transcripción, modelos de lenguaje y síntesis de voz para permitir una futura experiencia de voz en tiempo real.

### FR-022 — Persistencia de audio
Se conservan la transcripción, el resultado de evaluación y los metadatos necesarios. El audio original no se conserva de forma persistente por defecto. El audio temporal se elimina al terminar la transcripción (con un tope de seguridad de 1 hora para restos) y deben revisarse las condiciones de retención de los proveedores externos. Transcripciones, resultados e historial se conservan 12 meses.

### FR-023 — RAG
El sistema puede recuperar fragmentos de documentos jurídicos y académicos aprobados para fundamentar explicaciones, evaluación oral y asistencia de estudio. Debe conservarse la trazabilidad de los fragmentos utilizados. La falta de evidencia suficiente debe representarse explícitamente. RAG no sustituye la revisión humana del contenido publicado.

### FR-024 — Control de costos
Se deben reutilizar preguntas y respuestas aprobadas, indexar documentos cuando se incorporen o cambien, evitar evaluaciones duplicadas, limitar el contexto recuperado y medir consumo por función y usuario. Los límites iniciales son 5 simulaciones orales por día y 100 por mes por usuario, con alerta al 80 % y error claro al alcanzarlos; son configurables y se reajustan con datos reales de costo.

## 9. Experiencia responsive

### FR-025 — Diseño adaptable
La experiencia de estudiante y administración debe funcionar en móvil, tablet y escritorio desde la primera versión. Deben ser utilizables la lectura de preguntas, grabación de voz, temporizadores, resultados, selección de materias, calendario, progreso y reportes. Deben contemplarse permisos de micrófono, errores de red y reconexión. Debe existir una alternativa textual al uso de voz, y los flujos deben ser accesibles (teclado, lectores de pantalla y contraste suficiente).

## 10. Seguridad, historial y trazabilidad

### FR-026 — Historial de sesión
El sistema conserva configuración, estado, intentos, tiempos, transcripciones y evaluaciones durante 12 meses. El estudiante puede solicitar la eliminación de sus transcripciones y resultados desde su perfil; se ejecuta en un máximo de 30 días y deja un registro de auditoría sin contenido. Las transiciones relevantes deben quedar auditadas.

### FR-027 — Integridad
Las decisiones sobre autorización, temporizadores, publicación, estado de sesión y resultados se validan en el backend. Las solicitudes tardías, duplicadas o concurrentes no deben producir estados incompatibles.

## 11. Comentarios de usuarios

### FR-028 — Casilla de comentarios
Un usuario con sesión iniciada puede enviar comentarios sobre la aplicación desde un botón visible en el panel: tipo (`suggestion`, `problem` u `other`) y un mensaje de hasta 2.000 caracteres. Se guardan con el usuario, la página desde la que se envió y la fecha. Solo un administrador puede consultarlos. Los comentarios no sustituyen el reporte de preguntas o evaluaciones (FR-016), que conserva la versión de contenido y el intento asociado. Se conservan conforme a la política general de retención (12 meses).

## 12. Suscripción y pagos

### FR-029 — Suscripción mensual
El estudiante puede suscribirse desde la aplicación a un plan mensual de $9.990 CLP con 7 días de prueba gratis (valores configurables). El backend crea la suscripción en Mercado Pago y redirige al estudiante a la página de pago de Mercado Pago. La aplicación nunca recibe, procesa ni guarda datos de tarjeta.

### FR-030 — Estado y acceso
El backend es la fuente de verdad del acceso. El estado local de la suscripción se actualiza solo consultando la API de Mercado Pago: tras una notificación webhook con firma válida o cuando el estudiante vuelve de la página de pago. Nunca se confía en el contenido de una notificación ni en parámetros de la URL de retorno. El estudiante tiene acceso al estudio mientras la suscripción está `authorized` (incluida la prueba gratis). Los administradores no requieren suscripción. Cada cambio de estado queda registrado.

### FR-031 — Cancelación
El estudiante puede cancelar su suscripción desde la aplicación; el backend la cancela en Mercado Pago. El acceso tras la cancelación queda pendiente de decisión (README, punto 5).
