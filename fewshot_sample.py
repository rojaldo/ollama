from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_ollama import OllamaLLM

# 1. Definimos los ejemplos (Dataset miniatura)
ejemplos = [
    {"pregunta": "¿Cuál es la capital de España?", "respuesta": "Madrid. Contexto: Europa."},
    {"pregunta": "¿Cuál es la capital de Francia?", "respuesta": "París. Contexto: Europa."}
]

# 2. Formato para cada ejemplo (Cómo se presentarán los ejemplos anteriores)
formato_ejemplo = PromptTemplate(
    input_variables=["pregunta", "respuesta"],
    template="P: {pregunta}\nR: {respuesta}"
)

# 3. Construimos el prompt final integrando ejemplos, prefijo y sufijo
few_shot_prompt = FewShotPromptTemplate(
    examples=ejemplos,
    example_prompt=formato_ejemplo,
    prefix="Responde siguiendo el formato de ciudad seguido de su continente:",
    suffix="P: {input}\nR:", # El modelo completará a partir de aquí
    input_variables=["input"]
)

# Paso 1: Ver el prompt formateado con la consulta
prompt_formateado = few_shot_prompt.format(input="¿Cuál es la capital de Italia?")
print("=== Prompt con ejemplos (Few-Shot) ===")
print(prompt_formateado)

# Paso 2: Crear instancia del modelo Ollama
llm = OllamaLLM(model="llama3.2", temperature=0.7)

# Paso 3: Invocar el modelo directamente con el prompt
respuesta = llm.invoke(prompt_formateado)
print("\n=== Respuesta del modelo ===")
print(respuesta)

# Paso 4: Usar el prompt como parte de una chain (LCEL)
chain = few_shot_prompt | llm

# Realizar múltiples consultas con la cadena
consultas = [
    "¿Cuál es la capital de Alemania?",
    "¿Cuál es la capital de Japón?",
    "¿Cuál es la capital de Brasil?"
]

print("\n=== Múltiples consultas ===")
for consulta in consultas:
    respuesta = chain.invoke({"input": consulta})
    print(f"\nPregunta: {consulta}")
    print(f"Respuesta: {respuesta}")