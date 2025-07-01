from datetime import datetime
from locale import LC_TIME, setlocale

import reflex as rx
from app.database.locations import get_all_locations
from app.database.matches import Partita, get_all_matches, get_months_matches
from app.database.players import get_all_players, get_player_name
from app.templates.base import State
from dateutil.relativedelta import relativedelta

setlocale(LC_TIME, "it_IT.UTF-8")


class MatchesState(State):
    matches: list[Partita] = []
    players: list[tuple[int, str]] = []
    locations: list[tuple[int, str]] = []
    months: list[tuple[str, str]] = []

    @rx.event
    def on_load(self):
        filters = self.build_filters()
        self.matches = get_all_matches(filters, sort=[("info.date", -1)])
        self.players = [
            (int(player.id), get_player_name(player.id))
            for player in get_all_players(sort=[("name", 1)], parse=True)
        ]
        self.locations = [
            (int(location.id), location.name)
            for location in get_all_locations(sort=[("name", 1)], parse=True)
        ]
        self.months = list(get_months_matches().items())

    @rx.event
    def chips_update(self):
        filters = self.build_filters()
        self.matches = get_all_matches(filters, sort=[("info.date", -1)])

    @rx.event
    def build_filters(self):
        date_filter = [
            {"info.date": {"$gte": month, "$lt": month + relativedelta(months=1)}}
            for el in self.selected_items.get("months", [])
            if (month := datetime(*map(int, el.split(".")[::-1]), 1))
        ]
        filters = {
            "players_ids": {
                "$in": [int(el) for el in self.selected_items.get("players", [])]
            },
            "info.location": {
                "$in": [int(el) for el in self.selected_items.get("location", [])]
            },
            "info.location-type": {"$in": list(self.selected_items.get("field", []))},
            "info.type": {"$in": list(self.selected_items.get("type", []))},
        }
        if date_filter:
            filters["$or"] = date_filter
        return {key: val for key, val in filters.items() if key == "$or" or val["$in"]}
