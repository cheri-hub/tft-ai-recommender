import streamlit as st
import pandas as pd
import joblib
import json
from collections import Counter

# Carregar modelo e dados auxiliares
model = joblib.load("model/random_forest_tft.pkl")
vetorizado_df = pd.read_csv("dataset/dataset.csv", dtype=str, low_memory=False)

with open("helper/campeao_traits.json", "r", encoding="utf-8") as f:
    campeao_traits = json.load(f)

# Preparar lista de campeões
lista_de_campeoes = sorted(set(vetorizado_df[[f"champ_{i}_name" for i in range(1, 11)]].stack().dropna().unique()))

# Inicializar sessão
if "comp" not in st.session_state:
    st.session_state.comp = {}

# Interface
st.title("🔮 Recomendador TFT - Previsão de Top 4")
st.markdown("Monte sua composição abaixo selecionando campeões e suas estrelas.")

# Seletor de campeão
col1, col2 = st.columns(2)
with col1:
    selected_champ = st.selectbox("Escolha um campeão", lista_de_campeoes)
with col2:
    estrela = st.selectbox("Nível de estrela", [1, 2, 3])

if st.button("Adicionar à composição"):
    if len(st.session_state.comp) >= 10:
        st.warning("❌ Máximo de 10 campeões por composição.")
    else:
        st.session_state.comp[selected_champ] = estrela

# Mostrar composição atual
if st.session_state.comp:
    st.markdown("### 🧠 Sua composição:")
    for champ, star in st.session_state.comp.items():
        st.write(f"• {champ} ({star}⭐)")

    if st.button("Limpar composição"):
        st.session_state.comp = {}

    # 🔥 Análise da composição
    st.markdown("---")
    st.subheader("📊 Análise da composição:")

    campeoes = st.session_state.comp.keys()
    qtd_campeoes = len(campeoes)

    # Calcular traits
    all_traits = []
    for champ in campeoes:
        traits = campeao_traits.get(f"TFT14_{champ}", [])
        all_traits.extend(traits)

    trait_counts = Counter(all_traits)
    traits_ativas = [trait for trait, count in trait_counts.items() if count >= 2]
    qtd_traits_ativas = len(traits_ativas)
    tier_medio = round(sum(int(st.session_state.comp[c]) for c in campeoes) / qtd_campeoes, 2) if qtd_campeoes > 0 else 0

    st.markdown(f"• 🧍‍♂️ **Qtd. Campeões:** {qtd_campeoes}")
    st.markdown(f"• ⭐ **Tier médio:** {tier_medio}")
    st.markdown(f"• 🧬 **Traits ativas:** {', '.join(traits_ativas) if traits_ativas else 'Nenhuma'}")

    if not traits_ativas:
        st.warning("⚠️ Nenhuma trait ativa. Considere ajustar sua composição!")

    # 🔥 Sugestões de melhorias
    st.subheader("💡 Sugestões para sua composição:")

    if qtd_campeoes < 10:
        st.markdown(f"👉 Você pode adicionar mais {10 - qtd_campeoes} campeão(ões).")

    # Sugestão de traits próximas de ativar
    quase_ativas = [trait for trait, count in trait_counts.items() if count == 1]

    if quase_ativas:
        st.markdown(f"👉 Você está próximo de ativar: **{', '.join(quase_ativas)}**")

        st.markdown("Sugestão de campeões que ativam essas traits:")
        for trait in quase_ativas:
            sugestoes = [
                champ.replace("TFT14_", "")
                for champ, champ_traits in campeao_traits.items()
                if trait in champ_traits and champ.replace("TFT14_", "") not in campeoes
            ]
            if sugestoes:
                st.write(f"• 🧠 **{trait}** → {', '.join(sugestoes[:5])}")
            else:
                st.write(f"• 🧠 **{trait}** → Nenhum campeão disponível.")

    else:
        st.markdown("✅ Nenhuma trait pendente, ótimo!")

    st.markdown("---")

    # 🔮 Previsão
    if st.button("🔍 Prever resultado"):
        data = {col: None for col in vetorizado_df.columns if col not in ["is_top4", "placement"]}
        champ_list = list(st.session_state.comp.items())

        # Preencher campeões
        for i in range(1, 11):
            if i <= len(champ_list):
                champ_name, tier = champ_list[i-1]
                data[f"champ_{i}_name"] = champ_name
                data[f"champ_{i}_tier"] = tier
            else:
                data[f"champ_{i}_name"] = "missing"
                data[f"champ_{i}_tier"] = 0

        # Preencher traits
        for i in range(1, 21):
            if i <= len(traits_ativas):
                data[f"trait_{i}"] = traits_ativas[i-1]
            else:
                data[f"trait_{i}"] = "missing"

        # Preencher itens (placeholder)
        for i in range(1, 11):
            for j in range(1, 4):
                data[f"item_{i}_{j}"] = "missing"

        data["qtd_campeoes"] = qtd_campeoes
        data["qtd_traits_ativas"] = qtd_traits_ativas

        # Criar DataFrame
        input_df = pd.DataFrame([data])

        # Tratar tipos (igual ao treino)
        for col in input_df.columns:
            if "tier" in col or col in ["qtd_campeoes", "qtd_traits_ativas"]:
                input_df[col] = pd.to_numeric(input_df[col], errors="coerce").fillna(0).astype(float)
            else:
                input_df[col] = input_df[col].fillna("missing").astype(str)

        # 🔥 Validação da composição mínima
        if qtd_campeoes < 5:
            st.warning("❌ Você precisa ter pelo menos 5 campeões para uma previsão válida.")
            st.stop()

        if qtd_traits_ativas == 0:
            st.warning("❌ Sua composição não possui nenhuma trait ativa. Adicione sinergias para uma previsão válida.")
            st.stop()

        # Fazer previsão
        prediction = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0][1]

        st.subheader("🎯 Resultado da previsão:")
        if prediction == 1:
            st.success(f"Alta chance de Top 4! 🚀 (Confiança: {prob:.2%})")
        else:
            st.warning(f"Baixa chance de Top 4. ⚠️ (Confiança: {prob:.2%})")
else:
    st.info("Nenhum campeão adicionado ainda. 👾")
