from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

# Herramientas más complejas
@tool
def generar_reporte(contenido: str) -> str:
    """Generar un reporte"""
    return f"Reporte generado: {contenido}"

@tool
def buscar_informacion(tema: str) -> str:
    """Buscar información sobre un tema"""
    return f"Información encontrada sobre {tema}: ..."

@tool
def analizar_datos(datos: str) -> str:
    """Analizar un conjunto de datos"""
    return f"Análisis completado: {datos}"



tools = [
    buscar_informacion,
    analizar_datos,
    generar_reporte,
]

# Crear agente con la API actual de LangChain
llm = ChatOllama(model="llama3.1")

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "Eres un asistente que resuelve tareas en varios pasos. "
        "Usa las herramientas disponibles cuando aporten valor y responde en espanol."
    )
)


def mostrar_traza(mensajes) -> None:
    print("\n--- Traza del agente ---")
    for indice, mensaje in enumerate(mensajes, start=1):
        tipo = getattr(mensaje, "type", type(mensaje).__name__)
        print(f"\nPaso {indice} [{tipo}]")

        contenido = getattr(mensaje, "content", "")
        if contenido:
            print(contenido)

        tool_calls = getattr(mensaje, "tool_calls", None)
        if tool_calls:
            print("Tool calls:")
            for tool_call in tool_calls:
                nombre = tool_call.get("name", "desconocida")
                argumentos = tool_call.get("args", {})
                print(f"- {nombre}: {argumentos}")

        nombre_herramienta = getattr(mensaje, "name", None)
        if nombre_herramienta:
            print(f"Herramienta: {nombre_herramienta}")


def ejecutar_tarea(agent_app, historial, tarea_usuario: str, mostrar_pasos: bool = False) -> str:
    cantidad_previa = len(historial)
    entrada = list(historial) + [{"role": "user", "content": tarea_usuario}]
    resultado = agent_app.invoke({"messages": entrada})
    mensajes = resultado["messages"]
    historial[:] = mensajes

    if mostrar_pasos:
        mostrar_traza(mensajes[cantidad_previa:])

    respuesta_final = mensajes[-1].content
    return respuesta_final

# Usar el agente en tareas complejas
task = "Necesito buscar información sobre machine learning, analizarla y generar un reporte ejecutivo"
chat_history = []
respuesta = ejecutar_tarea(agent, chat_history, task, mostrar_pasos=True)
print(f"\nRespuesta: {respuesta}")