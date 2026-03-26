# 👕 Analizador de Prendas de Ropa con Visión IA

Sistema completo de reconocimiento de prendas de ropa usando **Gradio** + **Ollama** + **Llama Vision**.

## 📋 Características

- ✅ Interfaz web intuitiva con Gradio
- ✅ Análisis detallado de prendas de ropa
- ✅ Soporte para captura de cámara web
- ✅ Resultados en Español e Inglés
- ✅ Información sobre materiales, colores, estilos y cuidado
- ✅ Seguro (todo se ejecuta localmente)

## 🚀 Inicio Rápido

### 1. Requisitos Previos

Asegúrate de tener:
- **Python 3.7+**
- **Ollama** instalado y ejecutándose
- Acceso a internet (para descargar el modelo la primera vez)

### 2. Descargar el Modelo de Visión

```bash
ollama pull llava
```

Alternativas más ligeras:
```bash
ollama pull llava-phi    # Versión más pequeña y rápida
```

### 3. Ejecutar Ollama

En una terminal dedicada:
```bash
ollama serve
```

Verás:
```
listening on 127.0.0.1:11434
```

### 4. Instalar Dependencias (Si es necesario)

```bash
pip install gradio ollama pillow
```

Ya están instaladas en tu `requirements.txt`, pero puedes verificar:
```bash
pip list | grep -E "gradio|ollama|pillow"
```

### 5. Ejecutar la Aplicación

```bash
# Opción 1: Desde el directorio del script
python vision_sample.py

# Opción 2: Con ruta completa
cd /home/rojaldo/cursos/llm/ollama/samples/ollama_01
python vision_sample.py
```

### 6. Acceder a la Interfaz

La aplicación se abrirá automáticamente en tu navegador:
```
http://localhost:7860
```

Si no se abre automáticamente, ve manualmente a esa URL.

## 📖 Cómo Usar

1. **Subir Imagen**: Haz clic en "Selecciona una imagen de prenda"
   - Puedes arrastrar y soltar
   - O hacer clic para seleccionar desde archivos
   - O capturar desde webcam

2. **Seleccionar Idioma**: Elige Español o English

3. **Analizar**: Haz clic en "🔍 Analizar Prenda"

4. **Ver Resultado**: El análisis aparecerá en la columna derecha

### Ejemplos de Análisis

El sistema proporcionará:

```
✅ Tipo de prenda: Camiseta/Polera
✅ Colores principales: Azul navy + Blanco
✅ Material: Algodón 100%
✅ Estilo: Casual deportivo
✅ Características especiales: Estampado gráfico, costuras reforzadas
✅ Condición: Excelente/Nueva
✅ Marca: [Si está visible]
✅ Recomendaciones de cuidado: Información específica
```

## 🔧 Opciones Avanzadas

### Cambiar Modelo de Visión

Edita el archivo `vision_sample.py` y cambia:

```python
model_name = "llava"  # Cambiar a "llava-phi" o otro modelo
```

### Modelos Disponibles en Ollama

```bash
ollama pull llava         # LLaVA 7B - Recomendado (mejor precisión)
ollama pull llava-phi     # LLaVA Phi - Más ligero y rápido
ollama pull llava-llama2  # LLaVA con Llama 2
```

### Personalizar Prompts

Modifica la sección de `prompts` en el código para cambiar las preguntas:

```python
if language == "es":
    prompt = """Tu prompt personalizado aquí..."""
```

## 🐛 Solución de Problemas

### Error: "Unknown model 'llava'"

**Solución**:
```bash
ollama pull llava
```

Espera a que se descargue completamente (puede tomar varios minutos).

### Error: "Connection refused" o "Cannot connect to Ollama"

**Solución**:
1. Verifica que Ollama está ejecutándose:
```bash
ps aux | grep ollama
```

2. Inicia Ollama si no está corriendo:
```bash
ollama serve
```

3. Verifica que escucha en `localhost:11434`:
```bash
curl http://localhost:11434/api/tags
```

### La aplicación es muy lenta

**Solución**: Usa un modelo más ligero:
```bash
# Cambiar en el código a:
model_name = "llava-phi"
```

O incrementa los recursos de tu sistema.

### La imagen no se carga bien

**Solución**:
- Asegúrate de que es un formato soportado (PNG, JPG, JPEG, BMP)
- El tamaño recomendado es menor a 5MB
- Intenta con otra imagen

## 📊 Ejemplos de Entrada

La aplicación funciona mejor con:

✅ **Buenas candidatas aplicadas**:
- Camisetas y poleras
- Pantalones y jeans
- Vestidos
- Chaquetas y abrigos
- Faldas
- Accesorios (bufandas, gorros)

⚠️ **Puede tener dificultades con**:
- Imágenes muy oscuras
- Objetos que no son ropa
- Fotos de grupo (enfécate en una prenda)

## 📝 Notas Técnicas

- **Framework**: Gradio 6.9+
- **Motor de IA**: Ollama + LLaVA (Llama Vision)
- **Lenguaje**: Python 3.14
- **Host**: localhost:11434
- **Puerto Gradio**: 7860 (por defecto)

## 🎯 Casos de Uso

1. **E-commerce**: Describir productos automáticamente
2. **Moda**: Analizar tendencias en prendas
3. **Recomendaciones**: Sugerir prendas similares
4. **Inventario**: Catalogar prendas rápidamente
5. **Educación**: Enseñar sobre materiales y estilos
6. **Sostenibilidad**: Evaluar condición y durabilidad

## 🚀 Siguientes Pasos

Una vez que funcione, puedes:

1. **Entrenar modelos personalizados**: Fine-tune para tu dominio específico
2. **Agregar base de datos**: Guardar análisis en base de datos
3. **Integrar con e-commerce**: Conectar con plataformas de venta
4. **Análisis batch**: Procesar múltiples imágenes
5. **API REST**: Exponer como servicio web

## 📞 Soporte

Si encuentras problemas:

1. Verifica que Ollama está ejecutándose
2. Comprueba el modelo con: `ollama list`
3. Mira los logs de Ollama
4. Prueba con una imagen diferente

---

**Versión**: 1.0  
**Última actualización**: Marzo 2026  
**Estado**: ✅ Funcional y Listo para Usar
