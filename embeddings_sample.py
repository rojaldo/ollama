import ollama
import numpy as np
from typing import Dict, List, Tuple

# Cliente de Ollama
client = ollama.Client(host='http://localhost:11434')

def obtener_embedding(palabra: str, modelo: str = "nomic-embed-text") -> np.ndarray:
    """
    Obtiene el embedding de una palabra usando Ollama.
    
    Args:
        palabra: La palabra para la que se obtiene el embedding
        modelo: El modelo a usar (por defecto: nomic-embed-text)
    
    Returns:
        Vector numpy con el embedding
    """
    try:
        response = client.embeddings(model=modelo, prompt=palabra)
        return np.array(response["embedding"])
    except Exception as e:
        print(f"Error al obtener embedding para '{palabra}': {e}")
        return None

def calcular_similitud(v1: np.ndarray, v2: np.ndarray) -> float:
    """
    Calcula la similitud del coseno entre dos vectores.
    La similitud del coseno mide el ángulo entre dos vectores.
    
    Args:
        v1: Primer vector
        v2: Segundo vector
    
    Returns:
        Similitud entre -1 y 1 (1 = idénticos)
    """
    if v1 is None or v2 is None:
        return None
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def normalizar_vector(v: np.ndarray) -> np.ndarray:
    """
    Normaliza un vector a magnitud 1.
    
    Args:
        v: Vector a normalizar
    
    Returns:
        Vector normalizado
    """
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def operacion_analogica(palabra_base: str, restar: List[str], sumar: List[str], 
                       modelo: str = "nomic-embed-text") -> Dict:
    """
    Realiza la operación analógica: base - restar + sumar
    Útil para encontrar: rey - hombre + mujer ≈ reina
    
    Args:
        palabra_base: Palabra base (ej: "reina")
        restar: Lista de palabras a restar (ej: ["mujer"])
        sumar: Lista de palabras a sumar (ej: ["hombre"])
        modelo: Modelo de embeddings a usar
    
    Returns:
        Diccionario con el resultado y detalles de la operación
    """
    
    print(f"\n{'='*60}")
    print(f"Operación Analógica de Embeddings")
    print(f"{'='*60}")
    print(f"Base: {palabra_base}")
    print(f"Restar: {restar}")
    print(f"Sumar: {sumar}")
    print(f"{'='*60}\n")
    
    # Obtener el vector base
    print(f"1. Obteniendo embedding de '{palabra_base}'...")
    v_base = obtener_embedding(palabra_base, modelo)
    if v_base is None:
        return None
    print(f"   ✓ Vector obtenido (dimensión: {len(v_base)})")
    
    # Restar vectores
    v_resultado = v_base.copy()
    print(f"\n2. Restando vectores...")
    for palabra in restar:
        print(f"   - Obteniendo embedding de '{palabra}'...")
        v = obtener_embedding(palabra, modelo)
        if v is not None:
            v_resultado -= v
            print(f"     ✓ '{palabra}' restado")
        else:
            print(f"     ✗ Error al obtener '{palabra}'")
    
    # Sumar vectores
    print(f"\n3. Sumando vectores...")
    for palabra in sumar:
        print(f"   - Obteniendo embedding de '{palabra}'...")
        v = obtener_embedding(palabra, modelo)
        if v is not None:
            v_resultado += v
            print(f"     ✓ '{palabra}' sumado")
        else:
            print(f"     ✗ Error al obtener '{palabra}'")
    
    # Normalizar el resultado
    v_resultado_norm = normalizar_vector(v_resultado)
    
    print(f"\n4. Resultado de la operación:")
    print(f"   Vector resultado (sin normalizar): magnitud = {np.linalg.norm(v_resultado):.4f}")
    print(f"   Vector resultado (normalizado): magnitud = {np.linalg.norm(v_resultado_norm):.4f}")
    
    return {
        "vector": v_resultado,
        "vector_normalizado": v_resultado_norm,
        "operacion": f"{palabra_base} - {' - '.join(restar)} + {' + '.join(sumar)}"
    }

def buscar_palabra_mas_cercana(v_target: np.ndarray, palabras_candidatas: List[str], 
                               modelo: str = "nomic-embed-text", top_k: int = 5) -> List[Tuple[str, float]]:
    """
    Encuentra las palabras más cercanas a un vector objetivo.
    
    Args:
        v_target: Vector objetivo
        palabras_candidatas: Lista de palabras candidatas para comparar
        modelo: Modelo de embeddings a usar
        top_k: Número de resultados principales a retornar
    
    Returns:
        Lista de tuplas (palabra, similitud) ordenadas por similitud descendente
    """
    
    resultados = []
    
    print(f"\n5. Buscando palabras más cercanas al resultado...")
    print(f"   Comparando con {len(palabras_candidatas)} candidatos...\n")
    
    for palabra in palabras_candidatas:
        v = obtener_embedding(palabra, modelo)
        if v is not None:
            sim = calcular_similitud(v_target, v)
            resultados.append((palabra, sim))
    
    # Ordenar por similitud descendente
    resultados.sort(key=lambda x: x[1], reverse=True)
    
    # Retornar top k
    top_resultados = resultados[:top_k]
    
    print(f"   Top {top_k} palabras más cercanas:")
    for i, (palabra, sim) in enumerate(top_resultados, 1):
        barra = "█" * int(sim * 50)
        print(f"   {i}. {palabra:15} | {sim:.4f} | {barra}")
    
    return top_resultados

def experimento_reina_rey():
    """
    Experimento clásico: reina - mujer + hombre ≈ rey
    
    Este es un ejemplo clásico en procesamiento de lenguaje natural que demuestra
    que los embeddings capturan relaciones semánticas.
    """
    
    print("\n" + "="*60)
    print("EXPERIMENTO CLÁSICO: Analogías de Embeddings")
    print("="*60)
    
    # Realizar la operación analógica
    resultado = operacion_analogica(
        palabra_base="reina",
        restar=["mujer"],
        sumar=["hombre"],
        modelo="nomic-embed-text"
    )
    
    if resultado is not None:
        # Buscar las palabras más cercanas
        palabras_candidatas = [
            "rey", "reina", "príncipe", "princesa",
            "hombre", "mujer", "corona", "trono",
            "monarca", "regal", "nobleza", "poder"
        ]
        
        resultados = buscar_palabra_mas_cercana(
            resultado["vector_normalizado"],
            palabras_candidatas,
            top_k=10
        )
        
        # Análisis específico
        print(f"\n{'='*60}")
        print("ANÁLISIS DEL RESULTADO")
        print(f"{'='*60}")
        
        # Encontrar similitud con "rey"
        v_rey = obtener_embedding("rey", "nomic-embed-text")
        if v_rey is not None:
            sim_rey = calcular_similitud(resultado["vector_normalizado"], v_rey)
            print(f"\n✓ Similaridad con 'rey': {sim_rey:.4f} (en escala 0-1)")
            print(f"  Interpretación: ", end="")
            
            if sim_rey > 0.8:
                print("¡Muy similar! El resultado es muy cercano a 'rey'")
            elif sim_rey > 0.6:
                print("Bastante similar. El vector está en la dirección correcta.")
            elif sim_rey > 0.4:
                print("Moderadamente similar. Hay cierta relación.")
            else:
                print("Poco similar. El resultado no es muy cercano a 'rey'.")
        
        return resultado, resultados
    
    return None, None

def mostrar_vectores_individuales(palabras: List[str]):
    """
    Muestra información sobre los vectores individuales de un conjunto de palabras.
    
    Args:
        palabras: Lista de palabras a analizar
    """
    
    print(f"\n{'='*60}")
    print("ANÁLISIS DE VECTORES INDIVIDUALES")
    print(f"{'='*60}\n")
    
    vectores = {}
    for palabra in palabras:
        v = obtener_embedding(palabra, "nomic-embed-text")
        if v is not None:
            vectores[palabra] = v
            print(f"'{palabra}':")
            print(f"  - Dimensión: {len(v)}")
            print(f"  - Magnitud: {np.linalg.norm(v):.4f}")
            print(f"  - Primeros 5 componentes: {v[:5]}")
            print()
    
    # Matriz de similitudes
    if len(vectores) > 1:
        print(f"MATRIZ DE SIMILITUDES ENTRE PALABRAS:\n")
        palabras_list = list(vectores.keys())
        
        # Encabezado
        print(f"{'':15}", end="")
        for p in palabras_list:
            print(f"{p:12}", end="")
        print()
        print("-" * (15 + 12 * len(palabras_list)))
        
        # Filas
        for p1 in palabras_list:
            print(f"{p1:15}", end="")
            for p2 in palabras_list:
                sim = calcular_similitud(vectores[p1], vectores[p2])
                print(f"{sim:12.4f}", end="")
            print()

if __name__ == "__main__":
    # Ejecutar el experimento principal
    resultado, top_palabras = experimento_reina_rey()

    # Mostrar resultado

    print("RESULTADO FINAL DEL EXPERIMENTO")
    print(f"{'='*60}\n")
    if resultado is not None:
        print(f"Operación realizada: {resultado['operacion']}")
        print(f"Vector resultado (primeros 5 componentes): {resultado['vector'][:5]}")
        print(f"Vector resultado normalizado (primeros 5 componentes): {resultado['vector_normalizado'][:5]}")
        print(f"\nTop palabras más cercanas al resultado:")
        for palabra, similitud in top_palabras:
            print(f" - {palabra}: similitud = {similitud:.4f}")
    else:
        print("No se pudo realizar el experimento debido a errores en la obtención de embeddings.")
    
    # Mostrar vectores individuales para referencia
    mostrar_vectores_individuales(["rey", "reina", "hombre", "mujer"])

    