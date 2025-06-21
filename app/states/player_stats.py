import reflex as rx
from app.states.overview import OverviewState


class PlayerState(OverviewState):
    player_name: str = ""

    @rx.event
    def on_load(self):
        self.player_name = self.match.players[int(self.player_id)]
