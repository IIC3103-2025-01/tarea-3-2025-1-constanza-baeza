import os
import requests

LLM_URL = os.getenv("ASTEROIDE_LLM_URL", "https://asteroide.ing.uc.cl/v1/chat/completions")
MODELO_LLM = "integracion"

def preguntar_al_llm(fragmentos: list[str], pregunta: str) -> str:
    contexto = "\n\n".join(fragmentos)

    body = {
        "model": MODELO_LLM,
        "messages": [
            {"role": "system", "content": "Responde preguntas basadas en el siguiente contexto:\n\n" + contexto},
            {"role": "user", "content": pregunta}
        ],
        "temperature": 0.7,
        "top_k": 18,
        "num_ctx": 512
        #   "temperature": 6,        # ✅ corregido
        # "top_k": 18,
        # "num_ctx": 512,
        # "repeat_last_n": 10      # ✅ agrégalo si no lo tenías
    }

    try:
        resp = requests.post(LLM_URL, json=body, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except requests.exceptions.RequestException as e:
        print("❌ ERROR al llamar al LLM:")
        print("Status:", getattr(e.response, "status_code", "sin código"))
        print("Texto:", getattr(e.response, "text", "sin respuesta"))
        raise e  # Para que FastAPI devuelva 503 como corresponde
