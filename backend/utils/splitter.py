import re

def split_por_parrafos(texto: str) -> list[str]:
    return [p.strip() for p in texto.split("\n\n") if p.strip()]

def split_por_oraciones(parrafo: str, max_oraciones: int = 5) -> list[str]:
    oraciones = re.split(r'(?<=[\.\?\!])\s+', parrafo)
    return [
        " ".join(oraciones[i:i+max_oraciones]).strip()
        for i in range(0, len(oraciones), max_oraciones)
    ]

def fragmentar_texto(texto: str) -> list[str]:
    parrafos = split_por_parrafos(texto)
    fragments = []
    for p in parrafos:
        if len(p.split()) > 200:
            fragments.extend(split_por_oraciones(p))
        else:
            fragments.append(p)
    return fragments
