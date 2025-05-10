
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

# Carrega o CSV original
df = pd.read_csv("../dataset/tft_match_dataset.csv")

# 1. Processar a coluna "champions" (lista separada por vírgulas)
df["champions"] = df["champions"].fillna("").apply(lambda x: x.split(",") if x else [])

# 2. Processar a coluna "traits" (lista separada por vírgulas)
df["traits"] = df["traits"].fillna("").apply(lambda x: x.split(",") if x else [])

# 3. One-hot encoding dos campeões
mlb_champs = MultiLabelBinarizer()
champions_encoded = pd.DataFrame(
    mlb_champs.fit_transform(df["champions"]),
    columns=[f"champ_{c}" for c in mlb_champs.classes_]
)

# 4. One-hot encoding das traits (sinergias)
mlb_traits = MultiLabelBinarizer()
traits_encoded = pd.DataFrame(
    mlb_traits.fit_transform(df["traits"]),
    columns=[f"trait_{t}" for t in mlb_traits.classes_]
)

# 5. Criar a variável alvo "is_top4"
df["is_top4"] = df["placement"].apply(lambda x: 1 if x <= 4 else 0)

# 6. Juntar os dados transformados
df_final = pd.concat([champions_encoded, traits_encoded, df[["cost_total", "is_top4"]]], axis=1)

# 7. Salvar em novo CSV
df_final.to_csv("../dataset/dataset_vetorizado.csv", index=False)
print("[OK] Dataset vetorizado salvo como ../dataset/dataset_vetorizado.csv")
