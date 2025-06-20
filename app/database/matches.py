from datetime import datetime

import reflex as rx
from app.database.connection import DB
from app.database.players import get_player_name


class Partita(rx.Base):
    code: str
    name: str
    date: datetime
    date_str: str
    players: list[str]
    players_n: int
    score: tuple[int, int]
    team1_idx: list[int]
    team2_idx: list[int]
    win_team1: bool


def parse_model(data):
    players_n = len(data.get("players_ids"))
    score = data.get("game", {}).get("game_outcome")
    return Partita(
        code=data.get("code"),
        name=data.get("match_name"),
        date=data.get("match_date"),
        date_str=format(data.get("match_date"), "%A • %d %B %y • %H:%M"),
        players=[get_player_name(p_id, short=True) for p_id in data.get("players_ids")],
        players_n=players_n,
        score=score,
        team1_idx=[0, 1] if players_n == 4 else [0],
        team2_idx=[2, 3] if players_n == 4 else [1],
        win_team1=score[0] > score[1],
    )


def get_all_matches(filters=None, sort=None, limit=10**10, parse=True):
    matches = DB.stats.find(filters, sort=sort or [("match_date", 1)], limit=limit)
    if parse:
        return [parse_model(match) for match in matches]
    return matches
