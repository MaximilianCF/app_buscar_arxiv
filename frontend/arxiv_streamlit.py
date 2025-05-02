
import streamlit as st
import requests
from datetime import datetime

API_ARXIV = "https://webapparxiv.onrender.com/api/arxiv/buscar"
API_IA = "https://webapparxiv.onrender.com/api/ia/resumir"

st.set_page_config(page_title="ArXiv com IA", layout="wide")
st.title("📚 ArXiv + IA WebApp")

@st.cache_data(ttl=3600)
def get_usd_to_brl():
    try:
        resp = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL")
        if resp.status_code == 200:
            return float(resp.json()["USDBRL"]["bid"])
    except:
        pass
    return 5.50

if "resultados" not in st.session_state:
    st.session_state.resultados = []
if "resumos" not in st.session_state:
    st.session_state.resumos = {}

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
        st.session_state.resultados = data["dados"]
        st.session_state.resumos = {}
    else:
        st.warning("⚠️ Nenhum artigo encontrado.")
        st.session_state.resultados = []

for i, artigo in enumerate(st.session_state.resultados):
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
                st.session_state.resumos[i] = resumo

        if i in st.session_state.resumos:
            resumo = st.session_state.resumos[i]
            cotacao = get_usd_to_brl()
            usd = resumo['usd']
            brl = usd * cotacao
            tokens = resumo['tokens']

            st.markdown(
                f'''
                <div style='background-color:#0e1117;padding:10px;border-radius:8px;color:#eee'>
                    <b>Tokens usados:</b> {tokens}<br>
                    <b>Custo (USD):</b> ${usd:.6f}<br>
                    <b>Custo estimado (BRL):</b> R${brl:.4f}<br>
                    <span style="font-size:0.8em; color:#bbb">
                    Cotação usada: 1 USD ≈ R${cotacao:.2f} (AwesomeAPI)
                    </span>
                </div>
                ''',
                unsafe_allow_html=True
            )
