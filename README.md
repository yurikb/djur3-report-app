# DJUR3 Report App ⚖️

App web para analisar planilhas do DJUR3 e gerar relatórios jurídicos.

## Funcionalidades

- Upload de planilha `.xlsx` exportada do DJUR3
- Campo para configurar **tom/objetivo** do relatório
- Gera relatório markdown com:
  - Dashboard geral (valores, UFs, cooperativas)
  - Distribuição por tipo de ação, relevância, fase processual
  - Casos com observações (ATP.Texto)
  - Top 10 prazos mais urgentes
- Download do relatório em Markdown

## Como rodar local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy no Streamlit Cloud (gratuito)

1. Crie um repositório no GitHub com os arquivos
2. Acesse https://share.streamlit.io
3. Conecte seu GitHub e selecione o repositório
4. Streamlit detecta `app.py` e `requirements.txt` automaticamente
5. Pronto! URL pública gerada.

## Estrutura

```
djur3-report-app/
├── app.py              # Interface web (Streamlit)
├── extractor.py        # Lógica de extração e geração
├── requirements.txt    # Dependências
└── README.md           # Este arquivo
```
