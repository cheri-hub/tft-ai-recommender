
import requests
import os
import pandas as pd
from dotenv import load_dotenv
from time import sleep
from datetime import datetime, timedelta, timezone

# Carrega a chave da API
load_dotenv()
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
HEADERS = {"X-Riot-Token": RIOT_API_KEY}

REGION_TFT = "americas"
REGION_SUMMONER = "br1"

def get_challenger_players():
    url = f"https://{REGION_SUMMONER}.api.riotgames.com/tft/league/v1/challenger"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return [entry["summonerId"] for entry in resp.json()["entries"]]
    else:
        print("[ERRO] Falha ao buscar jogadores challenger:", resp.status_code)
        return []

def get_summoner_info(summoner_id):
    url = f"https://{REGION_SUMMONER}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()
    return None

def get_match_ids(puuid, count=20):
    url = f"https://{REGION_TFT}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count={count}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()
    return []

def get_match_data(match_id):
    url = f"https://{REGION_TFT}.api.riotgames.com/tft/match/v1/matches/{match_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()
    return None

def extrair_partidas_recentes(partidas_json):
    tres_dias_atras = datetime.now(timezone.utc) - timedelta(days=3)
    registros = []
    for partida in partidas_json:
        game_time = datetime.fromtimestamp(partida["info"]["game_datetime"] / 1000, tz=timezone.utc)
        if game_time < tres_dias_atras:
            continue
        for jogador in partida["info"]["participants"]:
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
    return registros

def main():
    print("🔎 Coletando jogadores Challenger...")
    summoner_ids = get_challenger_players()
    all_partidas = []
    for idx, summoner_id in enumerate(summoner_ids[:10]):  # limite reduzido para testes
        info = get_summoner_info(summoner_id)
        if not info:
            continue
        puuid = info["puuid"]
        match_ids = get_match_ids(puuid, count=20)
        for match_id in match_ids:
            dados = get_match_data(match_id)
            if dados:
                all_partidas.append(dados)
                print(f"[{idx+1}] Coletado match {match_id}")
                sleep(1.2)

    print(f"✅ Total de partidas brutas coletadas: {len(all_partidas)}")
    print("🧼 Filtrando e formatando partidas recentes...")
    registros = extrair_partidas_recentes(all_partidas)
    df = pd.DataFrame(registros)
    output_path = "../dataset/tft_challenger_dataset.csv"
    df.to_csv(output_path, index=False)
    print(f"[OK] Dataset final salvo como: {output_path}")

if __name__ == "__main__":
    main()
