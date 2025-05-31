# TFT4Caster

Sistema inteligente para previsão de Top 4 no Teamfight Tactics (TFT).

---

## 🎓 Tecnologias Utilizadas

* Python 3.10+
* pandas
* scikit-learn
* Streamlit
* matplotlib
* seaborn
* requests
* joblib
* tqdm
* pyperclip

---

## 🚫 Requisitos

* Ter o Python instalado
* Criar e ativar um ambiente virtual (recomendado)

### 🔹 Criar ambiente virtual:

```bash
python -m venv venv
```

### 🔹 Ativar o ambiente virtual:

* **Windows:**

```bash
venv\Scripts\activate
```

* **Mac/Linux:**

```bash
source venv/bin/activate
```

### 🔹 Instalar dependências:

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuração da API da Riot

Crie um arquivo `.env` na raiz do projeto com a seguinte variável:

```env
RIOT_API_KEY=sua_chave_api_aqui
```

Consiga sua chave gratuita em: [https://developer.riotgames.com/](https://developer.riotgames.com/)

---

## 💡 Passo a Passo para Executar o Projeto

### 1. Coletar dados da API da Riot

```bash
python api/coletartft.py
```

### 2. Processar e limpar os dados

```bash
python helper/parser.py
```

### 3. Validar os dados

```bash
python helper/validate_dataset.py
```

### 4. Treinar o modelo de machine learning

```bash
python model/train_model.py
```

### 5. Iniciar a aplicação Streamlit

```bash
streamlit run app.py
```

---

## 🌐 Funcionalidades

* Prever chance de Top 4 com base na composição montada manualmente
* Exibir sinergias (traits) ativas
* Mostrar custo total e quantidade de campeões
* Visualização com ícones e estatísticas

---

## 📁 Estrutura do Projeto

```
tft-ai-recommender/
├── api/
│   └── coletartft.py
├── helper/
│   ├── parser.py
│   ├── validate_dataset.py
│   └── arquivos auxiliares (.json)
├── model/
│   └── train_model.py
│   └── random_forest_tft.pkl (gerado)
├── dataset/
│   └── dataset.csv (gerado)
├── app.py
├── requirements.txt
└── .env
```

---

## 🚀 Futuras melhorias

* Sugestão automática de composições
* Reforço visual com badges, gráficos e ícones
* Integração com banco de dados e cache
* Versão web hospedada (Streamlit Cloud ou HuggingFace)

---

## 👤 Autor

**TFT4Caster** - projeto de IA aplicada ao game design por \[Luis Montagner]
