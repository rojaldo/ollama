from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

llm = OllamaLLM(model="llama3.2")


# Estructura: mensaje del sistema + pregunta del usuario
chat = ChatPromptTemplate.from_messages([
    ("system", "Eres experto en {tema}. Sé muy técnico."),
    ("human", "¿Qué es {concepto}?"),
])

chain = chat | llm | StrOutputParser()

# El modelo recibe instrucciones claras
respuesta = chain.invoke({
    "tema": "programación",
    "concepto": "una función"
})
print(respuesta)

respuesta = chain.invoke({
    "tema": "física cuántica",
    "concepto": "el entrelazamiento cuántico"
})
print(respuesta)