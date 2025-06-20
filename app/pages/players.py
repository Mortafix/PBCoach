import reflex as rx
from app.components.extra import page_title
from app.states.matches import MatchesState
from app.templates import template


@template(
    route="/players",
    title="Giocatori",
    on_load=MatchesState.on_load,
)
def matches_page() -> rx.Component:
    return rx.vstack(
        page_title("users", "Giocatori"),
        rx.badge(rx.text("Coming soon!", size="4"), size="3"),
        spacing="5",
        width="100%",
    )
