import re

from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


def estimate_token_count(text):
    return len(re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE))


def chunk_text_by_tokens(text, max_tokens=500):
    words = text.split()
    chunks = []
    current_words = []

    for word in words:
        candidate_words = current_words + [word]
        candidate_text = " ".join(candidate_words)

        token_count = estimate_token_count(candidate_text)

        if token_count <= max_tokens:
            current_words = candidate_words
            continue

        if current_words:
            chunks.append(" ".join(current_words))
            current_words = [word]
        else:
            chunks.append(candidate_text)
            current_words = []

    if current_words:
        chunks.append(" ".join(current_words))

    return chunks

loader = PyPDFLoader("./data/BOE-A-2010-8067.pdf")
paginas = loader.load()

primeras_2 = paginas[:2]
paginas_importantes = [p for p in paginas if "configuración" in p.page_content.lower()]

llm = OllamaLLM(model="llama3.2", temperature=0.3)
chunks_por_pagina = [
    chunk_text_by_tokens(pagina.page_content, max_tokens=500)
    for pagina in primeras_2
]

contexto = "\n\n".join(
    f"Pagina {indice_pagina} - Chunk {indice_chunk}:\n{chunk}"
    for indice_pagina, chunks in enumerate(chunks_por_pagina, start=1)
    for indice_chunk, chunk in enumerate(chunks, start=1)
)

prompt = ChatPromptTemplate.from_template(
    "Contexto:\n{contexto}\n\nPregunta: {pregunta}"
)
cadena = prompt | llm

respuesta = cadena.invoke({"contexto": contexto, "pregunta": "¿cuando se publicó El Real Decreto 1538/2006?"})
print(respuesta)