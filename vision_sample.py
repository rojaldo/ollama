import gradio as gr
import ollama
import base64
import os
from pathlib import Path
from PIL import Image
import io

# Crea el cliente de Ollama
client = ollama.Client(host='http://localhost:11434')

def encode_image_to_base64(image_path):
    """Convierte una imagen a base64 para enviar al modelo de visión"""
    with open(image_path, "rb") as image_file:
        return base64.standard_b64encode(image_file.read()).decode("utf-8")

def analyze_clothing(image, language="es"):
    """
    Analiza una prenda de ropa usando Llama Vision.
    
    Args:
        image: Imagen subida desde Gradio (PIL Image object)
        language: Idioma para la respuesta ('es' o 'en')
    
    Returns:
        Análisis detallado de la prenda
    """
    try:
        if image is None:
            return "Por favor, sube una imagen primero."
        
        # Convierte la imagen PIL a formato base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.standard_b64encode(buffered.getvalue()).decode("utf-8")
        
        # Define el prompt según el idioma
        if language == "es":
            prompt = """Analiza esta imagen de una prenda de ropa y proporciona un análisis detallado que incluya:

1. **Tipo de prenda**: ¿Qué tipo de prenda es? (camiseta, pantalón, vestido, chaqueta, etc.)
2. **Color(es) principal(es)**: Describe los colores predominantes
3. **Material aparente**: ¿Qué material parece ser? (algodón, poliéster, lana, mezclilla, etc.)
4. **Estilo/Diseño**: ¿Cuál es el estilo? (casual, formal, deportivo, vintage, etc.)
5. **Características especiales**: ¿Tiene botones, cremalleras, estampados, patrones, bordados, etc.?
6. **Condición**: ¿En qué condición se ve? (nueva, usada, desgastada, etc.)
7. **Posible marca/colección**: Si se identifica alguna marca o etiqueta visible
8. **Recomendaciones de cuidado**: Sugerencias de lavado/mantenimiento basadas en la apariencia

Por favor, sé específico y detallado en tus observaciones."""
        else:
            prompt = """Analyze this clothing item image and provide a detailed analysis including:

1. **Type of garment**: What type of clothing is it? (t-shirt, pants, dress, jacket, etc.)
2. **Main color(s)**: Describe the predominant colors
3. **Apparent material**: What material does it appear to be? (cotton, polyester, wool, denim, etc.)
4. **Style/Design**: What is the style? (casual, formal, sporty, vintage, etc.)
5. **Special features**: Does it have buttons, zippers, prints, patterns, embroidery, etc.?
6. **Condition**: What condition does it appear to be in? (new, used, worn, etc.)
7. **Possible brand/collection**: If any brand or visible label is identified
8. **Care recommendations**: Suggestions for washing/maintenance based on appearance

Please be specific and detailed in your observations."""
        
        model_name = "llama3.2-vision:latest"
        
        response = client.generate(
            model=model_name,
            prompt=prompt,
            images=[img_base64],  # Pasa la imagen en base64
            stream=False
        )
        
        return response['response']
    
    except ollama.ResponseError as e:
        if "unknown model" in str(e).lower():
            return f"""❌ Error: El modelo '{model_name}' no está disponible en Ollama.

Para usar análisis de imágenes, primero descarga el modelo de visión:
```bash
ollama pull llava
```

O si prefieres un modelo más ligero:
```bash
ollama pull llava-phi
```

Después, asegúrate de que Ollama está ejecutándose:
```bash
ollama serve
```
"""
        else:
            return f"❌ Error de Ollama: {str(e)}"
    
    except Exception as e:
        return f"❌ Error al procesar la imagen: {str(e)}\n\nAsegúrate de que:\n1. Ollama está ejecutándose (ollama serve)\n2. El modelo 'llava' está descargado (ollama pull llava)"

def create_sample_analysis(language="es"):
    """Retorna un análisis de ejemplo"""
    if language == "es":
        return """**Análisis de ejemplo (Camiseta):**

1. **Tipo de prenda**: Camiseta/Polera de manga corta
2. **Color(es) principal(es)**: Azul marino (Pantone 533) con detalles en blanco
3. **Material aparente**: Algodón 100% tejido jersey
4. **Estilo/Diseño**: Casual, deportivo moderno con cuello redondo
5. **Características especiales**: 
   - Estampado gráfico minimalista en el pecho
   - Costuras reforzadas en los hombros
   - Etiqueta visible de marca en el cuello
6. **Condición**: Excelente, parece nueva o casi nueva sin signos de desgaste
7. **Posible marca**: Etiqueta visible de marca premium
8. **Recomendaciones de cuidado**: 
   - Lavar con agua fría (máx 30°C)
   - Dar vuelta antes de lavar para proteger el estampado
   - Secar al aire de preferencia
   - Planchar a baja temperatura si es necesario"""
    else:
        return """**Example Analysis (T-Shirt):**

1. **Type of garment**: Short-sleeve t-shirt/tee
2. **Main color(s)**: Navy blue (Pantone 533) with white accents
3. **Apparent material**: 100% cotton jersey knit
4. **Style/Design**: Casual, modern sporty with crew neck
5. **Special features**: 
   - Minimalist graphic print on the chest
   - Reinforced seams on the shoulders
   - Visible brand label on the neck
6. **Condition**: Excellent, appears new or nearly new with no signs of wear
7. **Possible brand**: Premium brand label visible
8. **Care recommendations**: 
   - Wash in cold water (max 30°C)
   - Turn inside out before washing to protect the graphic
   - Air dry preferably
   - Iron at low temperature if necessary"""

# Crea la interfaz de Gradio
def create_interface():
    with gr.Blocks(title="Reconocimiento de Prendas de Ropa", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
# 👕 Analizador de Prendas de Ropa
## Con Visión por IA (Llama Vision + Ollama)

Sube una foto de una prenda de ropa y obtén un análisis detallado con información sobre:
- Tipo de prenda
- Colores y materiales
- Estilo y diseño
- Condiciones especiales
- Recomendaciones de cuidado

> **Nota**: Requiere que `ollama pull llava` esté instalado.
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Subir Imagen 📷")
                image_input = gr.Image(
                    type="pil",
                    label="Selecciona una imagen de prenda",
                    sources=["upload", "webcam"]
                )
                
                language_choice = gr.Radio(
                    choices=[("Español 🇪🇸", "es"), ("English 🇬🇧", "en")],
                    value="es",
                    label="Idioma del análisis",
                    interactive=True
                )
                
                analyze_btn = gr.Button(
                    "🔍 Analizar Prenda",
                    variant="primary",
                    size="lg"
                )
            
            with gr.Column(scale=1):
                gr.Markdown("### Análisis de la Prenda 📊")
                output_text = gr.Textbox(
                    label="Resultado del análisis",
                    lines=20,
                    max_lines=30,
                    interactive=False
                )
        
        # Fila de ejemplos
        gr.Markdown("### Ejemplos 📚")
        with gr.Row():
            example_es_btn = gr.Button("Ver ejemplo (Español)")
            example_en_btn = gr.Button("Ver example (English)")
        
        # Acciones de los botones
        analyze_btn.click(
            fn=analyze_clothing,
            inputs=[image_input, language_choice],
            outputs=output_text
        )
        
        example_es_btn.click(
            fn=lambda: create_sample_analysis("es"),
            outputs=output_text
        )
        
        example_en_btn.click(
            fn=lambda: create_sample_analysis("en"),
            outputs=output_text
        )
        
        gr.Markdown("""
---
### 🛠️ Requisitos
- **Ollama** ejecutándose en `localhost:11434`
- Modelo descargado: `ollama pull llava`

### 📝 Cómo usar
1. Sube una imagen de la prenda de ropa
2. Selecciona el idioma preferido
3. Haz clic en "Analizar Prenda"
4. Espera a que se procese la imagen

### ⚙️ Instalación rápida
```bash
# 1. Descargar el modelo de visión
ollama pull llava

# 2. Ejecutar Ollama (en otra terminal)
ollama serve

# 3. Ejecutar este script
python vision_sample.py
```
        """)
    
    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(share=False)
