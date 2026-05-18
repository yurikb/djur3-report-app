import streamlit as st
from extractor import extrair, gerar_relatorio_template, gerar_relatorio_ia, limpar

st.set_page_config(
    page_title="DJUR3 - Relatório de Processos",
    page_icon="⚖️",
    layout="wide",
)

st.title("⚖️ DJUR3 - Extrator de Relatórios")
st.markdown("Faça upload da planilha exportada do **DJUR3** e gere relatórios analíticos.")

with st.sidebar:
    st.header("Configurações")

    modo = st.radio(
        "Modo de geração",
        ["📊 Relatório Estruturado (template)", "🤖 Relatório com IA (DeepSeek V4 Flash)"],
        index=0,
        help="Template usa dados extraídos direto. IA segue as instruções do agente jurídico + DeepSeek via OpenRouter.",
    )

    st.markdown("**Tom / Objetivo do Relatório**")
    prompt_extra = st.text_area(
        "Instruções adicionais",
        placeholder="Ex: Destacar que a condução técnica pelo escritório foi correta.\nOu: Minimizar um erro do escritório.\nOu: Foco em processos urgentes.",
        help="Este campo é usado tanto no template quanto enviado para a IA.",
    )

    if modo.startswith("🤖"):
        st.divider()
        st.markdown("**Configuração da IA**")
        with st.expander("API Key (opcional no deploy)", expanded=False):
            api_key = st.text_input("API Key (OpenRouter ou DeepSeek)", type="password", help="Deixe vazio pra usar a configurada como secret do servidor")
            if api_key:
                os.environ["AI_API_KEY"] = api_key
            api_url = st.text_input("API URL", value="https://openrouter.ai/api/v1/chat/completions")
            if api_url:
                os.environ["AI_API_URL"] = api_url
            model = st.text_input("Modelo", value="deepseek/deepseek-v4-flash")
            if model:
                os.environ["AI_MODEL"] = model

st.divider()

uploaded_file = st.file_uploader(
    "Selecione o arquivo .xlsx do DJUR3",
    type=["xlsx"],
    accept_multiple_files=False,
)

if uploaded_file:
    with st.spinner("Processando planilha..."):
        dados, headers = extrair(uploaded_file)

    st.success(f"✅ {len(dados)} processos processados com sucesso!")

    total_v = sum(float(d.get("PRO.Valor da causa", 0) or 0) for d in dados)
    ufs = set(str(d.get("UF", "") or "") for d in dados)
    tipos = set(str(d.get("Tipo de ação", "") or "") for d in dados)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Processos", len(dados))
    with col2:
        st.metric("Valor Total", f"R$ {total_v:,.2f}")
    with col3:
        st.metric("Estados", len(ufs))
    with col4:
        st.metric("Tipos de Ação", len(tipos))

    st.divider()

    if modo.startswith("🤖"):
        with st.spinner("Gerando relatório via IA (pode levar até 2 minutos)..."):
            relatorio, erro = gerar_relatorio_ia(dados, headers, prompt_extra)

        if erro:
            st.error(f"Erro ao gerar relatório via IA: {erro}")
            st.info("Gerando relatório estruturado como fallback...")
            relatorio, _ = gerar_relatorio_template(dados, headers, prompt_extra)
        else:
            st.success("Relatório gerado com IA!")
    else:
        relatorio, _ = gerar_relatorio_template(dados, headers, prompt_extra)

    st.subheader("📄 Relatório Gerado")
    with st.container():
        st.markdown(relatorio)

    st.download_button(
        label="📥 Baixar Relatório (.md)",
        data=relatorio,
        file_name="relatorio_djur3.md",
        mime="text/markdown",
        type="primary",
    )

    with st.expander("🔍 Dados Brutos (primeiras 20 linhas)"):
        st.dataframe(
            [
                {
                    "PJ": d.get("PJ"),
                    "Tipo": limpar(d.get("Tipo de ação", "")),
                    "UF": d.get("UF", ""),
                    "Fase": limpar(d.get("PRO.FAS.Descrição", "")),
                    "Valor": d.get("PRO.Valor da causa", 0),
                    "Relevância": limpar(d.get("Relevancia", "")),
                    "Processo": limpar(d.get("PRO.Número do processo", "")),
                }
                for d in dados[:20]
            ]
        )

else:
    st.info("👆 Faça upload de um arquivo .xlsx para começar.")

    st.divider()
    st.subheader("Como usar")
    st.markdown("""
    1. **Exporte** a planilha do DJUR3 (sheet: CPJ3C)
    2. **Faça upload** acima
    3. (Opcional) **Configure** o tom do relatório na sidebar
    4. Escolha **modo template** (rápido) ou **modo IA** (análise narrativa)
    5. **Baixe** o relatório em Markdown

    ### Modo IA
    Requer API key da DeepSeek (ou OpenAI-compatible).
    Configure como env vars no deploy ou digite na sidebar.
    """)

st.divider()
st.caption("Feito para Cintia 👩‍⚖️ — DJUR3 Report App v1.1")
