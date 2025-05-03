import requests
import os
import json
from dotenv import load_dotenv
from time import sleep

# Carrega a chave do .env
load_dotenv()
RIOT_API_KEY = os.getenv("RIOT_API_KEY")

# Constantes da API
HEADERS = {"X-Riot-Token": RIOT_API_KEY}
REGION_TFT = "americas"
REGION_SUMMONER = "americas"  # ou "na1", "euw1", etc., dependendo do invocador

# Caminho de saída
#OUTPUT_FILE = "dataset/partidas_raw.json"

def get_puuid(summoner_name, tag_line):
    #https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/Cheritosss/00000?api_key=RGAPI-3d5899a2-1652-4c63-912c-fb5bca78f49d
    url = f"https://{REGION_SUMMONER}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json().get("puuid")
    else:
        print(f"[ERRO] Falha ao buscar PUUID ({resp.status_code}): {resp.text}")
        return None

def get_match_ids(puuid, count=10):
    url = f"https://{REGION_TFT}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count={count}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"[ERRO] Falha ao buscar match IDs ({resp.status_code}): {resp.text}")
        return []

def get_match_data(match_id):
    url = f"https://{REGION_TFT}.api.riotgames.com/tft/match/v1/matches/{match_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"[ERRO] Falha ao buscar partida {match_id} ({resp.status_code})")
        return None

def salvar_partidas_json(partidas, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(partidas, f, indent=2, ensure_ascii=False)
    print(f"[OK] Dados salvos em {output_file}")

def coletar_partidas(summoner_name, tag_line, qtd_partidas=5):
    print(f"🔍 Buscando partidas do jogador: {summoner_name}#{tag_line}")
    puuid = get_puuid(summoner_name, tag_line)
    if not puuid:
        return
    
    output_file_path = f"dataset/partidas_raw_{summoner_name}#{tag_line}.json"

    match_ids = get_match_ids(puuid, qtd_partidas)
    print(f"🎯 {len(match_ids)} partidas encontradas. Coletando dados...")

    partidas = []
    for match_id in match_ids:
        dados = get_match_data(match_id)
        if dados:
            partidas.append(dados)
            print("...")
            sleep(1.2)  # para evitar rate limit

    salvar_partidas_json(partidas, output_file_path)

if __name__ == "__main__":
    nome_jogador = input("Digite o nome do invocador: ")
    tag_jogador = input("Digite a tag do invocador: ")
    coletar_partidas(nome_jogador, tag_jogador, qtd_partidas=10)
