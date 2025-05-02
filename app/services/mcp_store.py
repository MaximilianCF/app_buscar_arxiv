import os
import json

CACHE_PATH = "app/cache/"
_cache = {}

# Garante que pasta existe
os.makedirs(CACHE_PATH, exist_ok=True)

def salvar_cache(cache_id: str, dados):
    _cache[cache_id] = dados
    with open(f"{CACHE_PATH}{cache_id}.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def verificar_cache(cache_id: str):
    if cache_id in _cache:
        return _cache[cache_id]
    
    caminho = f"{CACHE_PATH}{cache_id}.json"
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            _cache[cache_id] = json.load(f)
            return _cache[cache_id]
    
    return None
