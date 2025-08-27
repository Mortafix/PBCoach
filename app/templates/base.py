from re import search

import reflex as rx
from app.database.matches import Partita


class State(rx.State):
    is_header_open: bool = True
    is_hamburger_visible: bool = True
    is_sidebar_open: bool = True
    is_sidebar_force_open: bool = False
    is_in_match: bool = False
    expander_is_open: bool = False
    selected_items: dict[str, list[str]] = {}

    # ---- MATCH
    match: Partita | None = None
    match_stats: dict = {}
    match_insights: dict = {}

    # ---- FUNCS

    @rx.event
    def on_load(self):
        if self.match and self.match.code == self.match_id:
            return
        self.is_header_open = True
        if search(r"^/match/", self.router.route_id):
            self.is_in_match = True
            self.match = None
            self.is_sidebar_open = True
            self.is_hamburger_visible = True
            return
        self.is_hamburger_visible = False
        self.is_in_match = False
        self.is_sidebar_force_open = False
        self.is_sidebar_open = False
        self.selected_items = {}

    @rx.event
    def toggle_sidebar(self):
        self.is_sidebar_open = not self.is_sidebar_open

    @rx.event
    def toggle_sidebar_force(self):
        self.is_sidebar_force_open = not self.is_sidebar_force_open
        self.is_sidebar_open = True
