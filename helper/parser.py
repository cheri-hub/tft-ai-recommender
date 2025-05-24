import json
import pandas as pd
from collections import defaultdict
from datetime import datetime

# CONFIGURAÇÕES
INPUT_JSON = "dataset/tft_raw_match_log.json"
OUTPUT_CSV = "dataset/dataset.csv"
LOG_FILE = "log/parser_log.txt"
MAX_CHAMPS = 10
MAX_TRAITS = 20
MAX_ITEMS_PER_CHAMP = 3


# FUNÇÃO DE LOG
def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {msg}\n")
    print(msg)


# FUNÇÃO DE EXTRAÇÃO
def extract_participant_data_with_named_tiers(participant):
    champ_names = []
    champ_tiers = []
    champ_items = []

    champ_dict = defaultdict(lambda: {"tier": 0, "items": []})

    for unit in participant.get("units", []):
        champ_name = unit.get("character_id", "").replace("TFT14_", "")
        champ_dict[champ_name]["tier"] += unit.get("tier", 1)

        items = unit.get("itemNames", [])
        champ_dict[champ_name]["items"].extend(items)

    sorted_champs = sorted(champ_dict.items(), key=lambda x: x[1]["tier"], reverse=True)
    sorted_champs = sorted_champs[:MAX_CHAMPS]

    for champ_name, data in sorted_champs:
        champ_names.append(champ_name)
        champ_tiers.append(data["tier"])

        items = data["items"][:MAX_ITEMS_PER_CHAMP]
        items += [None] * (MAX_ITEMS_PER_CHAMP - len(items))
        champ_items.append(items)

    champ_names += [None] * (MAX_CHAMPS - len(champ_names))
    champ_tiers += [None] * (MAX_CHAMPS - len(champ_tiers))
    champ_items += [[None]*MAX_ITEMS_PER_CHAMP] * (MAX_CHAMPS - len(champ_items))

    traits = []
    for trait in participant.get("traits", []):
        if trait.get("tier_current", 0) > 0:
            trait_name = trait.get("name", "").replace("TFT14_", "")
            traits.append(trait_name)
    traits = traits[:MAX_TRAITS] + [None] * (MAX_TRAITS - len(traits))

    flat_items = [item for sublist in champ_items for item in sublist]

    placement = int(participant.get("placement", 9))
    is_top4 = 1 if placement <= 4 else 0

    qtd_campeoes = sum(1 for name in champ_names if name is not None)
    qtd_traits_ativas = sum(1 for trait in traits if trait is not None)

    return champ_names + champ_tiers + traits + flat_items + [placement, is_top4, qtd_campeoes, qtd_traits_ativas]


# PROCESSAMENTO
open(LOG_FILE, "w").close()

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

records = []

for match in data:
    try:
        participants = match.get("info", {}).get("participants", [])
        match_id = match.get('metadata', {}).get('match_id', 'unknown')
        log(f"✔️ Partida {match_id} com {len(participants)} jogadores")

        for p in participants:
            records.append(extract_participant_data_with_named_tiers(p))

    except Exception as e:
        log(f"❌ Erro na partida {match_id}: {e}")
        raise

# GERAR DADOS SINTÉTICOS NEGATIVOS
for qtd in range(1, 5):
    fake_row = [None] * (MAX_CHAMPS * 2)  # champs + tiers
    fake_row += [None] * MAX_TRAITS       # traits
    fake_row += [None] * (MAX_CHAMPS * MAX_ITEMS_PER_CHAMP)  # itens
    fake_row += [8, 0, qtd, 0]            # placement, is_top4, qtd_campeoes, qtd_traits_ativas
    records.append(fake_row)

log(f"➕ Adicionados dados sintéticos negativos para qtd_campeoes 1-4")

# NOMES DAS COLUNAS
champ_name_cols = [f"champ_{i+1}_name" for i in range(MAX_CHAMPS)]
champ_tier_cols = [f"champ_{i+1}_tier" for i in range(MAX_CHAMPS)]
trait_cols = [f"trait_{i+1}" for i in range(MAX_TRAITS)]
item_cols = [f"item_{i+1}_{j+1}" for i in range(MAX_CHAMPS) for j in range(MAX_ITEMS_PER_CHAMP)]
columns = champ_name_cols + champ_tier_cols + trait_cols + item_cols + ["placement", "is_top4", "qtd_campeoes", "qtd_traits_ativas"]

# Criar DataFrame
df = pd.DataFrame(records, columns=columns)

log("\n🔍 [CHECK] is_top4:")
log(str(df["is_top4"].value_counts(dropna=False)))

log("\n🔍 [CHECK] placement:")
log(str(df["placement"].value_counts().sort_index()))

df.to_csv(OUTPUT_CSV, index=False)
log(f"\n✅ Dataset salvo como {OUTPUT_CSV}")
