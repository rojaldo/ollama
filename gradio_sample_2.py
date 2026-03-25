import gradio as gr

def procesar_datos(texto, numero, imagen):
    # Lógica de procesamiento aquí
    return f"Procesado: {texto}", numero * 2, imagen

demo = gr.Interface(
    fn=procesar_datos,
    inputs=[
        gr.Textbox(label="Mensaje"),
        gr.Slider(0, 100, label="Puntuación"),
        gr.Image(label="Sube una foto")
    ],
    outputs=["text", "number", "image"]
)

demo.launch()