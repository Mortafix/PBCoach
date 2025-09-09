import reflex as rx
from app.database.connection import DB


class Player(rx.Base):
    id: int
    name: str
    surname: str
    short_name: str
    gender: str


def parse_model(data):
    name = data.get("name")
    surname = data.get("surname")
    short_name = f"{name} {surname[0]}." if surname else name
    return Player(
        id=data.get("id"),
        name=name,
        surname=surname,
        short_name=short_name,
        gender=data.get("gender", ""),
    )


def get_all_players(filters=None, sort=None, limit=10**10, names=False, parse=False):
    players = DB.players.find(filters, sort=sort or [("id", 1)], limit=limit)
    if names:
        return [f"{player.get('name')} {player.get('surname')}" for player in players]
    if parse:
        return [parse_model(player) for player in players]
    return list(players)


def get_last_id():
    entry = list(get_all_players(sort=[("id", -1)], limit=1))
    return entry[0].get("id") if entry else 0


def add_player_to_db(name, surname, gender):
    new_id = get_last_id() + 1
    data = {
        "id": new_id,
        "name": name.title(),
        "surname": surname.title(),
        "gender": gender,
    }
    if DB.players.insert_one(data):
        return new_id


def get_player_name(player_id, short=False, only_name=False):
    if player_id < 0:
        return f"Sconosciuto {-player_id}"
    player = DB.players.find_one({"id": player_id})
    name, surname = player.get("name"), player.get("surname")
    if only_name or not surname:
        return name
    if short:
        return f"{name} {surname[0]}."
    return f"{name} {surname}"


def get_players_general_stats():
    played = dict()
    qualities = dict()
    qualities_hist = dict()
    for match in DB.stats.find(
        {"info.type": {"$ne": "Allenamento"}}, sort=[("info.date", 1)]
    ):
        players_stats = [stats for stats in match.get("players") if stats]
        players_ids = match.get("players_ids")
        for player in players_ids:
            played[player] = played.get(player, 0) + 1
        for i, player in enumerate(players_stats):
            player_id = players_ids[i]
            quality = round(player.get("average_shot_quality") * 100)
            qualities_hist[player_id] = qualities_hist.get(player_id, []) + [quality]
    # qualita pesata sulle ultime partite
    for player, history in qualities_hist.items():
        pesi = list(range(1, len(history) + 1))
        media_ponderata = sum(v * p for v, p in zip(history, pesi)) / sum(pesi)
        qualities[player] = round(media_ponderata)
    return played, qualities, qualities_hist


def get_player_gender_from_db(player_id):
    giocatore = DB.players.find_one({"id": player_id})
    return giocatore.get("gender", "") if giocatore else ""
