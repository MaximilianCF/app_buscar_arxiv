
import streamlit as st
import requests
from datetime import datetime
from streamlit_extras.copy_to_clipboard import copy_to_clipboard_button
from streamlit_extras.badges import badge

API_ARXIV = "http://localhost:8000/api/arxiv/buscar"
API_IA = "http://localhost:8000/api/ia/resumir"

st.set_page_config(page_title="ArXiv Blaster Master", layout="wide")
st.title("🚀 ArXiv Blaster Master HAL-9000")

# Campos de entrada
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
    submitted = st.form_submit_button("📡 Buscar Artigos")

# Campos da IA
st.subheader("⚙️ Configurações da IA")
api_key = st.text_input("🔑 API Key OpenAI", type="password")
modelo = st.selectbox("🧠 Modelo IA", ["gpt-3.5-turbo", "gpt-4"])
max_tokens = st.slider("📝 Tokens para resumo", 100, 2048, 600)

if submitted:
    payload = {
        "tema": termo,
        "dias": int(dias),
        "max_resultados": int(max_artigos),
        "categoria": categoria
    }
    with st.spinner("🔄 Consultando ArXiv..."):
        try:
            r = requests.post(API_ARXIV, json=payload)
            data = r.json()
        except Exception as e:
            st.error(f"Erro ao buscar artigos: {e}")
            st.stop()

    if data["dados"]:
        st.success(f"✅ {len(data['dados'])} artigos encontrados ({data['origem']})")

        for i, artigo in enumerate(data["dados"]):
            with st.expander(f"📄 {artigo['titulo']}", expanded=False):
                st.markdown(f"**👥 Autores**: {', '.join(artigo['autores'])}")
                st.markdown(f"**📅 Publicado em**: {artigo['data']}")
                st.markdown(f"[🔗 PDF Oficial]({artigo['pdf']})")
                st.markdown("**🧠 Resumo Original:**")
                st.code(artigo["resumo"][:500] + "...", language="markdown")

                if st.button(f"🤖 Resumir com IA", key=f"resumir_{i}"):
                    with st.spinner("Gerando resumo IA..."):
                        r = requests.post(API_IA, json={
                            "texto": artigo["resumo"],
                            "fonte": "openai",
                            "modelo": modelo,
                            "api_key": api_key,
                            "max_tokens": max_tokens
                        })
                        resumo = r.json()
                        st.success("✅ Resumo gerado com sucesso!")
                        st.markdown("### ✂️ Resumo IA")
                        copy_to_clipboard_button(resumo["resumo_gerado"], "📋 Copiar Resumo IA")
                        st.code(resumo["resumo_gerado"], language="markdown")
                        badge(label=f"{resumo['tokens']} tokens", color="green")
                        badge(label=f"${resumo['usd']} USD", color="blue")
                        badge(label=f"R${resumo['brl']} BRL", color="violet")
    else:
        st.warning("⚠️ Nenhum artigo encontrado.")
