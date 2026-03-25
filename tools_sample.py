"""
Tools para Ollama - Demonstración de Function Calling con Gradio
Implementa 3 herramientas:
1. Obtener hora actual
2. API de Chuck Norris para chistes
3. API de Star Wars para datos de personajes
"""

import json
import requests
from datetime import datetime
from typing import Any
import gradio as gr
from ollama import Client

# Inicializar cliente Ollama
client = Client(host='http://localhost:11434')

# ==================== DEFINICIÓN DE HERRAMIENTAS ====================

tools = [
    {
        "type": "function",
        "function": {
            "name": "hora_actual",
            "description": 'Obtiene la hora actual formateada en HH:MM:SS.',
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_chuck_norris_joke",
            "description": "Obtiene un chiste de Chuck Norris",
            "parameters": {
                "type": "object",
                "properties": {

                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_star_wars_character",
            "description": "Obtiene información de un personaje de Star Wars de la API",
            "parameters": {
                "type": "object",
                "properties": {
                    "character": {
                        "type": "string",
                        "description": "Nombre del personaje (ej: 'Luke Skywalker')"
                    }
                },
                "required": ["character"]
            }
        }
    }
]

# ==================== IMPLEMENTACIÓN DE HERRAMIENTAS ====================

def hora_actual() -> str:
    """Obtiene la hora actual"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_chuck_norris_joke() -> dict:
    """Obtiene un chiste de Chuck Norris desde la API"""

    url = "https://api.chucknorris.io/jokes/random"
    try:
        
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        print(f"Chiste obtenido: {data.get('value')}")
        
        return {
            "success": True,
            "joke": data.get("value", "No se pudo obtener el chiste"),
            "category": data.get("categories", ["general"])[0] if data.get("categories") else "general"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Error al conectar con la API de Chuck Norris: {str(e)}"
        }


def get_star_wars_character(character: str) -> dict:
    """Obtiene información de un personaje de Star Wars"""
    try:
        # Buscar el personaje
        search_url = "https://swapi.dev/api/people/"
        response = requests.get(search_url, timeout=5)
        response.raise_for_status()
        
        people = response.json().get("results", [])
        
        # Buscar por nombre (búsqueda simple)
        found_character = None
        for person in people:
            if character.lower() in person.get("name", "").lower():
                found_character = person
                break
        
        if found_character:
            # Obtener información adicional de películas
            films = found_character.get("films", [])
            film_names = []
            for film_url in films:
                try:
                    film_response = requests.get(film_url, timeout=5)
                    film_response.raise_for_status()
                    film_names.append(film_response.json().get("title"))
                except:
                    pass
            
            return {
                "success": True,
                "name": found_character.get("name", "N/A"),
                "birth_year": found_character.get("birth_year", "N/A"),
                "height": found_character.get("height", "N/A"),
                "mass": found_character.get("mass", "N/A"),
                "hair_color": found_character.get("hair_color", "N/A"),
                "skin_color": found_character.get("skin_color", "N/A"),
                "eye_color": found_character.get("eye_color", "N/A"),
                "gender": found_character.get("gender", "N/A"),
                "homeworld": found_character.get("homeworld", "N/A"),
                "films": film_names
            }
        else:
            return {
                "success": False,
                "error": f"No se encontró el personaje '{character}' en la API de Star Wars"
            }
    
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Error al conectar con la API de Star Wars: {str(e)}"
        }


# ==================== PROCESADOR DE HERRAMIENTAS ====================

def process_tool_call(tool_name: str, tool_input: dict) -> str:
    """
    Procesa las llamadas a herramientas y retorna el resultado
    """
    if tool_name == "hora_actual":
        result = hora_actual()
        return json.dumps({"result": result})
    
    elif tool_name == "get_chuck_norris_joke":
        result = get_chuck_norris_joke()
        return json.dumps(result)
    
    elif tool_name == "get_star_wars_character":
        character = tool_input.get("character", "Luke Skywalker")
        result = get_star_wars_character(character)
        return json.dumps(result, ensure_ascii=False)
    
    else:
        return json.dumps({"error": f"Herramienta desconocida: {tool_name}"})


# ==================== FUNCIÓN PRINCIPAL ====================


def process_message(message: str, history: list) -> str:
    """
    Procesa un mensaje del usuario en el ChatInterface de Gradio
    y devuelve la respuesta del asistente
    """
    messages = [{"role": "user", "content": message}]
    
    # Primera llamada al modelo con herramientas disponibles
    response = client.chat(
        model="llama3.1",
        messages=messages,
        tools=tools,
        stream=False
    )
    
    # Verificar si el modelo quiere usar una herramienta
    if response.get("message", {}).get("tool_calls"):
        tool_calls = response["message"]["tool_calls"]
        
        # Procesar cada llamada a herramienta
        for tool_call in tool_calls:
            tool_name = tool_call["function"]["name"]
            tool_input = tool_call["function"]["arguments"]
            
            # Ejecutar la herramienta
            tool_result = process_tool_call(tool_name, tool_input)
            
            # Agregar el resultado del tool a los mensajes
            messages.append({"role": "assistant", "content": response["message"]["content"]})
            messages.append({
                "role": "tool",
                "content": tool_result
            })
        
        # Segunda llamada al modelo con el resultado de las herramientas
        final_response = client.chat(
            model="llama3.2",
            messages=messages,
            stream=False
        )
        
        assistant_message = final_response.get("message", {}).get("content", "")
        return assistant_message
    else:
        # El modelo respondió sin usar herramientas
        assistant_message = response.get("message", {}).get("content", "")
        return assistant_message


if __name__ == "__main__":
    # Crear la interfaz de Chat con Gradio
    demo = gr.ChatInterface(
        fn=process_message,
        examples=[
            "¿Qué hora es ahora mismo?",
            "Cuéntame un chiste de Chuck Norris",
            "Dame información detallada sobre Luke Skywalker",
            "¿Cuál es la hora actual? Chiste de Chuck y datos de Luke Skywalker"
        ],
        title="🤖 Ollama Assistant con Tools",
        description="""
        Asistente alimentado por Ollama con acceso a 3 herramientas:
        - ⏰ **Hora actual** del sistema
        - 😄 **Chistes de Chuck Norris** (API externa)
        - ⭐ **Información de Star Wars** (SWAPI)
        
        Prueba escribiendo una pregunta y el asistente decidirá qué herramientas usar.
        """
    )
    
    # Lanzar la interfaz
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
