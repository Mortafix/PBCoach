import reflex as rx


class State(rx.State):
    is_sidebar_open: bool = True
    is_sidebar_force_open: bool = False
    is_in_match: bool = False

    # ---- PAGE
    current_page: str = "/"
    previous_page: str = "/"

    # ---- MATCH
    match_name: str = ""
    match_players: list[str] = []
    match_is_double: bool = True

    # ---- VARS

    @property
    def current_url(self) -> str:
        return self.router.page.path

    # ---- FUNCS

    @rx.event
    def on_load(self):
        # update pages
        if self.current_url != self.current_page:
            self.previous_page = self.current_page
            self.current_page = self.current_url
        self.is_sidebar_force_open = False
        self.is_in_match = False
        self.match_name = ""
        self.match_players = []
        self.match_is_double = True

    @rx.event
    def toggle_sidebar(self):
        self.is_sidebar_open = not self.is_sidebar_open

    @rx.event
    def toggle_sidebar_force(self):
        self.is_sidebar_force_open = not self.is_sidebar_force_open
        self.is_sidebar_open = True
