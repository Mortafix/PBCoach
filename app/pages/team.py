import reflex as rx
from app.components.extra import page_loading, page_title
from app.states.overview import OverviewState
from app.states.team import TeamState
from app.templates import template


@template(
    route="/[match_id]/team",
    title="Statistiche Team",
    on_load=[OverviewState.on_load, TeamState.on_load],
)
def team_page() -> rx.Component:
    page = rx.vstack(
        rx.cond(
            TeamState.is_sidebar_open,
            page_title("users", "Statisiche del Team"),
            page_title("users", f"Statisiche del Team • {TeamState.match_name}"),
        ),
        rx.badge(rx.text("Coming soon!", size="4"), size="3"),
        spacing="5",
        width="100%",
    )
    return rx.cond(TeamState.match_players, page, page_loading())
