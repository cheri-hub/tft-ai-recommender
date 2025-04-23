# tft-ai-recommender
# 🎯 Sistema de Recomendação de Composições no Teamfight Tactics com Inteligência Artificial

Este projeto propõe o desenvolvimento de um sistema inteligente de recomendação de composições em partidas de Teamfight Tactics (TFT), com base no estado atual do jogo e utilizando modelos de Machine Learning treinados com dados reais.

## 📌 Funcionalidades
- Coleta de dados da Riot API
- Pré-processamento e vetorização dos dados
- Treinamento de modelos de IA (KNN, Random Forest)
- Interface simples para input do jogador
- Recomendações de comps com base em partidas históricas

## 🗂 Estrutura do Projeto
- `api/` – scripts de coleta de dados da Riot API
- `dataset/` – base de dados bruta e tratada
- `model/` – código de treinamento e modelos treinados
- `interface/` – interface interativa do sistema (MVP em Streamlit)
- `docs/` – materiais de apoio para o TCC (metodologia, anexos etc.)

## ▶️ Como rodar
```bash
pip install -r requirements.txt
streamlit run interface/app.py
