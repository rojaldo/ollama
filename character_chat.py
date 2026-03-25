import gradio as gr
import ollama

# crea el cliente de Ollama
client = ollama.Client(host='http://localhost:11434')

def chat_with_ollama(message, history, character):
    # Construimos la lista de mensajes con el contexto
    messages = [{'role': 'system', 'content': f'Eres {character}.'}]
    
    # En algunas versiones de Gradio, el mensaje actual puede venir como una lista de dicts
    # Ollama espera que content sea siempre una cadena (string) para mensajes simples
    if isinstance(message, list):
        # Intentamos extraer el texto si viene en el formato [{'text': '...', 'type': 'text'}]
        message = " ".join([m['text'] for m in message if 'text' in m])
    elif isinstance(message, dict) and 'text' in message:
        message = message['text']

    for interaction in history:
        if isinstance(interaction, (list, tuple)):
            user_msg, bot_msg = interaction
            # Limpiamos el contenido si viene en formato estructurado de Gradio
            if isinstance(user_msg, list):
                user_msg = " ".join([m['text'] for m in user_msg if 'text' in m])
            elif isinstance(user_msg, dict) and 'text' in user_msg:
                user_msg = user_msg['text']
            
            messages.append({'role': 'user', 'content': str(user_msg)})
            messages.append({'role': 'assistant', 'content': str(bot_msg)})
        elif isinstance(interaction, dict):
            # Clonamos el dict para no modificar el original de Gradio
            clean_msg = interaction.copy()
            if isinstance(clean_msg.get('content'), list):
                clean_msg['content'] = " ".join([m['text'] for m in clean_msg['content'] if 'text' in m])
            messages.append(clean_msg)
    
    # Añadimos el mensaje actual del usuario
    messages.append({'role': 'user', 'content': str(message)})

    # Usamos el modelo 'llama3.2' como ejemplo, asegúrate de tenerlo descargado (ollama pull llama3.2)
    response = client.chat(model='llama3.2', messages=messages)
    return response['message']['content']

# add a character selector to the interface

demo = gr.ChatInterface(
    fn=chat_with_ollama,
    additional_inputs=[
        gr.Dropdown(
            choices=["Mario Bros", "Sherlock Holmes", "Albert Einstein", "Yoda", "Batman"],
            value="Mario Bros",
            label="Selecciona un Personaje"
        )
    ],
    title="Chat con Ollama",
    description="Interfaz de chat simple integrada con Ollama.",
    examples=[
        ["¿Qué es un LLM?", "Mario Bros"],
        ["¿Cómo funciona Ollama?", "Sherlock Holmes"],
        ["Escribe un poema corto sobre IA.", "Albert Einstein"]
    ]
)

if __name__ == "__main__":
    demo.launch()