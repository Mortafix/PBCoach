from locale import LC_TIME, setlocale

import reflex as rx
from app.database.matches import Partita, get_all_matches
from app.templates.base import State

setlocale(LC_TIME, "it_IT.UTF-8")


class MatchesState(State):
    matches: list[Partita] = []

    @rx.event
    def on_load(self):
        self.matches = get_all_matches()
