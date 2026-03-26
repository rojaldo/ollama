---
theme: seriph
background: https://images.unsplash.com/photo-1518433278981-bd302da5ad0d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  ## Curso Avanzado de Ollama con Python
  Guía completa de implementación y dominio de LLMs locales.
drawings:
  persist: false
transition: slide-left
title: Ollama con Python - Curso Avanzado
---

# Ollama con Python
## Curso Avanzado de Implementación

Despliegue local, Inferencia Profunda, Tools, Visión y RAG.

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Comenzar curso <carbon:arrow-right class="inline"/>
  </span>
</div>

---

# 1. El Ecosistema Ollama

Dominando los LLMs en infraestructura local.

### 1.1 ¿Por qué Ollama local?
- **Privacidad Total**: Los datos nunca salen de tu máquina.
- **Coste Cero por Token**: Solo pagas hardware y electricidad.
- **Latencia Mínima**: Sin dependencia de red externa ni colas de API.
- **Soberanía de Datos**: Control absoluto sobre modelos y versiones.

### 1.2 Arquitectura del Sistema
1. **Ollama Serve**: El *daemon* que gestiona la GPU/RAM y expone la API REST (Puerto 11434).
2. **Wrapper Python**: Cliente ligero que abstrae las llamadas HTTP a objetos nativos.

---

# 1.3 Instalación y Configuración

Entornos de despliegue y variables críticas.

- **Nativo**: Máximo rendimiento (CUDA en Linux/Win, Metal en Mac).
- **Docker**: Aislamiento y despliegue rápido con *Open WebUI*.

### Variables de Entorno Clave
| Variable | Propósito |
| --- | --- |
| `OLLAMA_HOST` | Dirección del servidor (ej. `0.0.0.0:11434`). |
| `OLLAMA_MODELS` | Ruta personalizada para el almacenamiento. |
| `OLLAMA_KEEP_ALIVE` | Tiempo de persistencia en VRAM (def. 5m). |

---

# 2. La Librería `ollama-python`

Niveles de abstracción y gestión de conexión.

### Instalación
```bash
python -m venv venv && source venv/bin/activate
pip install ollama
```

### 2.2 Tres Modos de Operación
1. **Funciones Globales**: `ollama.chat(...)` -> Acceso directo a localhost.
2. **`Client` (Síncrono)**: Gestión de múltiples hosts, timeouts y headers.
3. **`AsyncClient` (Asincrónico)**: Ideal para FastAPI y alta concurrencia.

---

# 2.3 Inspección de Hardware (Práctica)

Entendiendo los límites de tu máquina antes de cargar modelos.

```python
import ollama

def check_models():
    models = ollama.list()
    for m in models['models']:
        size_gb = m['size'] / (1024**3)
        print(f"Modelo: {m['name']} | {size_gb:.2f} GB")

    # ¿Qué hay cargado en la GPU/RAM ahora mismo?
    active = ollama.ps()
    print(f"Modelos en memoria: {active['models']}")
```

- **Offloading**: Si el modelo > VRAM, Ollama usa RAM del sistema (mucho más lento).

---

# 3. Inferencia: Generate vs Chat

Dos formas de interactuar con el modelo según el caso de uso.

### 3.1 Generate API (Inferencia Atómica)
Ideal para tareas de NLP puras (Extracción, Clasificación, Resumen). **Sin historial.**

```python
response = ollama.generate(
    model='llama3', 
    prompt='Extrae nombres de personas del texto...',
    format='json' # ¡Crucial para integración técnica!
)
```

### 3.2 Chat API (Gestión de Contexto)
Maneja una conversación secuencial. El modelo es *stateless*, requiere enviar todo el historial.

- `system`: Reglas inamovibles.
- `user`: Peticiones del humano.
- `assistant`: Respuestas previas de la IA.

---

# 3.3 Streaming y Experiencia de Usuario

Elimina la latencia percibida recibiendo fragmentos en tiempo real.

```python
def stream_demo():
    for chunk in ollama.chat(
        model='llama3',
        messages=[{'role': 'user', 'content': 'Escribe un ensayo...'}],
        stream=True
    ):
        print(chunk['message']['content'], end='', flush=True)
```

### Ventajas del Streaming:
- **UX Inmediata**: El usuario ve actividad al instante.
- **Eficiencia**: Procesa el texto mientras se sigue generando.

---

# 4. Tools y Function Calling (Nivel Experto)

Permite que el modelo interactúe con el mundo real a través de tu código.

### El Flujo de Trabajo
1. **Definición**: Pasas un JSON Schema de tus funciones Python al modelo.
2. **Razonamiento**: Si el modelo necesita datos (ej: clima), devuelve una `tool_call`.
3. **Ejecución**: Tu script ejecuta la función real en Python.
4. **Respuesta**: Reinyectas el resultado al modelo para la respuesta final.

### Modelos Optimizados
Se requieren modelos entrenados para esto: **Llama 3.1**, **Mistral**, **Gemma 2**.

---

# 4.2 Ejemplo de Agente Meteorológico

```python
tools = [{
    'type': 'function',
    'function': {
        'name': 'get_weather',
        'description': 'Obtiene el clima de una ciudad',
        'parameters': {'type': 'object', 'properties': {'city': {'type': 'string'}}}
    }
}]

# 1. El modelo detecta que necesita llamar a la función
response = ollama.chat(model='llama3.1', messages=msj, tools=tools)

# 2. Ejecutas la función real y devuelves el resultado
if response['message'].get('tool_calls'):
    result = execute_python_logic(args['city'])
    # 3. Respuesta final con datos reales
```

---

# 5. Visión y Modelos Multimodales

Procesamiento de imágenes con modelos como `llava` o `moondream`.

### Casos de Uso
1. **OCR Avanzado**: Lectura inteligente de facturas y tickets.
2. **Accesibilidad**: Describir imágenes para personas con discapacidad visual.
3. **QA Automático**: Analizar capturas de pantalla de interfaces.

```python
with open('img.png', 'rb') as f:
    res = ollama.generate(
        model='llava',
        prompt='¿Qué dice el cartel de fondo?',
        images=[f.read()]
    )
```

---

# 6. Embeddings: Del Texto a Vectores

La base matemática de la comparación semántica.

- **Espacio Vectorial**: Representación numérica del significado.
- **Similitud del Coseno**: Medición del ángulo entre vectores para saber si dos frases son similares.

```python
# Generar el "ADN matemático" de una frase
v1 = ollama.embeddings(model='mxbai-embed-large', prompt='El gato duerme')['embedding']
v2 = ollama.embeddings(model='mxbai-embed-large', prompt='Un felino descansa')['embedding']
```

> **Metáfora del Mapa**: Palabras con significados similares son "ciudades" cercanas en este mapa matemático.

---

# 6.2 Arquitectura RAG

**Retrieval Augmented Generation**: "Examen a libro abierto" para el LLM.

### Los 4 Pilares:
1. **Chunking**: Fragmentar documentos para no saturar el contexto.
2. **Vector DB**: Almacén rápido de vectores (ChromaDB, FAISS).
3. **Retrieval**: Buscar los fragmentos más relevantes para la duda del usuario.
4. **Inyección**: Replantear el prompt original añadiendo esos fragmentos como "apuntes".

---

# 6.3 Implementación de RAG (Ejemplo)

```python
def asistente_soporte(pregunta):
    # 1. Buscar contexto relevante en nuestra DB vectorial
    contexto = vector_db.search(pregunta)
    
    # 2. Inyectar en el prompt
    prompt = f"Usa SOLO este contexto: {contexto}. Pregunta: {pregunta}"
    
    # 3. Generar respuesta
    res = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
    return res['message']['content']
```

- **Solución al "Corte de Conocimiento"**: El modelo accede a datos actualizados de tus PDFs o bases de datos sin re-entrenamiento.

---

# 7. Escalabilidad y Asincronía

No bloquees tu servidor mientras la IA piensa.

### Uso de `AsyncClient`
```python
import asyncio
from ollama import AsyncClient

async def run_parallel():
    client = AsyncClient()
    tasks = [client.generate(model='llama3', prompt=f'Tema {i}') for i in range(5)]
    results = await asyncio.gather(*tasks)
```

- **Imprescindible**: Para aplicaciones en producción o servicios web (FastAPI).

---

# 8. Gestión de Modelos (CRUD Completo)

Control total sobre el ciclo de vida de tus modelos.

- **Pull**: Descarga y actualización automática.
- **List/PS**: Control de inventario y estado en VRAM.
- **Delete**: Gestión de espacio en disco (limpieza técnica).

### Ejemplo de Pull con Progreso
```python
for progress in ollama.pull('llama3', stream=True):
    percent = (progress.get('completed', 0) / progress.get('total', 1)) * 100
    print(f"\rProgreso: {percent:.1f}%", end='')
```

---

# 8.3 Customización: `Create` y `Modelfile`

Crea tus propios modelos especializados.

### El Archivo de Configuración (`Modelfile`)
```dockerfile
FROM llama3
SYSTEM Eres un experto en Python que solo responde en código.
PARAMETER temperature 0.1
PARAMETER num_ctx 4096
```

### Creación vía API
```python
ollama.create(model='python-expert', modelfile=content)
```
- Permite "congelar" configuraciones de temperatura y prompts de sistema complejos.

---

# 8.4 Gestión de Variantes y Publicación

- **Copy**: Clonar modelos para probar diferentes configuraciones sin descargar de nuevo.
- **Push**: Subir tus modelos personalizados a la librería de Ollama (requiere auth).

```python
# Clonar para backups o variantes
ollama.copy('llama3', 'llama3-testing-temp-0.8')

# Eliminar modelos obsoletos
ollama.delete('llama3-testing-temp-0.8')
```

---
layout: center
class: text-center
---

# ¡Fin del Curso Avanzado!

## ¿Listo para construir la próxima generación de IAs locales?

[Acceder al código completo](ollama_python.adoc)
