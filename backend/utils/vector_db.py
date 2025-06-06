import faiss
import numpy as np

class DBVectorialFAISS:
    def __init__(self, dim: int = 768):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self.textos = []

    def agregar(self, embeds: np.ndarray, textos: list[str]):
        if embeds.size == 0:
            return

        if embeds.ndim == 1:
            embeds = embeds.reshape(1, -1)

        n, d = embeds.shape
        if d != self.dim:
            return

        self.index.add(embeds.astype("float32"))
        self.textos.extend(textos)

    def buscar_similares(self, query_vectors: np.ndarray, top_k: int = 3) -> list[tuple[str, float]]:
        """
        Recibe:
          - query_vectors: un np.ndarray de forma (N_consultas, dim)
          - top_k: cuántos vecinos queremos por cada consulta

        Retorna una lista de tuplas (texto, score) para la primera consulta.
        (Asumimos que solo se pasa un vector, de forma (1, dim).)
        """

        D, I = self.index.search(query_vectors.astype("float32"), top_k)

        resultados: list[tuple[str, float]] = []
        for idx, score in zip(I[0], D[0]):
            if idx < len(self.textos):
                texto = self.textos[idx]
                resultados.append((texto, float(score)))
        return resultados
