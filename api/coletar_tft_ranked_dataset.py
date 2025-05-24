
import requests
import os
import json
import pandas as pd
from dotenv import load_dotenv
from time import sleep
from datetime import datetime, timedelta, timezone

# Carrega a chave da API
load_dotenv()
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
HEADERS = {"X-Riot-Token": RIOT_API_KEY}
JSON_OUTPUT_PATH = "dataset/tft_raw_match_log.json"
CSV_OUTPUT_PATH = "dataset/tft_match_dataset.csv"
MATCH_QUANTITY = 50

# Mapeamento das regiões por cluster
REGION_GROUPS = {
    "americas": ["br1", "na1", "la1", "la2"],
    "europe": ["euw1", "eun1", "tr1", "ru"],
    "asia": ["kr", "jp1"],
    "sea": ["oc1"]
}

def get_league_players(region, endpoint):
    url = f"https://{region}.api.riotgames.com{endpoint}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return [entry["summonerId"] for entry in resp.json()["entries"]]
    else:
        print(f"[ERRO] {region} {endpoint} =>", resp.status_code)
        return []

def get_summoner_info(region, summoner_id):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()
    return None

def get_match_ids(puuid, tft_region):
    url = f"https://{tft_region}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count={MATCH_QUANTITY}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()
    return []

def get_match_data(match_id, tft_region):
    url = f"https://{tft_region}.api.riotgames.com/tft/match/v1/matches/{match_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()
    return None

# def extrair_partidas_recentes(partidas_json):
#     dias_atras = datetime.now(timezone.utc) - timedelta(days=7)
#     registros = []
#     for partida in partidas_json:
#         game_time = datetime.fromtimestamp(partida["info"]["game_datetime"] / 1000, tz=timezone.utc)
#         if game_time < dias_atras:
#             continue
#         for jogador in partida["info"]["participants"]:
#             campeoes = []
#             itens = []
#             traits = []

#             for unit in jogador.get("units", []):
#                 campeoes.append(unit.get("character_id", "unknown"))
#                 itens.append([item for item in unit.get("itemNames", [])])

#             for trait in jogador.get("traits", []):
#                 if trait.get("tier_current", 0) > 0:
#                     traits.append(trait["name"])

#             registros.append({
#                 "champions": ",".join(campeoes),
#                 "cost_total": sum([unit.get("tier", 0) for unit in jogador.get("units", [])]),
#                 "traits": ",".join(traits),
#                 "items": "|".join([",".join(map(str, i)) if i else "None" for i in itens]),
#                 "placement": jogador.get("placement", 0)
#             })
#     return registros

def main():
    print("🌍 Iniciando coleta global (Challenger, Grandmaster, Master)...")
    endpoints = [
        "/tft/league/v1/challenger",
        "/tft/league/v1/grandmaster",
        "/tft/league/v1/master"
    ]

    all_partidas = []
    for tft_region, summoner_regions in REGION_GROUPS.items():
        for summoner_region in summoner_regions:
            print(f"🔍 Coletando em: {summoner_region.upper()} (cluster {tft_region})")
            for endpoint in endpoints:
                summoner_ids = get_league_players(summoner_region, endpoint)
                for idx, summoner_id in enumerate(summoner_ids[:100]):  # limitar por região
                    info = get_summoner_info(summoner_region, summoner_id)
                    if not info:
                        continue
                    puuid = info["puuid"]
                    match_ids = get_match_ids(puuid, tft_region)
                    for match_id in match_ids:
                        dados = get_match_data(match_id, tft_region)
                        if dados:
                            all_partidas.append(dados)
                            print(f"✔ Match {match_id}")
                            sleep(0.2)

    print(f"✅ Total de partidas brutas coletadas: {len(all_partidas)}")

    with open(JSON_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_partidas, f, indent=2, ensure_ascii=False)
    print(f"[OK] JSON bruto salvo em: {JSON_OUTPUT_PATH}")

    # print("🧼 Processando partidas recentes...")
    # registros = extrair_partidas_recentes(all_partidas)
    # df = pd.DataFrame(registros)
    
    # if os.path.exists(CSV_OUTPUT_PATH):
    #     os.remove(CSV_OUTPUT_PATH)
    # df.to_csv(CSV_OUTPUT_PATH, index=False)
    # print(f"[OK] Dataset final salvo como: {CSV_OUTPUT_PATH}")

if __name__ == "__main__":
    main()
