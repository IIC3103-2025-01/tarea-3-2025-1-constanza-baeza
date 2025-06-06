# backend/test_llm.py

from utils.llm_client import preguntar_al_llm

if __name__ == "__main__":
    fragmentos = [
        "Alan Turing fue un matemático británico considerado uno de los padres de la computación.",
        "Trabajó en la ruptura de códigos durante la Segunda Guerra Mundial, especialmente con la máquina Enigma."
    ]

    pregunta = "¿Quién fue Alan Turing y por qué es importante?"

    try:
        respuesta = preguntar_al_llm(fragmentos, pregunta)
        print("\n--- Respuesta del LLM ---")
        print(respuesta)
    except Exception as e:
        print("Error al consultar al LLM:", e)
