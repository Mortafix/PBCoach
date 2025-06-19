from datetime import datetime
from json import load
from os import path

import reflex as rx
from app.database.connection import DB


def get_match_stats(code):
    return DB.stats.find_one({"code": code})


def get_match_insights(code):
    return DB.insights.find_one({"code": code})


def create_match(code, match_data):
    players = [int(match_data.get(f"giocatore_{i+1}", -1)) for i in range(4)]
    unknown_idx = 1
    for i, player in enumerate(players):
        if player < 0:
            players[i] = -unknown_idx
            unknown_idx += 1
    # get json
    base_client_dir = path.join(rx.get_upload_dir(), code)
    stats_data = load(open(path.join(base_client_dir, "stats.json")))
    stats_data |= {
        "match_name": match_data.get("name"),
        "match_date": datetime.fromisoformat(
            f"{match_data.get('date')}T{match_data.get('time')}"
        ),
        "players_ids": players,
    }
    insights_data = load(open(path.join(base_client_dir, "insights.json")))
    if DB.stats.insert_one(stats_data):
        return DB.insights.insert_one(insights_data)
    return False
