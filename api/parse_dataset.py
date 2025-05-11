
import pandas as pd

# Carrega o CSV original com estrelas no formato "TFT14_Jhin:2"
df = pd.read_csv("dataset/tft_match_dataset.csv")

# 1. Processar campeões com estrela
def processar_campeoes(camplist):
    resultado = {}
    for item in camplist.split(","):
        if ":" in item:
            champ, estrela = item.split(":")
            resultado[champ] = int(estrela)
    return resultado

df["champions"] = df["champions"].fillna("")
champ_dicts = df["champions"].apply(processar_campeoes)

# 2. Obter todos os campeões únicos
todos_champ = sorted(set(k for d in champ_dicts for k in d.keys()))

# 3. Criar colunas numéricas com os níveis de estrela
for champ in todos_champ:
    df[f"champ_{champ}"] = champ_dicts.apply(lambda d: d.get(champ, 0))

# 4. Processar traits
df["traits"] = df["traits"].fillna("").apply(lambda x: x.split(",") if x else [])

from sklearn.preprocessing import MultiLabelBinarizer
mlb_traits = MultiLabelBinarizer()
traits_encoded = pd.DataFrame(mlb_traits.fit_transform(df["traits"]), columns=[f"trait_{t}" for t in mlb_traits.classes_])

# 5. Criar variável alvo
df["is_top4"] = df["placement"].apply(lambda x: 1 if x <= 4 else 0)

# 6. Criar qtd_campeoes
df["qtd_campeoes"] = champ_dicts.apply(lambda d: len(d))

# 7. Montar dataset final
df_final = pd.concat([df[[f"champ_{c}" for c in todos_champ]], traits_encoded, df[["cost_total", "qtd_campeoes", "is_top4"]]], axis=1)

# 8. Salvar novo CSV vetorizado
df_final.to_csv("dataset/dataset_vetorizado.csv", index=False)
print("[OK] Dataset vetorizado com estrelas e qtd_campeoes salvo.")
