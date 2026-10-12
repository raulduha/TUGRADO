# Arquitectura propuesta

## 1. Componentes principales

- **Frontend**: Next.js + TypeScript. Aplicación responsive para escritorio, tablet y móvil.
- **Backend API**: FastAPI + Python. Fuente de verdad para identidad autorizada, reglas de negocio, estados, temporizadores, resultados y publicación.
- **Base de datos relacional**: PostgreSQL para usuarios, programas, preguntas, versiones, sesiones, reportes, planes y auditoría. Acceso mediante SQLAlchemy y migraciones con Alembic.
- **Almacenamiento temporal de importaciones**: para documentos que se procesan; PDF, DOCX y TXT de hasta 25 MB, en Vercel Blob detrás de una interfaz, con acceso restringido y eliminación tras el procesamiento.
- **Servicio de transcripción**: detrás de una interfaz independiente del proveedor.
- **Servicio de evaluación/generación**: proveedor de modelo de lenguaje intercambiable.
- **Servicio de síntesis de voz**: opcional en el MVP; detrás de una interfaz para habilitar respuestas habladas.
- **Capa RAG**: ingesta, extracción, fragmentación, embeddings, recuperación, filtros por metadatos y referencias a fuentes. Índice vectorial: pgvector sobre PostgreSQL, a validar con una prueba de concepto.
- **Tareas asíncronas**: procesamiento de importaciones, indexación, transcripción y evaluación cuando corresponda. Cola implementada como tabla en PostgreSQL (Neon) detrás de una interfaz.

## 2. Contratos y límites

El frontend consume la API documentada por FastAPI. Se recomienda generar contratos TypeScript desde OpenAPI para reducir divergencias. La lógica de negocio no debe depender de componentes de interfaz.

Los proveedores de modelos, transcripción, embeddings y síntesis deben implementarse detrás de interfaces internas. La lógica de dominio no debe depender de un SDK específico.

## 3. Sesiones y temporizadores

El backend mantiene la hora de inicio, límite total, límite individual, tiempo restante y eventos de pausa/reanudación. El frontend presenta los temporizadores, pero no determina por sí solo si una respuesta llegó a tiempo.

### Expiración total
1. El backend marca la sesión como no habilitada para iniciar nuevas preguntas.
2. Si existe una pregunta activa, permite terminarla según su límite individual y las extensiones autorizadas.
3. Al terminar o expirar la pregunta activa, cierra la sesión.
4. Rechaza solicitudes tardías, duplicadas o que intenten abrir una pregunta nueva.

### Extensión individual
Al expirar el límite individual, el frontend ofrece durante 15 segundos solicitar 60 segundos adicionales. El backend verifica estado, identidad, política de extensiones y concurrencia, registra el evento y devuelve el nuevo límite autorizado: hora de concesión + 60 s. El máximo es 1 extensión por pregunta.

### Pausa voluntaria
Solo se permite sin pregunta activa, hasta 30 segundos y una vez por simulación. Al vencer, el backend reanuda el reloj.

### Desconexión y recuperación
La sesión guarda checkpoints en eventos relevantes: presentación de pregunta, respuesta enviada, transcripción lista, evaluación completada, extensión concedida y pausa/reanudación. Al detectarse una desconexión aplicable, el backend pausa el reloj; al reconectar, restaura el estado y tiempo restante guardados. Detección: latido del cliente cada 10 s; sin latido durante 30 s se reconoce la desconexión y el reloj se pausa retroactivamente desde el último latido. Ventana máxima de recuperación: 30 minutos, contados desde el último latido. Una solicitud duplicada debe ser idempotente.

El checkpoint de pausa guarda el estado previo para poder volver a él, incluido `awaiting_current_question_completion`. El audio temporal no se persiste, por lo que una grabación en curso o sin transcribir al desconectarse no se restaura. El estudiante vuelve a grabar con el tiempo restante de la pregunta. El tiempo de transcripción y evaluación no se imputa al estudiante: el backend registra la hora de recepción de cada respuesta; en ese momento se detienen el reloj de la pregunta y el total, y el total se reanuda al terminar (o fallar) la transcripción y evaluación.

## 4. Voz

### MVP: por turnos
`pregunta -> captura de audio temporal -> transcripción -> validación de transcripción -> recuperación de fuentes/criterios -> evaluación -> feedback según configuración`.

El audio se procesa temporalmente y no se guarda en el historial persistente. La transcripción, evaluación, versiones de pregunta/rúbrica y fuentes utilizadas pueden conservarse durante 12 meses.

El sistema debe manejar errores de micrófono, permisos denegados, silencio, transcripción insuficiente, proveedor no disponible y evaluación fallida. Los fallos técnicos no deben convertirse automáticamente en una evaluación académica negativa.

### Evolución a tiempo real
La arquitectura debe separar la interfaz de voz y el proveedor para permitir más adelante conversación continua, interrupciones y repreguntas. Esta capacidad no forma parte del MVP.

## 5. RAG jurídico

1. Ingerir documentos aprobados.
2. Extraer texto y metadatos, conservar vínculo con el documento original.
3. Dividir contenido en fragmentos con identificadores estables y referencias de origen.
4. Generar embeddings e indexar los fragmentos.
5. Recuperar fragmentos relevantes según pregunta, jurisdicción, materia, fecha/validez y filtros de acceso.
6. Pasar al modelo solo los fragmentos pertinentes, instrucciones de evaluación y rúbrica versionada.
7. Guardar trazabilidad de las fuentes utilizadas cuando se emite una explicación o evaluación relevante.
8. Si no hay evidencia suficiente, el sistema debe declarar la limitación y evitar inventar una cita.

El contenido recuperado se considera material de referencia, no instrucciones para cambiar las reglas de la aplicación. La generación automática de contenido no publica preguntas sin revisión humana.

## 6. Plan de estudio

La planificación de fechas, carga semanal, cobertura y tareas debe usar lógica determinista y validable. La IA puede ayudar a resumir brechas o sugerir prioridades, pero no debe ser la única responsable de calcular fechas ni de garantizar cobertura.

Se conserva un plan original como línea base. Los cambios posteriores crean una revisión adaptativa con fecha, causas y actividades modificadas. Los resultados de estudio alimentan las recomendaciones futuras.

## 7. Control de costos

- No generar una pregunta nueva con IA cada vez que el estudiante practica si existe una pregunta aprobada adecuada.
- Indexar y calcular embeddings al ingresar o modificar documentos, no en cada pregunta.
- Limitar el número y tamaño de fragmentos recuperados.
- Evitar repetir transcripciones o evaluaciones por solicitudes duplicadas.
- Registrar consumo por función/proveedor/modelo cuando el proveedor permita medirlo.
- Establecer límites de uso, alertas y manejo de cuotas antes de producción.
- Evaluar calidad y costo con un conjunto representativo de respuestas jurídicas antes de seleccionar proveedores.

## 8. Seguridad y privacidad

- Autorización en backend para todas las operaciones protegidas.
- Acceso restringido a documentos, transcripciones y resultados.
- Audio temporal no persistente por defecto; eliminación definida y verificable.
- Revisar condiciones de retención de proveedores externos.
- Minimizar datos sensibles en logs.
- Auditar publicación de contenidos, correcciones administrativas, extensiones y cambios de estado.
- Retención de transcripciones, resultados e historial: 12 meses; falta definir el procedimiento de eliminación a solicitud del estudiante.

## 9. Responsive y accesibilidad

La interfaz debe adaptarse desde la primera versión. Los flujos de grabación, lectura de pregunta, temporizador, envío de respuesta, recuperación tras desconexión y revisión de resultados deben probarse en tamaños móviles y navegadores soportados. Debe existir una alternativa textual al uso de voz.

## 10. Decisiones técnicas

### Resueltas
- Base de datos: PostgreSQL en Neon, con SQLAlchemy y Alembic. Índice RAG: pgvector.
- Hosting del frontend: Vercel. Almacenamiento temporal: Vercel Blob. Cola: tabla en PostgreSQL detrás de una interfaz.
- Autenticación propia con correo y contraseña: Argon2id, mínimo 12 caracteres, correo verificado, recuperación con enlace de un solo uso de 30 minutos. Sesión en cookie HttpOnly/Secure/SameSite=Lax con token opaco; la sesión se guarda en PostgreSQL (hash del token) y es revocable. El frontend reenvía `/api` al backend para operar en el mismo origen, y el backend valida el encabezado `Origin` en las operaciones que modifican datos.
- Observabilidad: OpenTelemetry, sin datos personales ni audio en logs.
- Entorno local: Docker para PostgreSQL y backend. Correo en desarrollo: salida por consola.
- Retención: 12 meses; eliminación a solicitud en un máximo de 30 días; audio temporal eliminado al terminar la transcripción.
- Documentos: PDF, DOCX y TXT de hasta 25 MB. Escala 1 a 7 con conversión lineal ponderada y un decimal.
- Cuotas iniciales: 5 simulaciones orales por día y 100 por mes por usuario, alerta al 80 %.

### Pendientes
Ver `README.md` ("Pendientes explícitos"): hosting de producción del backend, proveedor de correo de producción y proveedores de IA tras la prueba de concepto.
