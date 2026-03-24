from ollama import Client

# Ejemplo con Cliente Síncrono configurado
# Ideal si Ollama corre en un servidor externo o en Docker con puerto mapeado
client = Client(host='http://localhost:11434')

try:
    response = client.list()
    print("Conexión exitosa al servidor remoto.")
    # chat 
    response = client.chat(model="llama3.2", messages=[
        {"role": "system", "content": "Eres un asistente de cine que responde preguntas sobre películas y actores. Responde en formato JSON con una lista de películas. No pongas nada mas, no hagas frases de cortesía, responde como una máquina"},
        {"role": "assistant", "content": "¡Hola! Estoy aquí para ayudarte con preguntas sobre cine."},
        {"role": "user", "content": "¿Qué películas ha hecho Bruce Willis?"}])
    print("Respuesta del modelo:", response)
except Exception as e:
    print(f"Error de conexión: {e}")