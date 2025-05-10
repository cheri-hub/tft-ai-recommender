
import streamlit as st
import pandas as pd
import joblib

# Carregar modelo
model = joblib.load("model/random_forest_tft.pkl")

# Carregar estrutura do dataset para gerar colunas
exemplo_df = pd.read_csv("dataset/dataset_vetorizado.csv", nrows=1)
feature_cols = [col for col in exemplo_df.columns if col not in ["is_top4"]]

# Interface do usuário
st.title("Recomendador TFT - Previsão de Top 4")

st.markdown("Insira os campeões, sinergias e custo total da sua composição atual.")

# Entradas básicas
champ_input = st.text_input("Campeões (separados por vírgula)", value="TFT9_Jhin,TFT9_Senna")
trait_input = st.text_input("Sinergias (separadas por vírgula)", value="Technogenius,Deadeye")
cost_total = st.number_input("Custo total da composição (soma dos tiers)", min_value=0, value=18)

if st.button("Prever"):
    # Preparar os dados de entrada
    champs = champ_input.replace(" ", "").split(",")
    traits = trait_input.replace(" ", "").split(",")

    data = {col: 0 for col in feature_cols}
    for champ in champs:
        col_name = f"champ_{champ}"
        if col_name in data:
            data[col_name] = 1
    for trait in traits:
        col_name = f"trait_{trait}"
        if col_name in data:
            data[col_name] = 1
    data["cost_total"] = cost_total

    input_df = pd.DataFrame([data])
    prediction = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]

    st.subheader("Resultado da previsão:")
    if prediction == 1:
        st.success(f"Alta chance de Top 4! (Confiança: {prob:.2%})")
    else:
        st.warning(f"Baixa chance de Top 4. (Confiança: {prob:.2%})")
