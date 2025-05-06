
import json
import pandas as pd

def extrair_dados_para_dataset(json_path, output_csv):
    with open(json_path, "r", encoding="utf-8") as f:
        dados_partidas = json.load(f)

    registros = []
    for partida in dados_partidas:
        for jogador in partida.get("info", {}).get("participants", []):
            campeoes = []
            itens = []
            traits = []

            for unit in jogador.get("units", []):
                campeoes.append(unit.get("character_id", "unknown"))
                itens.append([item for item in unit.get("items", [])])

            for trait in jogador.get("traits", []):
                if trait.get("tier_current", 0) > 0:
                    traits.append(trait["name"])

            registros.append({
                "champions": ",".join(campeoes),
                "cost_total": sum([unit.get("tier", 0) for unit in jogador.get("units", [])]),
                "traits": ",".join(traits),
                "items": str(itens),
                "placement": jogador.get("placement", 0)
            })

    df = pd.DataFrame(registros)
    df.to_csv(output_csv, index=False)
    print(f"[OK] Dataset salvo como: {output_csv}")

if __name__ == "__main__":
    caminho_json = input("Digite o caminho do arquivo JSON: ").strip()
    caminho_csv = input("Digite o nome do CSV de saída (ex: saida.csv): ").strip()
    extrair_dados_para_dataset(caminho_json, caminho_csv)
