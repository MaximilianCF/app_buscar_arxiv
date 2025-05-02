# app/routes/ia.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.ia_engine import resumir_texto_ia

router = APIRouter()

class RequisicaoResumo(BaseModel):
    texto: str
    modelo: str
    api_key: str
    max_tokens: Optional[int] = 600
    fonte: str = "openai"

@router.post("/resumir")
def resumir(payload: RequisicaoResumo):
    resposta = resumir_texto_ia(
        texto=payload.texto,
        modelo=payload.modelo,
        api_key=payload.api_key,
        max_tokens=payload.max_tokens,
        fonte=payload.fonte
    )
    return resposta
