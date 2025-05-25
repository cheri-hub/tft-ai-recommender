
# TFT4Caster 🎯

**TFT4Caster** é uma aplicação de inteligência artificial que prevê a chance de alcançar o Top4 no jogo **Teamfight Tactics (TFT)** com base na sua composição de campeões, traits e tiers.

> ⚙️ Ferramenta desenvolvida para ajudar jogadores a entenderem, analisarem e otimizarem suas composições rumo ao topo do ranking.

---

## 🚀 Funcionalidades

- 🔍 Previsão de chance de Top4 no TFT com base na sua composição.
- 🧠 Análise da composição:
  - Quantidade de campeões.
  - Tier médio.
  - Traits ativas e quase ativas.
- 📊 Visualização com gráficos da distribuição dos tiers.
- 📥 Pipeline completo de dados:
  - Coleta de dados via API da Riot.
  - Geração e processamento de datasets.
  - Treinamento de modelos de IA.
- 🌐 Interface interativa via **Streamlit**.

---

## 🛠️ Tecnologias utilizadas

- **Python 3**
- **Streamlit** (Interface)
- **Scikit-Learn** (Machine Learning)
- **Pandas** (Manipulação de Dados)
- **Matplotlib** (Gráficos)
- **Joblib** (Persistência de modelos)
- **Riot Games API** (Coleta de dados)
- **JSON, CSV, REST API**

---

## 📁 Estrutura do projeto

```
tft4caster/
│
├── api/                 # Scripts de coleta e processamento de dados da Riot API
├── dataset/             # Dados brutos e tratados
├── docs/                # Documentação e relatórios
├── interface/           # Interface Streamlit (app.py)
├── model/               # Treinamento do modelo (train_model.py)
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação do projeto
```

---

## ⚙️ Instalação e execução

### 🔥 Pré-requisitos

- Python 3.9 ou superior instalado.
- Pip instalado.
- (Opcional) Ambiente virtual recomendado.

### 📥 Instale as dependências:

```bash
pip install -r requirements.txt
```

### 🚀 Execute a interface:

```bash
cd interface
streamlit run app.py
```

### 🧠 Treine o modelo (se desejar):

```bash
cd model
python train_model.py
```

---

## 💻 Modo de uso

1. Abra o app no navegador (após rodar `streamlit run app.py`).
2. Monte sua composição selecionando campeões e estrelas.
3. Veja a análise:
   - Traits ativas.
   - Traits quase ativas.
   - Gráficos de tiers.
4. Clique em **"Prever Resultado"** para saber sua chance de Top4.
5. Ajuste sua comp com base nas sugestões e análises.

---

## ☁️ Deploy (opcional)

Para rodar na nuvem via **Streamlit Cloud**:

1. Suba este repositório no GitHub.
2. Acesse [streamlit.io](https://streamlit.io/) → *"Get Started"* → *"Deploy an app"*.
3. Escolha seu repositório.
4. Configure o comando de execução:

```bash
cd interface
streamlit run app.py
```

5. ✅ Done! Seu app estará online.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Fique livre para abrir issues, sugerir melhorias ou enviar pull requests.

---

## 📝 Licença

Este projeto é livre para uso pessoal e educacional. Para uso comercial, consulte os desenvolvedores.

---

## 📫 Contato

- Desenvolvido por Luis Enrique Montagner
