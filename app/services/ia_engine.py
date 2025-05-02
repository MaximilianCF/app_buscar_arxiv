# app/services/ia_engine.py
from openai import OpenAI

# instanciado dinamicamente dentro da função

def resumir_openai(texto: str, modelo: str, api_key: str, max_tokens: int):
    client = OpenAI(api_key=api_key)
    client.api_key = api_key
    resposta = client.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": texto}],
        max_tokens=max_tokens
    )
    resumo = resposta.choices[0].message.content
    tokens_usados = resposta.usage.total_tokens
    custo_usd = round((tokens_usados / 1000) * 0.0015, 6)  # estimativa p/ gpt-3.5-turbo
    try:
        import requests
        bcb = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL").json()
        brl = float(bcb["USDBRL"]["bid"])
    except:
        brl = 5.0  # fallback
    custo_brl = round(custo_usd * brl, 4)
    return {"resumo_gerado": resumo, "tokens": tokens_usados, "usd": custo_usd, "brl": custo_brl}

def resumir_texto_ia(texto: str, modelo: str, api_key: str, max_tokens: int, fonte: str):
    if fonte == "openai":
        return resumir_openai(texto, modelo, api_key, max_tokens)
    else:
        return {"resumo_gerado": "Fonte de IA não suportada.", "tokens": "?"}
