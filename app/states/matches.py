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
    matches_loading: bool = False
    matches: list[Partita] = []
    players: list[tuple[int, str]] = []
    locations: list[tuple[int, str]] = []
    months: list[tuple[str, str]] = []
    are_filters_set: bool = False

    @rx.event
    def on_load(self):
        self.matches_loading = True
        yield
        self.match = None
        self.are_filters_set = False
        self.matches = get_all_matches(sort=[("info.date", -1)])
        self.players = [
            (int(player.id), get_player_name(player.id))
            for player in get_all_players(sort=[("name", 1)], parse=True)
        ]
        self.locations = [
            (int(location.id), location.name)
            for location in get_all_locations(sort=[("name", 1)], parse=True)
        ]
        self.months = list(get_months_matches().items())
        self.matches_loading = False

    @rx.event
    def chips_update(self):
        self.matches_loading = True
        yield
        filters = self.build_filters()
        self.matches = get_all_matches(filters, sort=[("info.date", -1)])
        self.matches_loading = False

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
            "session.num_players": {
                "$in": [int(el) for el in self.selected_items.get("mode", [])]
            },
        }
        if date_filter:
            filters["$or"] = date_filter
        filters = {key: el for key, el in filters.items() if key == "$or" or el["$in"]}
        self.are_filters_set = bool(filters)
        return filters

    @rx.event
    def reset_filters(self):
        self.matches_loading = True
        yield
        self.selected_items.clear()
        self.are_filters_set = False
        self.matches = get_all_matches(sort=[("info.date", -1)])
        self.matches_loading = False
