import reflex as rx
from app.components.cards import card
from app.components.extra import page_loading, page_title
from app.components.player import player_item
from app.database.data import color_quality
from app.states.overview import OverviewState
from app.states.team import TeamState
from app.templates import template


def kitchen_item(team_idx, serving, receiving, distance) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.badge(
                rx.icon("chef-hat", size=24),
                rx.text("Arrivo in Kitchen", size="6"),
                color_scheme="gray",
                size="3",
            ),
            width="100%",
            align="center",
            justify="center",
        ),
        rx.hstack(
            rx.foreach(
                team_idx,
                lambda el, idx: kitchen_player_item(
                    el,
                    idx,
                    serving,
                    receiving,
                ),
            ),
            spacing="7",
            width="100%",
            justify=rx.cond(TeamState.match.is_double, "between", "center"),
        ),
        rx.divider(),
        rx.hstack(
            rx.text("Distanza totale percorsa"),
            rx.text(
                rx.text.strong(distance),
                "m",
                size="6",
            ),
            width="100%",
            justify="between",
        ),
        width="100%",
    )


def kitchen_player_item(player_index, index, serves_data, returns_data) -> rx.Component:
    def element(text, value, scale):
        color = color_quality(value, scale=scale)
        return rx.vstack(
            rx.progress(value=value, size="3", variant="soft", color_scheme=color),
            rx.hstack(
                rx.text(text, color_scheme="gray"),
                rx.badge(f"{value}%", color_scheme=color, size="3"),
                align="center",
                justify="between",
                width="100%",
            ),
            width="100%",
        )

    player_id = TeamState.match.players_ids[player_index]
    name = TeamState.match.players[player_index]
    return rx.vstack(
        rx.hstack(player_item(player_id, name), width="100%", justify="center"),
        element("Servizio", serves_data[index], [40, 50, 70]),
        element("Risposta", returns_data[index], [90, 92.5, 96]),
        width="100%",
    )


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
            page_title("users", f"Statisiche del Team • {TeamState.match.name}"),
        ),
        rx.hstack(
            card(
                kitchen_item(
                    TeamState.match.team1_idx,
                    TeamState.team1_serving,
                    TeamState.team1_receiving,
                    TeamState.team1_distance,
                ),
                width="100%",
            ),
            card(
                kitchen_item(
                    TeamState.match.team2_idx,
                    TeamState.team2_serving,
                    TeamState.team2_receiving,
                    TeamState.team2_distance,
                ),
                width="100%",
            ),
            width="100%",
        ),
        spacing="5",
        width="100%",
    )
    return rx.cond(TeamState.match, page, page_loading())
