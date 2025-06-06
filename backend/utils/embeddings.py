import os
import requests
import math

EMBED_URL  = os.getenv("ASTEROIDE_EMBED_URL", "https://asteroide.ing.uc.cl/api/embed")
MODEL_NAME = "nomic-embed-text"

def obtener_embedding(texto: str) -> list[float]:
    payload = {
        "model": MODEL_NAME,
        "input": texto
    }
    resp = requests.post(EMBED_URL, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["embeddings"][0]

def normalizar_vector(v: list[float]) -> list[float]:
    norm = math.sqrt(sum(x*x for x in v))
    return [x / norm for x in v] if norm else v

if __name__ == "__main__":
    texto = "Alan Turing was a British mathematician and computer scientist."

    try:
        emb = obtener_embedding(texto)
        print("Embedding generado. Dimensión:", len(emb))  # Debería ser 768
        print("Primeros 5 valores:", emb[:5])

        norm = normalizar_vector(emb)
        norm_l2 = sum(x**2 for x in norm)**0.5
        print("Norma del vector normalizado:", norm_l2)  # Debería ser ~1.0

    except Exception as e:
        print("Error al generar o normalizar embedding:", e)


