import time
import numpy as np
from utils.vector_db import DBVectorialFAISS
from utils.embeddings import obtener_embedding, normalizar_vector

if __name__ == "__main__":
    db = DBVectorialFAISS(dim=768)

    textos = [
        "Alan Turing was a pioneer in computer science.",
        "The capital of France is Paris.",
        "Python is a popular programming language."
    ]

    embeddings = []
    for texto in textos:
        try:
            emb = obtener_embedding(texto)
            time.sleep(0.3)  # ✅ Evita error 503
            embeddings.append(normalizar_vector(emb))
        except Exception as e:
            print(f"Error al obtener embedding para: {texto}\n{e}")

    arr = np.array(embeddings, dtype="float32")
    db.agregar(arr, textos)

    pregunta = "What did Alan Turing do?"
    try:
        emb_q = normalizar_vector(obtener_embedding(pregunta))
        query_arr = np.array([emb_q], dtype="float32")
        resultados = db.buscar_similares(query_arr, top_k=2)

        print("\n--- Resultados similares ---")
        for texto, score in resultados:
            print(f"Score: {score:.4f} | Texto: {texto}")
    except Exception as e:
        print("Error al hacer la consulta:", e)
