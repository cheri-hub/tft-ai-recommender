import pandas as pd
from datetime import datetime

# CONFIGURAÇÕES
INPUT_CSV = "dataset/dataset.csv"
LOG_FILE = "log/validate_log.txt"

# FUNÇÃO DE LOG
def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {msg}\n")
    print(msg)

# Limpa o arquivo de log ao iniciar
open(LOG_FILE, "w").close()

# Carregar dataset
df = pd.read_csv(INPUT_CSV)

log("\n🔍 [CHECK] Shape do dataset:")
log(str(df.shape))

log("\n🔍 [CHECK] Colunas do dataset:")
log(str(df.columns.tolist()))

log("\n🔍 [CHECK] Verificar distribuição de placement:")
if "placement" in df.columns:
    log(str(df["placement"].value_counts().sort_index()))
else:
    log("❌ [ERRO] Coluna 'placement' não encontrada no dataset.")

log("\n🔍 [CHECK] Verificar balanceamento de is_top4:")
if "is_top4" in df.columns:
    log(str(df["is_top4"].value_counts(dropna=False)))
else:
    log("❌ [ERRO] Coluna 'is_top4' não encontrada no dataset.")

log("\n🔍 [CHECK] Verificar campos com NaN:")
log(str(df.isna().sum()))

log("\n✅ Validação concluída. ✔️")
