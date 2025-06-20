import reflex as rx
from app.states.overview import OverviewState


class TeamState(OverviewState):
    @rx.event
    def on_load(self):
        ...
