
import streamlit as st
import pandas as pd
import joblib
import json

# Carregar modelo e dados auxiliares
model = joblib.load("model/random_forest_tft.pkl")
vetorizado_df = pd.read_csv("dataset/dataset_vetorizado.csv")
with open("data/campeao_traits.json", "r", encoding="utf-8") as f:
    campeao_traits = json.load(f)
with open("data/custo_por_campeao.json", "r", encoding="utf-8") as f:
    custo_por_campeao = json.load(f)
with open("data/depara_traits.json", "r", encoding="utf-8") as f:
    depara_traits = json.load(f)

# Preparar estrutura
feature_cols = [col for col in vetorizado_df.columns if col != "is_top4"]
lista_de_campeoes = sorted([col.replace("champ_", "").replace("TFT14_", "") for col in feature_cols if col.startswith("champ_")])

# Inicializar sessão
if "comp" not in st.session_state:
    st.session_state.comp = {}

# Interface
st.title("Recomendador TFT - Previsão de Top 4")
st.markdown("Monte sua composição abaixo selecionando campeões e suas estrelas. As sinergias e custo total serão calculadas automaticamente.")

# Seleção de campeão
col1, col2 = st.columns(2)
with col1:
    selected_champ = st.selectbox("Escolha um campeão", lista_de_campeoes)
with col2:
    estrela = st.selectbox("Nível de estrela", [1, 2, 3])

if st.button("Adicionar à composição"):
    st.session_state.comp[selected_champ] = estrela

# Mostrar composição atual
if st.session_state.comp:
    st.markdown("### Sua composição:")
    for champ, star in st.session_state.comp.items():
        st.write(f"{champ} ({star}⭐)")

    if st.button("Limpar composição"):
        st.session_state.comp = {}

    if st.button("Prever resultado"):
        data = {col: 0 for col in feature_cols}
        traits_ativos = set()
        cost_total = 0
        qtd_campeoes = len(st.session_state.comp)

        for champ, estrelas in st.session_state.comp.items():
            col_name = f"champ_TFT14_{champ}"
            if col_name in data:
                data[col_name] = estrelas
            champ_key = f"TFT14_{champ}"
            cost_total += estrelas * custo_por_campeao.get(champ_key, 1)
            traits_cruas = campeao_traits.get(champ_key, [])
            for trait in traits_cruas:
                trait_set14 = depara_traits.get(trait, trait)
                traits_ativos.add(trait_set14)

        for trait in traits_ativos:
            col_name = f"trait_{trait}"
            if col_name in data:
                data[col_name] = 1

        data["cost_total"] = cost_total
        data["qtd_campeoes"] = qtd_campeoes

        input_df = pd.DataFrame([data])
        prediction = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0][1]

        st.subheader("Resultado da previsão:")
        if prediction == 1:
            st.success(f"Alta chance de Top 4! (Confiança: {prob:.2%})")
        else:
            st.warning(f"Baixa chance de Top 4. (Confiança: {prob:.2%})")
else:
    st.info("Nenhum campeão adicionado ainda.")
