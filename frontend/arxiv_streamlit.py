
import streamlit as st
import requests
from datetime import datetime

API_ARXIV = "http://webapparxiv.streamlit.app/api/arxiv/buscar"
API_IA = "http://webapparxiv.streamlit.app/api/ia/resumir"

st.set_page_config(page_title="ArXiv com IA", layout="wide")
st.title("📚 ArXiv + IA WebApp")

# Inputs
with st.form("form_busca"):
    col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
    with col1:
        termo = st.text_input("🔍 Termo de busca")
    with col2:
        dias = st.number_input("Últimos X dias", min_value=1, value=30)
    with col3:
        max_artigos = st.number_input("Máx. artigos", min_value=1, value=5)
    with col4:
        categoria = st.selectbox("Categoria arXiv", ["cs.AI", "cs.LG", "stat.ML", "econ.EM", "q-fin.MF", "math.ST"])
    submitted = st.form_submit_button("Buscar Artigos")

# IA settings
api_key = st.text_input("🔑 API Key OpenAI", type="password")
modelo = st.selectbox("Modelo IA", ["gpt-3.5-turbo", "gpt-4"], index=0)
max_tokens = st.slider("Tokens para resumo", min_value=100, max_value=2048, value=600)

if submitted:
    payload = {
        "tema": termo,
        "dias": int(dias),
        "max_resultados": int(max_artigos),
        "categoria": categoria
    }
    with st.spinner("🔄 Buscando artigos..."):
        try:
            resp = requests.post(API_ARXIV, json=payload)
            data = resp.json()
        except:
            st.error("Erro ao consultar API.")
            st.stop()

    if data["dados"]:
        st.success(f"✅ {len(data['dados'])} artigos encontrados ({data['origem']})")
        for i, artigo in enumerate(data["dados"]):
            with st.expander(f"📄 {artigo['titulo']}", expanded=False):
                st.markdown(f"**Autores**: {', '.join(artigo['autores'])}")
                st.markdown(f"**Publicado em**: {artigo['data']}")
                st.markdown(f"[🔗 PDF Oficial]({artigo['pdf']})")
                st.markdown("**Resumo Original:**")
                st.code(artigo["resumo"][:500] + "...", language="markdown")

                if st.button(f"🤖 Resumir com IA", key=f"res_{i}"):
                    with st.spinner("Gerando resumo..."):
                        r = requests.post(API_IA, json={
                            "texto": artigo["resumo"],
                            "fonte": "openai",
                            "modelo": modelo,
                            "api_key": api_key,
                            "max_tokens": max_tokens
                        })
                        resumo = r.json()
                        st.markdown(f"**Resumo IA:**")
                        st.success(resumo["resumo_gerado"])
                        st.info(f"📊 {resumo['tokens']} tokens | 💵 ${resumo['usd']} ≈ R${resumo['brl']}")
    else:
        st.warning("⚠️ Nenhum artigo encontrado.")
