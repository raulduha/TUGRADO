# Quality Gates — Agent Harness

Una tarea no se considera terminada solo porque el código compila. Debe superar los controles aplicables a su alcance.

## Gate 1 — Consistencia de especificaciones

- La tarea corresponde a requisitos y criterios de aceptación existentes.
- No introduce contradicciones entre requisitos, modelo de dominio y arquitectura.
- Las decisiones pendientes están identificadas y no se resuelven mediante supuestos silenciosos.

## Gate 2 — Autorización y publicación

- Las operaciones protegidas se autorizan en backend.
- Solo administradores autorizados pueden publicar contenido o resolver reportes.
- Quien crea o modifica una versión no puede aprobarla ni publicarla.
- La aprobación corresponde a una versión exacta.
- Se prueba que contenido no aprobado no se utiliza en sesiones ordinarias.

## Gate 3 — Integridad de sesión y temporizadores

- Se prueban el límite total y el individual.
- Al agotarse el límite total, se bloquea el inicio de nuevas preguntas.
- La pregunta activa puede terminar dentro del límite individual y de extensiones válidas.
- Una extensión aprobada fija el límite en exactamente la hora de concesión + 60 segundos.
- Se prueban solicitudes tardías, duplicadas y concurrentes.
- La desconexión reconocida pausa el tiempo; la reconexión restaura estado y tiempo restante.
- Las solicitudes duplicadas no crean extensiones, respuestas o evaluaciones duplicadas.
- La ventana de recuperación (30 min), el máximo de extensiones (1), la ventana de oferta (15 s), el latido (10 s / 30 s) y la pausa voluntaria (30 s, una vez) son configuración, no constantes. Las pruebas cubren los valores límite de cada uno.
- Se prueba que la pausa voluntaria se rechaza con pregunta activa y que una segunda pausa se rechaza.
- Se prueba que el reloj de la pregunta y el total se detienen en la hora de recepción de la respuesta, y que el total se reanuda al terminar el procesamiento.
- Se prueba que la ventana de recuperación se cuenta desde el último latido.

## Gate 4 — Retroalimentación

- Se prueban ambos modos: después de cada pregunta y al final.
- En el modo final no se muestran puntajes, explicaciones ni correcciones académicas antes del cierre.
- La configuración queda congelada en la sesión.

## Gate 5 — Voz y privacidad

- Se prueba el flujo por turnos de pregunta, audio temporal, transcripción y evaluación.
- Se manejan permisos denegados, silencio, transcripción insuficiente, fallos de red y proveedor no disponible.
- Una falla técnica no se transforma automáticamente en una evaluación negativa.
- El audio original no se persiste por defecto.
- Se comprueba la política de contraseñas, la verificación de correo y la caducidad del enlace de recuperación (AC-032).
- Se comprueban la caducidad y revocación de la sesión, el bloqueo temporal por intentos fallidos y que las respuestas no revelen si un correo está registrado (AC-036).
- Se comprueba que el audio temporal se elimina al terminar la transcripción (tope de 1 hora para restos) y que transcripciones y resultados se eliminan a los 12 meses.
- Se revisa la retención de proveedores externos antes de producción.

## Gate 6 — RAG y calidad jurídica

- Se verifica la trazabilidad de fuentes y fragmentos.
- Se aplican filtros por jurisdicción, materia y metadatos de vigencia cuando estén disponibles.
- Se prueba el caso sin fuentes suficientes.
- No se inventan citas ni se presenta contenido generado como aprobado.
- Los cambios de documentos actualizan la indexación correspondiente sin reindexar innecesariamente todo el corpus.

## Gate 7 — Evaluación asistida por IA

- La evaluación identifica las versiones de pregunta, respuesta de referencia y rúbrica.
- Se prueban respuestas correctas expresadas de forma distinta, respuestas parciales, incorrectas y ambiguas.
- Se distingue la incertidumbre y los errores técnicos de una evaluación académica.
- Se conserva el resultado y la justificación de forma trazable.
- El estudiante no puede modificar la puntuación.

## Gate 8 — Reportes y correcciones

- El reporte conserva la versión de contenido y el intento asociado.
- Solo un administrador autorizado puede resolverlo.
- Una corrección mantiene el resultado original y registra motivo, actor y fecha.
- Los cambios de contenido siguen versionado y revisión.

## Gate 9 — Plan de estudio

- Se valida el plan original contra fecha de examen, programa y disponibilidad.
- Los cálculos de fechas y cargas usan reglas deterministas.
- Una actualización adaptativa no sobrescribe el plan original.
- Se muestran tareas completadas, pendientes y atrasadas, cobertura y alertas de riesgo.
- No se afirma ni garantiza aprobación.

## Gate 10 — Responsive y accesibilidad

- Se prueban flujos críticos en viewport móvil, tablet y escritorio.
- Grabación, temporizador, respuesta, reconexión, calendario y revisión de resultados son utilizables en móvil.
- Existe una alternativa textual al flujo de voz.

## Gate 11 — Costo y rendimiento

- No se repiten llamadas costosas ante solicitudes duplicadas cuando pueden evitarse.
- Los documentos no se vuelven a indexar sin un cambio relevante.
- Se aplican límites configurados de consumo y errores claros al alcanzar cuotas.
- Se registran métricas de uso disponibles sin guardar datos personales innecesarios.

## Gate 11b — Pagos

- Se verifica la firma de las notificaciones (HMAC del encabezado `x-signature`) y se rechazan las inválidas.
- El estado se obtiene de la API del proveedor, no del contenido de la notificación ni de la URL de retorno.
- No se reciben, registran ni guardan datos de tarjeta; las credenciales no aparecen en logs.
- Las solicitudes y notificaciones duplicadas son idempotentes.
- El acceso al estudio se autoriza en backend según el estado de la suscripción.

## Gate 12 — Verificación final

- Ejecuta las pruebas relacionadas y registra los resultados reales.
- No afirmes que una prueba pasó si no se ejecutó.
- Documenta cambios, riesgos, decisiones pendientes y pasos manuales restantes.
