import reflex as rx
from app.components.cards import card
from app.components.charts import base_pie_chart
from app.components.extra import page_loading, page_title
from app.pages.overview import info_item
from app.states.overview import OverviewState
from app.states.player_stats import PlayerState
from app.templates import template


def serves_item(data) -> rx.Component:
    return rx.vstack(base_pie_chart("apple", "Servizi", data), width="100%")


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
                f"Statisiche di {PlayerState.player_name} • {PlayerState.match.name}",
            ),
        ),
        card(
            rx.hstack(
                info_item("Distanza", "unfold-vertical", PlayerState.distance, "m"),
                info_item(
                    "Tiri",
                    "flame",
                    PlayerState.shots,
                    f"di {PlayerState.shots_total}",
                    spacing="1",
                ),
                info_item("Qualità", "shield-check", PlayerState.quality, "%"),
                info_item("Errori", "circle-x", PlayerState.faults, "%"),
                spacing="5",
                align="center",
                justify_content="space-evenly",
                width="100%",
                wrap="wrap",
            ),
            width="100%",
        ),
        spacing="5",
        width="100%",
    )
    return rx.cond(PlayerState.match, page, page_loading())
