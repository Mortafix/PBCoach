from locale import LC_TIME, setlocale

import reflex as rx
from app.database.players import (Player, get_all_players,
                                  get_players_general_stats)
from app.templates.base import State

setlocale(LC_TIME, "it_IT.UTF-8")


class PlayersState(State):
    search_text: str = ""
    players: list[Player] = []
    is_search_active: bool = False
    players_played: dict[int, int] = {}
    players_quality: dict[int, int] = {}
    players_quality_history: dict[int, list[int]] = {}
    players_quality_chart_data: dict[int, list] = {}

    @rx.event
    def on_load(self):
        self.search_text = ""
        self.is_search_active = False
        self.is_hamburger_visible = False
        self.players = get_all_players(sort=[("name", 1), ("surname", 1)], parse=True)
        stats = get_players_general_stats()
        self.players_played, self.players_quality, self.players_quality_history = stats
        self.players_quality_chart_data = {
            player: [{"x": i, "y": valore} for i, valore in enumerate(history[:10])]
            for player, history in self.players_quality_history.items()
        }

    @rx.event
    def reset_search(self):
        self.search_text = ""
        self.is_search_active = False
        self.players = get_all_players(sort=[("name", 1), ("surname", 1)], parse=True)

    @rx.event
    def search(self, text):
        self.is_search_active = text != ""
        self.search_text = text
        filters = {
            "$or": [
                {attr: {"$regex": text, "$options": "i"}}
                for attr in ("name", "surname")
            ]
        }
        self.players = get_all_players(
            filters, sort=[("name", 1), ("surname", 1)], parse=True
        )
