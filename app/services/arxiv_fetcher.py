import arxiv
from datetime import datetime, timedelta, timezone

client = arxiv.Client()

def buscar_artigos(tema: str, categoria: str = None, dias: int = 30, max_resultados: int = 10):
    query = tema
    if categoria:
        query += f" AND cat:{categoria}"

    busca = arxiv.Search(
        query=query,
        max_results=max_resultados,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    data_limite = datetime.now(timezone.utc) - timedelta(days=dias)
    artigos = []

    for resultado in client.results(busca):
        publicado = resultado.published
        if publicado.tzinfo is None:
            publicado = publicado.replace(tzinfo=timezone.utc)
        if publicado >= data_limite:
            artigos.append({
                "titulo": resultado.title,
                "autores": [a.name for a in resultado.authors],
                "resumo": resultado.summary,
                "data": str(resultado.published.date()),
                "pdf": resultado.pdf_url
            })

    return artigos
