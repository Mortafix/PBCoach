import reflex as rx
from app.templates.base import State


class PlayerState(State):
    @rx.event
    def on_load(self):
        self.get_match_stat()
