---
theme: seriph
background: https://source.unsplash.com/collection/94734566/1920x1080
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  ## Presentación Completa de Inteligencia Artificial
  Basado en el documento ia.adoc
drawings:
  persist: false
transition: slide-left
title: Inteligencia Artificial - Curso Completo
---

# Inteligencia Artificial
## Una visión pedagógica y técnica profunda

---

# ¿Qué es la IA?

La inteligencia artificial es la inteligencia exhibida por máquinas. No es solo "programar", es **emular funciones cognitivas**.

### Las Tres Dimensiones de la Mente Artificial:

- **Percepción**: Capacidad de interpretar datos sensoriales. La IA no ve píxeles, ve un "gato"; no oye ondas, oye "voz".
- **Razonamiento y Decisión**: Evaluación de probabilidades y lógica para cumplir objetivos (ej: un coche autónomo decidiendo frenar).
- **Aprendizaje (Adaptación)**: El pilar moderno. El sistema ajusta sus parámetros internos analizando miles de ejemplos para mejorar con el tiempo.

<br>

> **Metáfora del Aprendiz**: Un aprendiz con memoria fotográfica infinita pero sin sentido común inicial que refina su modelo con cada error.

---

# Clasificación y Filosofías

### Por su alcance (ANI vs AGI)
1. **IA Débil (ANI)**: Especialista. Excelente en una sola tarea (Ajedrez, GPT, Reconocimiento facial). Es nuestra realidad actual.
2. **IA Fuerte (AGI)**: El "Santo Grial". Inteligencia igual o superior a la humana en **cualquier** tarea cognitiva. Autoconciencia y razonamiento abstracto.

### Evolución del Pensamiento
- **Simbólica (Top-Down)**: Dominó 1950-1980. Inteligencia como manipulación de símbolos y reglas lógicas explícitas (`SI... ENTONCES`).
- **Conexionista (Bottom-Up)**: El paradigma actual. No damos reglas, damos una estructura (redes neuronales) y datos para que la máquina descubra las reglas.

---

# Historia: El Viaje de la IA (I)

La historia de la IA no es lineal; es un ciclo de optimismo y decepción ("Inviernos").

1. **El Nacimiento (1950-1956)**: Alan Turing publica "¿Pueden las máquinas pensar?". En 1956, John McCarthy acuña el término en **Dartmouth**.
2. **Era Dorada (1956-1974)**: Programas que resolvían álgebra y demostraban teoremas. Se creía que la IA superaría al hombre en 20 años.
3. **Primer Invierno (1974-1980)**: El optimismo chocó con el hardware limitado. El **Informe Lighthill** provocó recortes masivos de fondos.
4. **Sistemas Expertos (1980-1987)**: Auge comercial. IA basada en manuales de expertos humanos para diagnóstico médico y logística corporativa.

---

# Las Etapas Históricas (II)

4. **Sistemas Expertos (1980-1987)**: IA aplicada a diagnóstico médico y logística corporativa.
5. **Segundo Invierno (1987-1993)**: Fracaso comercial de máquinas Lisp y dificultad de mantenimiento.
6. **Revolución Big Data (2010-Presente)**: GPUs potentes y Deep Learning masivo.

---

# Hitos del Intelecto Humano vencido

- **1997**: Deep Blue vence a Kasparov (Fuerza bruta algorítmica).
- **2011**: Watson gana Jeopardy! (Comprensión de contexto y lenguaje natural).
- **2016**: AlphaGo vence a Lee Sedol (Intuición mediante Redes Neuronales).
- **2021**: GPT-3 marca la era de los Modelos de Lenguaje Masivos.

---

# Técnicas: Heurística y Búsqueda

- **Heurística**: "Atajos mentales" que aceleran la solución de problemas.
- **Árboles de Búsqueda**:
  - **BFS (Anchura)**: Explora vecinos inmediatos (como buscar llaves habitación por habitación).
  - **DFS (Profundidad)**: Sigue una rama hasta el final (como salir de un laberinto con una pared).

---

# Redes Neuronales Artificiales (ANN)

Conocidas técnicamente como **Multi-Layer Perceptron (MLP)**. Se basan en capas jerárquicas de unidades de procesamiento.

### El Sistema de Filtrado de Información:
- **Capa de Entrada**: Interfaz con el mundo. Cada neurona es una característica (ej: número de habitaciones, antigüedad).
- **Capas Ocultas**: Donde reside la "inteligencia". Encuentran **patrones abstractos** (ej: combinar antigüedad y m2 para inferir "estado de conservación").
- **Capa de Salida**: Traduce el conocimiento en una decisión (ej: estimación de precio).

### El Ciclo de Aprendizaje:
1. **Forward Pass**: Los datos viajan a la salida y el modelo hace una predicción (normalmente errónea al inicio).
2. **Loss Function**: Cálculo de la diferencia entre la predicción y la realidad.
3. **Backpropagation**: El error vuelve atrás por la red ajustando los **Pesos (Weights)** mediante **Gradiente Descendente**.

---

# Vision Artificial: CNN

Especialmente diseñadas para datos con estructura de cuadrícula (imágenes). Introducen la **"Mirada Fragmentada"**.

### Componentes Clave:
- **Filtros (Kernels)**: Mirillas que se deslizan por la imagen buscando bordes, curvas y más tarde objetos complejos.
- **Mapas de Características**: Representación de dónde la red ha detectado patrones específicos.
- **Pooling (Submuestreo)**: Técnica de compresión que mantiene solo lo relevante, permitiendo **invariancia de traslación** (reconocer al gato esté donde esté).

> **Jerarquía de Reconocimiento**: Capas iniciales ven colores/bordes -> Capas medias ven formas -> Capas profundas ven "caras" u "objetos".

---

# Memoria y Secuencia: RNN y LSTM

Diseñadas para datos que dependen del orden, como el lenguaje o el mercado de valores.

### RNN (Redes Recurrentes)
- **Concepto**: Tienen un bucle que permite pasar información del "pasado" al "presente".
- **Problema**: **Desvanecimiento del Gradiente**. Olvidan el inicio de secuencias largas (efecto "teléfono escacharrado").

### LSTM (Long Short-Term Memory)
El "Archivista Selectivo" que soluciona el olvido mediante **Puertas (Gates)**:
- **Olvido**: Decide qué información borrar de la memoria central.
- **Entrada**: Filtra qué nuevos datos merecen guardarse.
- **Salida**: Decide qué parte de la memoria interna se enviará a la siguiente capa.

---

# Transformers: El Mecanismo de Auto-Atención

El "corazón" que permite a las máquinas entender el contexto como nunca antes.

### ¿Cómo funciona la Auto-Atención (Self-Attention)?
- **Visión Global**: A diferencia de las redes anteriores que leían palabra por palabra (de izquierda a derecha), la auto-atención permite que cada palabra en una frase "mire" a todas las demás simultáneamente.
- **Resolución de Ambigüedades**: En la frase *"El banco estaba cerrado porque no tenía dinero"*, el modelo usa la atención para conectar "banco" con "dinero", deduciendo que es una institución financiera.
- **Relaciones a Larga Distancia**: Puede conectar el sujeto del inicio de un párrafo con un pronombre al final del mismo, manteniendo la coherencia global.

---

# Transformers: Procesamiento y Posición

¿Cómo logramos que una máquina sea tan rápida y precisa al procesar lenguaje?

### Procesamiento en Paralelo
- **Adiós a la Secuencialidad**: Las RNN necesitaban terminar la palabra 1 para empezar la 2. Los Transformers analizan todas las palabras de un párrafo a la vez.
- **Explosión de Potencia**: Esto permite aprovechar al 100% la potencia de las GPUs modernas, reduciendo semanas de entrenamiento a días.

### Codificación Posicional (Positional Encoding)
Al procesar todo a la vez, el modelo pierde el sentido del orden ("El perro muerde al hombre" parecería igual a "El hombre muerde al perro").
- **La Solución**: Se añade una señal matemática única a cada palabra que indica su posición exacta. El modelo "sabe" dónde está cada pieza del puzle.

---

# Transformers: La Arquitectura Dual

Basada en el artículo fundamental de 2017: *"Attention Is All You Need"*.

### El Encoder (Codificador)
Comprime la información de entrada en una representación numérica rica en significado. Es como un lector experto que resume perfectamente lo que ha leído.
- *Ejemplo*: **BERT** usa solo esta parte para entender el significado del texto.

### El Decoder (Decodificador)
Utiliza la representación rica del encoder (o la suya propia) para generar una secuencia de salida lógica, palabra por palabra.
- *Ejemplo*: **GPT** (Generative Pre-trained Transformer) usa principalmente esta parte para "predecir" la siguiente palabra y generar texto fluido.

---

# Impacto de los Transformers en la IA Moderna

Gracias a esta arquitectura, hemos pasado de traductores toscos a asistentes casi humanos.

### Logros Clave:
- **Capacidades Emergentes**: Al escalar el tamaño de estos modelos (billones de parámetros), aparecen habilidades no programadas explícitamente, como razonar lógicamente o programar código.
- **Modelos Fundacionales**: Han permitido que un solo modelo (como GPT-4) sea bueno en cientos de tareas diferentes sin entrenamiento específico para cada una.
- **La Base de Ollama**: Los modelos que corremos localmente (Llama 3, Mistral, Gemma) son, en su esencia, arquitecturas Transformer optimizadas.

---

# El Duelo Creativo: GAN

Las **Redes Neuronales Generativas Adversarias** se basan en la competencia entre dos modelos ("El Falsificador y el Detective").

### El Ciclo de Entrenamiento:
1. **El Generador**: Crea datos (imágenes, audio) desde ruido aleatorio intentando engañar al Detective.
2. **El Discriminador**: Recibe datos reales y falsificaciones, aprendiendo a distinguirlos.
3. **Feedback**: Si el Detective pilla el fraude, el Generador aprende a ser más realista. Si el Falsificador engaña al policía, el Detective debe esforzarse más.

**Resultado**: Generación de rostros, arte o video hiperrealista que no existe en el mundo real.

---

# La Nueva Ola: Modelos de Difusión

Han superado a las GAN en calidad y estabilidad para la generación de imágenes.

### Concepto: Destrucción y Reconstrucción
- **Difusión Directa**: Añade ruido a una imagen clara paso a paso hasta que es caos puro.
- **Difusión Inversa**: El modelo aprende a quitar el ruido paso a paso. Predice qué píxeles sobran para revelar la figura oculta.

### Guía y Espacio Latente:
- **Conditioning**: El proceso de quitar ruido está guiado por texto (ej: "astronauta en Marte").
- **Latent Space**: No trabajan con píxeles gigantes, sino en una versión matemática comprimida mucho más eficiente.

---

# Autoencoders: El Resumen Ejecutivo

- **Encoder**: Comprime 1MB de foto en un **Espacio Latente** (un post-it numérico).
- **Decoder**: Reconstruye la foto desde ese post-it.
- **Utilidad**: Eliminación de ruido y detección de anomalías.

---

# Aprendizaje por Refuerzo (RL)

Se utiliza para entrenar **agentes inteligentes** que operan en entornos dinámicos, aprendiendo mediante la interacción.

### Los Tres Pilares del RL:
- **El Agente**: La entidad que toma decisiones (ej: un robot o un software de ajedrez).
- **El Entorno**: El mundo donde vive el agente (reglas del juego, leyes físicas).
- **La Recompensa (Reward)**: La señal de éxito o fracaso que el agente busca maximizar a largo plazo.

> **Concepto clave**: Aprender a tomar **decisiones secuenciales**. No se trata de clasificar una foto hoy, sino de ganar una partida mañana.

---

# RL: El Ciclo de Decisión y Estrategia

¿Cómo aprende realmente una máquina a superar a los humanos en juegos complejos?

### El Bucle de Interacción:
1. **Observación**: El agente percibe el estado actual del entorno.
2. **Acción**: Ejecuta un movimiento basado en su **Política (Policy)**.
3. **Resultado**: Recibe una recompensa y el entorno pasa a un nuevo estado.

### Exploración vs. Explotación:
- **Exploración**: Probar acciones nuevas al azar para descubrir mejores recompensas (aprender).
- **Explotación**: Usar el conocimiento ya adquirido para asegurar la mejor recompensa conocida (ganar).

---

# Hitos y Algoritmos de RL

El campo ha pasado de resolver laberintos simples a dominar la estrategia militar y científica.

### Algoritmos Modernos:
- **DQN (Deep Q-Network)**: Redes neuronales que estiman el valor de cada acción.
- **PPO (Proximal Policy Optimization)**: Estándar actual por su estabilidad en el aprendizaje.

### Logros Paradigmáticos de DeepMind:
- **AlphaZero**: Aprendió ajedrez desde cero en 4 horas, superando a todos los humanos y motores previos sin usar datos humanos.
- **AlphaStar**: Derrotó a profesionales en StarCraft II, un juego de estrategia en tiempo real con "niebla de guerra" e información incompleta.
- **RLHF (Reinforcement Learning from Human Feedback)**: La técnica que hace que ChatGPT y Llama 3 sean educados y útiles, alineando la IA con las preferencias humanas.

---

# Aprendizaje Supervisado y No Supervisado

### Aprendizaje Supervisado (Con Etiquetas)
El modelo aprende una función que mapea entradas a salidas basándose en ejemplos etiquetados por humanos.
- **Clasificación**: Predecir una categoría discreta (ej: "¿Es spam o no?", "¿Es un gato o un perro?").
- **Regresión**: Predecir un valor numérico continuo (ej: "Precio de una vivienda", "Temperatura de mañana").
- **Algoritmos**: Regresión Lineal, Árboles de Decisión, SVM, Redes Neuronales.

### Aprendizaje No Supervisado (Sin Etiquetas)
El modelo debe encontrar por sí solo estructuras o patrones ocultos en datos que no tienen una respuesta correcta previa.
- **Clustering**: Agrupar datos similares (ej: segmentar clientes por comportamiento de compra).
- **Reducción de Dimensionalidad**: Simplificar datos complejos manteniendo la información esencial (PCA).
- **Detección de Anomalías**: Identificar datos que no encajan en el patrón normal (fraude bancario).

---

# Aprendizaje Semi-Supervisado y por Transferencia

Técnicas avanzadas para situaciones donde el etiquetado de datos es costoso o el entrenamiento es prohibitivo.

### Aprendizaje Semi-Supervisado
Combina una pequeña cantidad de datos etiquetados con una gran cantidad de datos no etiquetados.
- **Uso Crítico**: Cuando etiquetar datos requiere expertos caros (ej: radiografías médicas), pero tenemos miles de imágenes sin etiquetar disponibles.
- **Técnicas**: Auto-etiquetado (Pseudo-labeling) donde el modelo etiqueta los datos nuevos y luego se re-entrena con ellos.

### Aprendizaje por Transferencia (Transfer Learning)
Reutiliza el conocimiento de un modelo ya entrenado en un dominio masivo para una tarea específica y pequeña.
- **Fine-Tuning**: Tomar un modelo como Llama 3 y "ajustarlo" con unos pocos documentos médicos para que sea experto en medicina.
- **Ventaja**: Permite a empresas pequeñas tener IAs de vanguardia sin gastar millones en entrenamiento desde cero.

---

# Modelos Pre-entrenados y Conceptos Clave

¿Cómo se gestionan y distribuyen los modelos modernos que usamos en Ollama?

### Elementos de un Modelo:
- **Checkpoints (Puntos de control)**: Son "fotos" del estado del modelo durante su entrenamiento que contienen los pesos aprendidos.
- **Espacio Latente (Latent Space)**: La representación matemática interna donde el modelo "entiende" los conceptos. En este espacio, "Rey" y "Reina" están cerca pero separados por el concepto "Género".
- **Inferencia**: El proceso de usar el modelo ya entrenado para responder. Es lo que hacemos cuando le preguntamos algo a Ollama.

### Modelos de Lenguaje (LLMs):
- **Fundacionales**: Entrenados en casi todo internet para entender el lenguaje general (GPT-4, Llama 3, Mistral).
- **Multimodales**: Modelos que no solo entienden texto, sino también imágenes y audio simultáneamente (ej: LLaVA).

---

# Ecosistema de Librerías

- **PyTorch (Meta)**: Favorita en investigación y prototipos.
- **TensorFlow (Google)**: Estándar industrial y despliegue masivo.
- **Scikit-learn**: El rey del Machine Learning clásico en Python.
- **OpenCV**: La visión artificial tradicional y procesamiento de imagen.

---
layout: center
class: text-center
---

# ¡Gracias por vuestra atención!

¿Alguna pregunta sobre el futuro de la IA?
