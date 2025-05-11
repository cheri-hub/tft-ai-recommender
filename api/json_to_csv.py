
import json
import csv

# Caminho de entrada e saída
input_file = "../dataset/tft_raw_match_log.json"
output_file = "../dataset/tft_match_dataset.csv"

# Lista para armazenar os dados transformados
dados_final = []

with open(input_file, "r", encoding="utf-8") as f:
    partidas = json.load(f)

for partida in partidas:
    for p in partida["info"]["participants"]:
        campeoes = []
        traits = []
        items = []
        custo_total = 0

        for unit in p.get("units", []):
            champ_id = unit.get("character_id")
            estrelas = unit.get("tier", 1)  # número de estrelas
            if champ_id:
                campeoes.append(f"{champ_id}:{estrelas}")
                custo_total += estrelas * unit.get("rarity", 0) + estrelas  # fórmula estimada
                for item in unit.get("items", []):
                    items.append(str(item))

        for t in p.get("traits", []):
            if t.get("tier_current", 0) > 0:
                traits.append(t["name"])

        dados_final.append({
            "champions": ",".join(campeoes),
            "traits": ",".join(traits),
            "items": ",".join(items),
            "cost_total": custo_total,
            "placement": p["placement"]
        })

# Salvar em CSV
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=dados_final[0].keys())
    writer.writeheader()
    writer.writerows(dados_final)

print("[OK] Novo dataset com estrelas gerado:", output_file)
