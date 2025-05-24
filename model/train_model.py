import pandas as pd
import joblib
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# CONFIGURAÇÕES
INPUT_CSV = "dataset/dataset.csv"
MODEL_PATH = "model/random_forest_tft.pkl"
LOG_FILE = "log/train_log.txt"

# FUNÇÃO DE LOG
def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {msg}\n")
    print(msg)

# Limpa o log no início
open(LOG_FILE, "w").close()

# Carregar dataset
log("🔍 Carregando dataset...")
df = pd.read_csv(INPUT_CSV, dtype=str, low_memory=False)

df["is_top4"] = pd.to_numeric(df["is_top4"], errors="coerce")
df = df[df["is_top4"].notna()]
df["is_top4"] = df["is_top4"].astype(int)

# Definir colunas
champ_name_cols = [f"champ_{i}_name" for i in range(1, 11)]
champ_tier_cols = [f"champ_{i}_tier" for i in range(1, 11)]
trait_cols = [f"trait_{i}" for i in range(1, 21)]
item_cols = [f"item_{i}_{j}" for i in range(1, 11) for j in range(1, 3+1)]
extra_numeric = ["qtd_campeoes", "qtd_traits_ativas"]

target_col = "is_top4"

categorical_cols = champ_name_cols + trait_cols + item_cols
numeric_cols = champ_tier_cols + extra_numeric

# Corrigir tipos
log("🔧 Corrigindo tipos de dados...")
df[categorical_cols] = df[categorical_cols].fillna("missing").astype(str)
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce").fillna(0).astype(float)

# Separar dados
X = df.drop(columns=[target_col, "placement"])
y = df[target_col]

log(f"🔍 Shape dos dados: {X.shape}")
log(f"🔍 Balanceamento do target:\n{y.value_counts(dropna=False)}")

# Pré-processamento
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", StandardScaler(), numeric_cols)
    ]
)

# Pipeline do modelo
clf = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

# Treinamento e teste
log("🚀 Iniciando treinamento...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
clf.fit(X_train, y_train)

# Avaliação
y_pred = clf.predict(X_test)
log(f"✅ Acurácia: {accuracy_score(y_test, y_pred)}")
log(f"✅ Matriz de confusão:\n{confusion_matrix(y_test, y_pred)}")
log(f"✅ Relatório de classificação:\n{classification_report(y_test, y_pred)}")

# Salvar modelo treinado
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(clf, MODEL_PATH)
log(f"💾 [OK] Modelo salvo em {MODEL_PATH}")
