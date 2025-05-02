from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.arxiv_fetcher import buscar_artigos

router = APIRouter()

class BuscaRequest(BaseModel):
    tema: str
    categoria: Optional[str] = None
    dias: int = 30
    max_resultados: int = 10

@router.post("/buscar")
def buscar_artigos_api(payload: BuscaRequest):
    artigos = buscar_artigos(
        tema=payload.tema,
        categoria=payload.categoria,
        dias=payload.dias,
        max_resultados=payload.max_resultados
    )
    return {"origem": "arxiv", "dados": artigos}
