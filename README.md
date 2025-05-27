
# TFT4Caster 🎯

**TFT4Caster** é uma aplicação de inteligência artificial que prevê sua chance de alcançar o **Top 4 no Teamfight Tactics (TFT)** com base na sua composição de campeões, traits e tiers.

> ⚙️ Este projeto **não inclui dataset nem modelo treinado**. O pipeline completo — desde a coleta de dados via API da Riot até o treinamento do modelo — está incluso para que você mesmo gere e atualize seu modelo localmente.

---

## 🚀 Funcionalidades

- 🔍 **Previsão da chance de Top 4** no TFT com base na sua composição.
- 🧠 **Análise da composição:**
  - Quantidade de campeões.
  - Tier médio.
  - Traits ativas e quase ativas.
- 📊 **Visualização com gráficos** da distribuição dos tiers.
- 📥 **Pipeline completo:**
  - Coleta de dados via **Riot API**.
  - Processamento dos dados brutos.
  - Geração do dataset.
  - Treinamento do modelo de machine learning.
- 🌐 Interface interativa em **Streamlit**.

---

## 🛠️ Tecnologias utilizadas

- **Python 3.9+**
- **Streamlit** (Interface)
- **Scikit-Learn** (Machine Learning)
- **Pandas** (Manipulação de Dados)
- **Matplotlib** (Gráficos)
- **Joblib** (Persistência de modelos)
- **Riot Games API** (Coleta de dados)
- **dotenv** (Gestão de variáveis sensíveis)
- **JSON, CSV, REST API**

---

## 📁 Estrutura do projeto

```
tft4caster/
│
├── api/                 # Scripts para coletar dados da API da Riot
├── dataset/             # Dados brutos e processados (gerados localmente)
├── docs/                # Documentação
├── interface/           # Interface do usuário (Streamlit)
├── model/               # Script para treinamento do modelo
├── requirements.txt     # Dependências
├── .env.example         # Exemplo do arquivo .env com chave da Riot
└── README.md            # Documentação do projeto
```

---

## 🔑 Configuração inicial

### 1️⃣ Obtenha uma chave da **Riot API**

- Acesse: https://developer.riotgames.com/
- Crie uma conta ou faça login.
- Gere sua chave de API.

### 2️⃣ Crie um arquivo `.env` na raiz do projeto:

```
RIOT_API_KEY=your_riot_api_key_here
```

> ⚠️ Sua chave da Riot tem validade limitada (para dev). Para usos prolongados, é necessário solicitar uma chave de produção.

---

## ⚙️ Instalação

### 🔥 Pré-requisitos

- Python 3.9+
- Pip instalado
- (Recomendado) Ambiente virtual

### 🏗️ Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 📥 Coletando dados

1. Vá até a pasta `/api/`:

```bash
cd api
```

2. Execute o script de coleta:

```bash
python coletar_tft_ranked_dataset.py
```

> 🔸 Este script irá:
> - Coletar dados de partidas ranked no TFT.
> - Gerar um arquivo JSON com dados brutos em `/dataset/tft_raw_match_log.json`.

---

## 🔄 Processando dados

Ainda na pasta `/api/`, execute:

```bash
python json_to_csv.py
```

> 🔸 Isso irá transformar os dados brutos em um CSV estruturado no diretório `/dataset/`.

---

## 🧠 Treinando o modelo

1. Vá para a pasta `/model/`:

```bash
cd model
```

2. Execute o treinamento:

```bash
python train_model.py
```

> 🔸 O modelo treinado será salvo na pasta `/model/` como `random_forest_tft.pkl`.

---

## 🚀 Executando a interface

1. Vá até a pasta `/interface/`:

```bash
cd interface
```

2. Execute a interface Streamlit:

```bash
streamlit run app.py
```

3. Acesse o link fornecido (geralmente `http://localhost:8501`) no navegador.

---

## 💻 Fluxo de uso

1. Monte sua composição selecionando campeões e níveis de estrela.
2. Veja a análise:
   - Traits ativas.
   - Traits quase ativas.
   - Gráfico da distribuição dos tiers.
3. Clique em **"Prever Resultado"** para calcular a chance de Top 4.
4. Ajuste sua composição com base nas análises.

---

## ☁️ Deploy (opcional)

### ✔️ Deploy na Streamlit Cloud:

1. Suba seu repositório no GitHub.
2. Acesse https://streamlit.io/ → *"Get Started"* → *"Deploy an app"*.
3. Configure o comando de execução:

```bash
cd interface
streamlit run app.py
```

4. ✅ Seu app estará online!

---

## 🧽 Manutenção e melhorias

- 🔄 Você pode rodar novamente a coleta de dados e o treinamento para atualizar o modelo com dados mais recentes.
- 🧠 Avalie melhorias no modelo ou na interface.

---

## 📝 Licença

Este projeto é livre para uso pessoal e educacional.  
Para uso comercial, consulte os desenvolvedores.

---

## 📫 Contato

- Desenvolvido por Luis Enrique Montagner
