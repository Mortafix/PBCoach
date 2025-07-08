from datetime import datetime
from locale import LC_TIME, setlocale

import reflex as rx
from app.database.connection import DB
from app.database.locations import get_location_name
from app.database.players import get_player_name

setlocale(LC_TIME, "it_IT.UTF-8")


class Partita(rx.Base):
    code: str
    name: str
    date: datetime
    date_str: str
    date_str_short: str
    location: str
    location_type: str
    type: str
    weather: str | None = None
    players: list[str]
    players_full: list[str]
    players_ids: list[int]
    players_full_ids: list[int]
    players_n: int
    score: tuple[int, int]
    team1_idx: list[int]
    team2_idx: list[int]
    win_team1: bool
    is_double: bool = True
    video_id: str | None = None


def parse_model(data):
    players_ids = data.get("players_ids")
    players = [get_player_name(p_id, short=True) for p_id in players_ids]
    players_n = len(players)
    score = data.get("game", {}).get("game_outcome")
    return Partita(
        code=data.get("code"),
        name=data.get("info").get("name"),
        date=data.get("info").get("date"),
        date_str=format(data.get("info").get("date"), "%A • %d %B %y • %H:%M"),
        date_str_short=format(data.get("info").get("date"), "%a • %d %b %y • %H:%M"),
        location=get_location_name(data.get("info").get("location")),
        location_type=data.get("info").get("location-type"),
        type=data.get("info").get("type"),
        weather=data.get("info").get("weather"),
        players=players,
        players_full=players if players_n == 4 else [players[0], "", players[1], ""],
        players_ids=players_ids,
        players_full_ids=players_ids
        if players_n == 4
        else [players_ids[0], 0, players_ids[1], 0],
        players_n=players_n,
        score=score,
        team1_idx=[0, 1] if players_n == 4 else [0],
        team2_idx=[2, 3] if players_n == 4 else [1],
        win_team1=score[0] > score[1],
        is_double=players_n == 4,
        video_id=data.get("info").get("video"),
    )


def get_all_matches(filters=None, sort=None, limit=10**10, parse=True):
    matches = DB.stats.find(filters, sort=sort or [("match_date", 1)], limit=limit)
    if parse:
        return [parse_model(match) for match in matches]
    return matches


def get_months_matches(fmt="%B %y"):
    return {
        format(date, "%m.%Y"): format(date, fmt).title()
        for match in DB.stats.find()
        if (date := match.get("info", {}).get("date"))
    }
