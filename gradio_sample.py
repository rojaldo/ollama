import gradio as gr
import ollama

# crea el cliente de Ollama
client = ollama.Client(host='http://localhost:11434')

def chat_with_ollama(message, history):
    # Usamos el modelo 'llama3.2' como ejemplo, asegúrate de tenerlo descargado (ollama pull llama3.2)
    response = client.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': message},
    ])
    return response['message']['content']

demo = gr.ChatInterface(
    fn=chat_with_ollama,
    title="Chat con Ollama",
    description="Interfaz de chat simple integrada con Ollama.",
    examples=["¿Qué es un LLM?", "¿Cómo funciona Ollama?", "Escribe un poema corto sobre IA."]
)

if __name__ == "__main__":
    demo.launch()