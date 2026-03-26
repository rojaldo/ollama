from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
import numpy as np

embeddings = OllamaEmbeddings(model="nomic-embed-text")

documentos = [
    Document(
        page_content="Las redes neuronales son modelos de aprendizaje machine inspirados en el cerebro humano.",
        metadata={"area": "ML", "anio": 2024}
    ),
    Document(
        page_content="Deep Learning utiliza múltiples capas para procesar información jerárquica.",
        metadata={"area": "DL", "anio": 2024}
    ),
    Document(
        page_content="Los transformers revolucionaron el procesamiento natural del lenguaje.",
        metadata={"area": "NLP", "anio": 2024}
    )
]

vector_store = FAISS.from_documents(
    documents=documentos,
    embedding=embeddings
)

vector_store.save_local("./faiss_index")

consulta = "¿Cómo funcionan los modelos de aprendizaje profundo?"
print(f"Consulta: {consulta}\n")

vector_consulta = embeddings.embed_query(consulta)
docs_recuperados = vector_store.similarity_search_with_score(consulta, k=3)

print(f"{'#':<3} {'Puntuación':<12} {'Contenido':<50} {'Área':<10}")
print("-" * 80)

for i, (doc, puntuacion) in enumerate(docs_recuperados, 1):
    contenido = (doc.page_content[:47] + "...") if len(doc.page_content) > 50 else doc.page_content
    area = doc.metadata.get("area", "N/A")
    print(f"{i:<3} {puntuacion:<12.4f} {contenido:<50} {area:<10}")

print("\n=== Análisis de distancia L2 ===\n")

for i, (doc, puntuacion) in enumerate(docs_recuperados, 1):
    vector_doc = embeddings.embed_query(doc.page_content)
    distancia_l2 = np.linalg.norm(np.array(vector_consulta) - np.array(vector_doc))
    print(f"Doc {i}: Distancia L2 = {distancia_l2:.4f}, Puntuación FAISS = {puntuacion:.4f}")