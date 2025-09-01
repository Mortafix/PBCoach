from datetime import datetime
from json import load
from os import path

import reflex as rx
from app.database.connection import DB


def get_match_stats(code):
    return DB.stats.find_one({"code": code}) or dict()


def get_matches_stats(filters, sort):
    return DB.stats.find(filters, sort=sort)


def get_match_insights(code):
    return DB.insights.find_one({"code": code})


def get_matches_insights(filters, sort):
    return DB.insights.find(filters, sort=sort)


# ----- NEW


def create_match(code, match_data, extra_info):
    players = [
        int(match_data.get(f"giocatore_{i+1}", -1))
        for i in range(4)
        if extra_info.get("players") == 4 or i in [0, 2]
    ]
    unknown_idx = 1
    for i, player in enumerate(players):
        if player < 0:
            players[i] = -unknown_idx
            unknown_idx += 1
    # get json
    base_client_dir = path.join(rx.get_upload_dir(), code)
    stats_data = load(open(path.join(base_client_dir, "stats.json")))
    stats_data |= {
        "info": {
            "name": match_data.get("name"),
            "date": datetime.fromisoformat(
                f"{match_data.get('date')}T{match_data.get('time')}"
            ),
            "type": match_data.get("match-type"),
            "location": int(match_data.get("location")),
            "location-type": match_data.get("location-type"),
            "weather": match_data.get("weather"),
            "video": extra_info.get("video") or match_data.get("video-id"),
            "pbvision-url": extra_info.get("url"),
        },
        "players_ids": players,
    }
    stats_data["game"]["game_outcome"] = [
        int(match_data.get("score1")),
        int(match_data.get("score2")),
    ]
    insights_data = load(open(path.join(base_client_dir, "insights.json")))
    if DB.stats.insert_one(stats_data):
        return DB.insights.insert_one(insights_data)
    return False
