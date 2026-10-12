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
El reloj de la pregunta se detiene cuando el backend recibe la respuesta; la latencia de transcripción y evaluación no reduce el tiempo del estudiante.

## AC-032 — Cuentas y contraseñas
Se rechazan contraseñas de menos de 12 caracteres o comunes. Una cuenta no verificada no puede usar la aplicación. El enlace de recuperación es de un solo uso y caduca a los 30 minutos.

## AC-033 — Eliminación a solicitud
El estudiante puede solicitar la eliminación de sus transcripciones y resultados; se ejecuta en un máximo de 30 días y queda un registro de auditoría sin contenido.

## AC-034 — Conversión a escala 1 a 7
El puntaje ponderado de 0 a 100 se convierte linealmente a 1,0–7,0 con un decimal, de forma determinista y reproducible.

## AC-035 — Cuotas
Al alcanzar el 80 % de la cuota se muestra una alerta; al llegar al límite (5 por día o 100 por mes) se rechaza con un error claro.
