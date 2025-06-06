from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import requests
import time  

from fastapi.middleware.cors import CORSMiddleware

from utils.scraper import obtener_texto_articulo
from utils.splitter import fragmentar_texto
from utils.embeddings import obtener_embedding, normalizar_vector
from utils.vector_db import DBVectorialFAISS
from utils.llm_client import preguntar_al_llm

app = FastAPI()

# Ruta raíz para evitar error 404 en Render
@app.get("/")
def read_root():
    return {"mensaje": "Wikipedia Chatbot activo"}

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = DBVectorialFAISS(dim=768)

class IndexarRequest(BaseModel):
    url: str

class PreguntarRequest(BaseModel):
    pregunta: str

@app.post("/indexar")
async def indexar(req: IndexarRequest):
    try:
        texto = obtener_texto_articulo(req.url)
    except ValueError:
        return {"fragmentos_indexados": 0}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    fragments = fragmentar_texto(texto)
    vecs = []
    textos_ok = []

    for f in fragments:
        try:
            emb = obtener_embedding(f)
            time.sleep(1)  # Para evitar rate limit
        except Exception:
            continue
        vecs.append(normalizar_vector(emb))
        textos_ok.append(f)

    if not vecs:
        return {"fragmentos_indexados": 0}

    arr = np.array(vecs, dtype="float32")
    db.agregar(arr, textos_ok)
    return {"fragmentos_indexados": len(textos_ok)}

@app.post("/preguntar")
async def preguntar(req: PreguntarRequest):
    try:
        emb_q = normalizar_vector(obtener_embedding(req.pregunta))
    except Exception:
        raise HTTPException(status_code=503, detail="No se pudo vectorizar la pregunta.")

    query_arr = np.array([emb_q], dtype="float32")

    similares = db.buscar_similares(query_arr, top_k=3)
    textos = [texto for texto, _ in similares]
    print("Preguntando al LLM con contexto:", textos)
    time.sleep(0.1)

    if not textos:
        return {"respuesta": "", "contexto": []}

    try:
        respuesta = preguntar_al_llm(textos, req.pregunta)
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(
            status_code=503,
            detail=f"El servicio de LLM no está disponible: {http_err}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"respuesta": respuesta, "contexto": textos}
