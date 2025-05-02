from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import arxiv
from app.routes import ia


app = FastAPI(title="ArXiv WebApp API", version="0.1")

# CORS para permitir acesso da interface (Flet ou browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção: restringir por domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas específicas do módulo Arxiv
app.include_router(arxiv.router, prefix="/api/arxiv", tags=["arxiv"])

# Rotas específicas do módulo IA
app.include_router(ia.router, prefix="/api/ia", tags=["ia"])


@app.get("/")
def root():
    return {"msg": "API do ArXiv WebApp Online!"}
