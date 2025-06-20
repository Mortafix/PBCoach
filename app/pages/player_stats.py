import reflex as rx
from app.components.extra import page_loading, page_title
from app.states.overview import OverviewState
from app.states.player_stats import PlayerState
from app.templates import template


@template(
    route="/[match_id]/player/[player_id]",
    title="Statistiche Team",
    on_load=[OverviewState.on_load, PlayerState.on_load],
)
def team_page() -> rx.Component:
    page = rx.vstack(
        rx.cond(
            PlayerState.is_sidebar_open,
            page_title("user", f"Statisiche di {PlayerState.player_name}"),
            page_title(
                "user",
                f"Statisiche di {PlayerState.player_name} • {PlayerState.match_name}",
            ),
        ),
        rx.badge(rx.text("Coming soon!", size="4"), size="3"),
        spacing="5",
        width="100%",
    )
    return rx.cond(PlayerState.match_players, page, page_loading())
