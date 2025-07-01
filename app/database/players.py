import reflex as rx
from app.database.connection import DB


class Player(rx.Base):
    id: int
    name: str
    surname: str


def parse_model(data):
    return Player(id=data.get("id"), name=data.get("name"), surname=data.get("surname"))


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


def add_player_to_db(name, surname):
    data = {"id": get_last_id() + 1, "name": name, "surname": surname}
    return DB.players.insert_one(data)


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
