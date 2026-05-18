# DJUR3 Report App ⚖️

App web pra analisar planilhas do DJUR3 e gerar relatórios jurídicos.

## Funcionalidades
- Upload de `.xlsx` exportado do DJUR3 (sheet CPJ3C)
- Campo pra configurar **tom/objetivo** do relatório
- **2 modos de geração**:
  - 📊 **Template** — extrai dados e monta relatório estruturado (offline, instantâneo)
  - 🤖 **IA (DeepSeek V4 Flash)** — usa as instruções do **agente jurídico** como system prompt, via OpenRouter/DeepSeek
- Download do relatório em Markdown

## Modo IA
O relatório via IA segue **rigorosamente** as regras do agente em `juridic-report-extractor-xlsx.md`:
- NUNCA inventa dados
- Só usa o que está na planilha
- Corrobora com valores brutos
- Preserva números de processo

## Como rodar local

```bash
pip install -r requirements.txt

# Configurar API key pro modo IA
set OPENROUTER_API_KEY=sk-or-v1-...
# ou via .env

streamlit run app.py
```

## Deploy no Streamlit Cloud (grátis)

1. Crie repositório no GitHub
2. Acesse https://share.streamlit.io
3. "New app" → selecione o repo
4. Main file: `app.py`
5. Vá em Settings → Secrets e adicione:
   ```toml
   OPENROUTER_API_KEY = "sk-or-v1-..."
   ```

## Variáveis de Ambiente

| Variável | Obrigatória | Padrão | Descrição |
|----------|-------------|--------|-----------|
| `OPENROUTER_API_KEY` | Sim (modo IA) | - | Chave da OpenRouter |
| `AI_API_URL` | Não | `https://openrouter.ai/api/v1/chat/completions` | Endpoint OpenAI-compatível |
| `AI_MODEL` | Não | `deepseek/deepseek-v4-flash` | Modelo |