> **Cada hito debe terminar con un sistema funcional y con tests manuales claros.**

---

# Fase A - Desarrollo Local (Mac M1 Pro)

## Objetivo

Construir un sistema completamente funcional utilizando únicamente la webcam de la Mac para desarrollar toda la lógica de visión artificial antes de incorporar Frigate y la cámara Reolink.

---

# Hito A.0 - Inicialización del Proyecto

## Objetivo

Crear la estructura base del proyecto.

### Tecnologías

- Python 3.12+
- uv (gestor de paquetes recomendado)
- Git
- Ruff
- Pyright
- pytest

### Entregables

```
vision-engine/
│
├── app/
├── models/
├── services/
├── detectors/
├── events/
├── utils/
├── tests/
├── main.py
└── pyproject.toml
```

### Criterios de aceptación

- Proyecto ejecuta correctamente.
- Entorno virtual configurado.
- Linter funcionando.
- Tipado funcionando.

---

# Hito A.1 - Captura de Cámara

## Objetivo

Capturar video desde la webcam.

### Implementar

- Inicializar webcam.
- Mostrar imagen.
- Mostrar FPS.
- Salir correctamente.

### Librerías

- OpenCV

### Resultado esperado

Video en tiempo real.

---

# Hito A.2 - Pipeline de Frames

## Objetivo

Crear un pipeline desacoplado.

```
Webcam

↓

Frame Provider

↓

Frame Processor

↓

Renderer
```

### Implementar

Interfaces.

Separación de responsabilidades.

### Resultado esperado

Arquitectura preparada para reemplazar webcam por RTSP.

---

# Hito A.3 - Configuración Centralizada

Crear archivo de configuración.

Ejemplo:

```
config.py
```

Configurar:

- resolución
- FPS
- modelo YOLO
- cámara

---

# Hito A.4 - Integración YOLO

## Objetivo

Detectar personas.

### Implementar

Carga del modelo.

Inferencia.

Filtrar únicamente clase "person".

### Mostrar

Bounding Boxes.

Confidence.

FPS.

---

# Hito A.5 - Modelo de Detecciones

Crear entidades.

```
Detection

Person

BoundingBox
```

Separar dominio de YOLO.

Nunca depender directamente del formato de Ultralytics.

---

# Hito A.6 - Tracking

Asignar IDs.

Ejemplo:

```
Persona 1

Persona 2
```

Persistir ID entre frames.

---

# Hito A.7 - Historial Temporal

Guardar:

- timestamp
- posición
- velocidad
- duración visible

---

# Hito A.8 - Eventos

Crear sistema de eventos.

Ejemplos:

```
PersonDetected

PersonEntered

PersonExited

TrackingLost
```

No enviar nada todavía.

Solo emitir eventos internos.

---

# Hito A.9 - Logger

Registrar todos los eventos.

Formato JSON.

Guardar archivo local.

---

# Hito A.10 - Persistencia Local

Guardar eventos.

SQLite local.

Tablas:

- persons
- detections
- events

---

# Hito A.11 - YOLO Pose

Integrar modelo Pose.

Mostrar:

- cabeza
- hombros
- cadera
- rodillas
- tobillos

---

# Hito A.12 - Skeleton Renderer

Dibujar esqueleto.

Mostrar keypoints.

---

# Hito A.13 - Clasificación de Postura

Crear enum.

```
Standing

Sitting

Lying

Unknown
```

Clasificar postura.

---

# Hito A.14 - Máquina de Estados

Cada persona tiene un estado.

```
Standing

↓

Walking

↓

Sitting

↓

Lying
```

Persistir cambios.

---

# Hito A.15 - Detección de Cambios Bruscos

Detectar transición.

Ejemplo.

Standing

↓

Lying

en menos de X segundos.

---

# Hito A.16 - Inmovilidad

Calcular.

Tiempo sin movimiento.

---

# Hito A.17 - Posible Caída

Reglas.

Standing

↓

Lying

↓

Inmovilidad

↓

Emitir:

```
PossibleFallDetected
```

---

# Hito A.18 - Grabación Automática

Guardar:

15 segundos previos.

30 segundos posteriores.

Generar clip.

---

# Hito A.19 - Snapshot

Guardar imagen.

Asociar al evento.

---

# Hito A.20 - API Cliente

Crear cliente HTTP.

No hardcodear URLs.

Preparar:

```
POST /events
```

---

# Hito A.21 - Serialización

Transformar evento.

```
PossibleFallDetected
```

↓

JSON.

---

# Hito A.22 - Envío a Cloudflare

Enviar:

- detecciones
- eventos
- imágenes
- clips

---

# Hito A.23 - Dashboard Local

Mostrar.

FPS.

Personas detectadas.

Estado.

Tracking.

Eventos.

Última caída.

---

# Hito A.24 - Configuración Hot Reload

Modificar parámetros.

Sin reiniciar.

Ejemplo.

Tiempo de inmovilidad.

Confianza mínima.

FPS.

---

# Hito A.25 - Testing

Casos.

Persona camina.

Persona se sienta.

Persona se acuesta.

Persona desaparece.

Persona cae.

Verificar.

Todos los eventos emitidos correctamente.

---

# Resultado Final de la Fase A

La aplicación debe ser capaz de:

- Capturar video desde la webcam.
- Detectar personas.
- Asignar IDs persistentes.
- Estimar la postura corporal.
- Detectar cambios de postura.
- Detectar inmovilidad.
- Emitir un evento "PossibleFallDetected".
- Grabar un clip asociado.
- Guardar un snapshot.
- Persistir los eventos localmente.
- Enviar los eventos al backend de Cloudflare mediante HTTP.
- Ejecutarse en tiempo real en una MacBook Pro M1 Pro.

### Una mejora arquitectónica que agregaría

Conociendo tu forma de trabajar (Clean Architecture, DDD y Hexagonal), **no dejaría que YOLO "invada" el resto del sistema**.

Crearía una interfaz como esta:

```text
VisionProvider
    │
    ├── YoloVisionProvider
    ├── MockVisionProvider
    └── FrigateVisionProvider (futuro)
```

Y el resto de la aplicación consumiría únicamente objetos de dominio (`Person`, `Pose`, `Detection`, `PossibleFallEvent`, etc.), sin saber si la información proviene de YOLO, Frigate u otra tecnología.

Eso te permitiría, en el futuro, reemplazar YOLO por otro modelo o incluso consumir las detecciones que ya genera Frigate sin reescribir la lógica de negocio. Es una decisión de arquitectura que probablemente te ahorre mucho trabajo cuando pases de la webcam de la Mac a la Reolink y luego a una infraestructura con múltiples cámaras.
