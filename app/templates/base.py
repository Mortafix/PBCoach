import reflex as rx
from app.database.matches import Partita


class State(rx.State):
    is_header_open: bool = True
    is_sidebar_open: bool = True
    is_sidebar_force_open: bool = False
    is_in_match: bool = False
    expander_is_open: bool = False
    selected_items: dict[str, list[str]] = {}

    # ---- PAGE
    current_page: str = "/"
    previous_page: str = "/"

    # ---- MATCH
    match: Partita | None = None
    match_stats: dict = {}
    match_insights: dict = {}

    # ---- VARS

    @property
    def current_url(self) -> str:
        return self.router.url

    # ---- FUNCS

    @rx.event
    def on_load(self):
        # update pages
        if self.current_url != self.current_page:
            self.previous_page = self.current_page
            self.current_page = self.current_url
        self.is_header_open = True
        self.is_sidebar_force_open = False
        self.is_sidebar_open = False
        self.is_in_match = False
        self.match = None
        self.selected_items = {}

    @rx.event
    def toggle_sidebar(self):
        self.is_sidebar_open = not self.is_sidebar_open

    @rx.event
    def toggle_sidebar_force(self):
        self.is_sidebar_force_open = not self.is_sidebar_force_open
        self.is_sidebar_open = True
