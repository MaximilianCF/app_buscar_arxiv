<div align="left" style="position: relative;">
<h1>ArXiv WebAPP</h1>
<p align="left">
		<img src="https://img.shields.io/github/license/MaximilianCF/app_buscar_arxiv?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
		<img  src="https://img.shields.io/github/last-commit/MaximilianCF/app_buscar_arxiv?style=default&logo=git&logoColor=white&color=0080ff"  alt="last-commit">
		<img  src="https://img.shields.io/github/languages/top/MaximilianCF/app_buscar_arxiv?style=default&color=0080ff"  alt="repo-top-language">
		<img  src="https://img.shields.io/github/languages/count/MaximilianCF/app_buscar_arxiv?style=default&color=0080ff"  alt="repo-language-count">
</p>
</div>
<br  clear="right">

# 🔍 ArXiv WebApp – Explore artigos científicos e sumarize com IA

**O ArXiv WebApp permite que qualquer pessoa pesquise artigos no arXiv.org e receba resumos automáticos com inteligência artificial (IA).**

O app ainda permite que você escolha qual IA preferida (OpenAI ou HuggingFace) quer usar para elaborar os resumos.

🎯 Ideal para estudantes, pesquisadores, curiosos e desenvolvedores.

# 📚 Tabela de conteúdos

- [🔍 ArXiv WebApp – Explore artigos científicos e sumarize com IA](#-arxiv-webapp--explore-artigos-científicos-e-sumarize-com-ia)
- [📚 Tabela de conteúdos](#-tabela-de-conteúdos)
  - [🚀 Acesse agora:](#-acesse-agora)
  - [✨ O que este app faz?](#-o-que-este-app-faz)
  - [🧪 Exemplo de uso](#-exemplo-de-uso)
  - [🧠 Tecnologias usadas](#-tecnologias-usadas)
  - [⚙️ Para desenvolvedores](#️-para-desenvolvedores)
  - [🧱 Arquitetura](#-arquitetura)
  - [🗂️ Estrutura do Projeto](#️-estrutura-do-projeto)
  - [⚙️ Como usar](#️-como-usar)
    - [1. Clonar o repositório](#1-clonar-o-repositório)
    - [2. Backend (FastAPI)](#2-backend-fastapi)
    - [3. Frontend (Streamlit)](#3-frontend-streamlit)
  - [🌐 Deploy na nuvem](#-deploy-na-nuvem)
    - [Backend – Render](#backend--render)
    - [Frontend – Streamlit Cloud](#frontend--streamlit-cloud)
  - [🧪 Exemplos de uso](#-exemplos-de-uso)
  - [🔐 Secrets *(caso queira utilizar localmente)*](#-secrets-caso-queira-utilizar-localmente)
  - [🤝 Contribuindo](#-contribuindo)
  - [🧑‍💻 Autor](#-autor)


## 🚀 Acesse agora:

👉 [Clique aqui para usar o app](https://webapparxiv.streamlit.app)  
*(Roda diretamente no navegador – sem instalação)*

## ✨ O que este app faz?

1. Você digita um termo de busca (ex: `"transformer language model"`)
2. O sistema busca os artigos mais relevantes no [arXiv.org](https://arxiv.org)
3. Cada artigo vem com um **resumo automático** gerado com IA (via OpenAI GPT)
4. A interface é simples, rápida e 100% online

## 🧪 Exemplo de uso

Digite: `quantum computing`  
✅ Em segundos, você verá os títulos e resumos inteligentes dos principais artigos sobre o tema.

## 🧠 Tecnologias usadas

|Componente |Tecnologia              |
|-----------|------------------------|
|Interface  |Streamlit               |
|Backend API|FastAPI + Uvicorn       |
|IA         |OpenAI GPT (via API)    |
|Hospedagem |Streamlit Cloud + Render|

## ⚙️ Para desenvolvedores

Este projeto é modular e segue a arquitetura descrita abaixo.


## 🧱 Arquitetura

    [Usuário]  
    ↓  
    [Streamlit App - Frontend. Usuário edita os filtros]  
    ↓ --> chamada HTTP (requests)  
    [FastAPI Backend - Render]  
    ↓  
    [arXiv + OpenAI]


 ## 🗂️ Estrutura do Projeto

```bash
arxiv-app/
├── app/                      # Backend (FastAPI)
│   ├── routes/
│   │   ├── arxiv.py          # Busca artigos no arXiv
│   │   └── ia.py             # Resumo com IA
│   └── main.py               # Entrypoint da API
├── frontend/                 # Frontend (Streamlit)
│   └── arxiv_streamlit.py
├── requirements.txt          # Requisitos da API
├── render.yaml               # Configuração para deploy no Render
├── README.md
```


## ⚙️ Como usar

###  1. Clonar o repositório

    git  clone  https://github.com/seu-usuario/app_buscar_arxiv.git
    cd  app_buscar_arxiv

### 2. Backend (FastAPI)


    pip install -r requirements.txt
    uvicorn app.main:app --reload 

Endpoints disponíveis em:

`http://localhost:8000/api/arxiv/buscar`
    
`http://localhost:8000/api/ia/resumir`

### 3. Frontend (Streamlit)

    cd frontend/
    streamlit run arxiv_streamlit.py


## 🌐 Deploy na nuvem

### Backend – Render

-   Aponte para `main.py` com:
       
    `uvicorn app.main:app --host 0.0.0.0 --port 10000`
   
-   Adicione `OPENAI_API_KEY` como variável de ambiente
    

### Frontend – Streamlit Cloud

-   Use o arquivo `frontend/arxiv_streamlit.py`
    
-   Atualize os endpoints no código para usar o domínio Render da API:
    
    API_ARXIV = "https://arxiv-api.onrender.com/api/arxiv/buscar"
    API_IA = "https://arxiv-api.onrender.com/api/ia/resumir"

## 🧪 Exemplos de uso

-   Digite o termo “transformer language model”
    
-   A aplicação buscará os artigos no arXiv
    
-   E usará o GPT para resumi-los automaticamente
    
## 🔐 Secrets *(caso queira utilizar localmente)*

No Render:

`OPENAI_API_KEY` → sua chave da OpenAI
    

No Streamlit:

Use `st.secrets["OPENAI_API_KEY"]` ou crie`.streamlit/secrets.toml`
    

## 🤝 Contribuindo

Quer sugerir melhorias, adicionar novas fontes científicas ou integrar outras IAs?  
Pull requests e ideias são bem-vindos!

## 🧑‍💻 Autor

**Maximilian Canez Fernandes**  
CNPI-T, desenvolvedor e entusiasta de IA aplicada ao conhecimento técnico.

> “I'm sorry Dave, I can't summarize that... unless você me der permissão via JSON.” – HAL 9000






