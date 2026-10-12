# Voz, planificación, RAG y experiencia responsive

## Voz por turnos

El MVP usa voz por turnos: el sistema presenta una pregunta, el estudiante responde hablando, se transcribe la respuesta y se evalúa con una rúbrica y una respuesta de referencia versionadas. La retroalimentación se muestra según la configuración elegida antes de comenzar.

La arquitectura debe permitir añadir conversación en tiempo real en una fase futura, sin hacerla requisito del MVP. La interfaz debe informar sobre permisos de micrófono, grabación, envío, procesamiento y errores. Debe existir alternativa textual.

## Temporizadores y recuperación

- El límite total impide iniciar preguntas nuevas una vez agotado.
- La pregunta activa puede terminar dentro del límite individual vigente.
- Al expirar el límite individual, se puede solicitar una extensión de 60 segundos.
- El backend decide y registra las extensiones; el máximo es 1 por pregunta y la oferta dura 15 segundos.
- La pausa voluntaria solo se permite entre preguntas, hasta 30 segundos y una vez por simulación.
- Ante una desconexión reconocida, el tiempo se pausa y la sesión se reanuda desde el último estado persistido con el tiempo restante.
- Deben prevenirse respuestas duplicadas y solicitudes concurrentes que creen extensiones múltiples.
- La desconexión se detecta con latido cada 10 s y caída a los 30 s; la sesión se recupera dentro de 30 minutos. Una grabación en curso o sin transcribir se descarta y se vuelve a grabar.

## Planificación de estudio

La aplicación genera un plan original desde la fecha del examen, el programa, la disponibilidad y el progreso conocido. Los resultados posteriores permiten crear revisiones adaptativas, sin borrar el plan original. El estudiante debe poder comparar objetivo original y progreso real, consultar tareas vencidas y recibir alertas de riesgo de cobertura.

Las fechas, la carga de estudio y la cobertura se calculan mediante reglas deterministas. La prioridad de cada materia es su peso en el programa multiplicado por la brecha de desempeño reciente; la regla es visible para el estudiante. La IA puede ayudar a interpretar resultados y sugerir prioridades, pero no debe ser la única fuente de cálculo ni prometer aprobación.

## RAG para contenido jurídico

RAG recupera fragmentos pertinentes de una biblioteca aprobada. La recuperación debe respetar jurisdicción, materia, metadatos de vigencia y permisos. Las explicaciones y evaluaciones relevantes deben poder vincularse con las fuentes recuperadas. Si no existe evidencia suficiente, la IA debe indicar la limitación.

Los documentos deben revisarse en cuanto a procedencia, integridad y metadatos antes de utilizarse para crear contenido publicado. Las preguntas generadas por IA son borradores hasta su aprobación humana.

## Costo

- Reutilizar contenido aprobado en lugar de generar preguntas nuevas en cada sesión.
- Indexar documentos una vez y actualizar el índice solo ante cambios relevantes.
- Recuperar una cantidad limitada de fragmentos relevantes.
- Usar lógica determinista para permisos, tiempos, estados y cálculos de calendario.
- Registrar consumo por función y establecer cuotas antes de producción.
- Medir calidad, latencia y costo con un conjunto de preguntas reales antes de seleccionar proveedores.

## Responsive

El diseño adaptable es parte del MVP. Deben probarse en móvil la lectura de preguntas, selección de alternativas, captura de voz, visualización de tiempo, reconexión, calendario y revisión de resultados. La experiencia no debe depender exclusivamente de voz.
