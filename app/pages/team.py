import reflex as rx
from app.components.cards import card
from app.components.charts import base_pie_chart
from app.components.extra import page_title
from app.components.player import player_item
from app.components.shots import custom_item, deep_item, quality_item
from app.database.data import color_quality
from app.pages.extra import match_not_found
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
            wrap="wrap",
        ),
        rx.divider(),
        rx.hstack(
            rx.text("Distanza totale percorsa"),
            rx.text(rx.text.strong(distance), "m", size="6"),
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
            custom_item(text, value, elem_type="quality", scale=scale),
            width="100%",
        )

    player_id = TeamState.match.players_ids[player_index]
    name = TeamState.match.players[player_index]
    return rx.vstack(
        rx.hstack(player_item(player_id, name), width="100%", justify="center"),
        element("Servizio", serves_data[index], [40, 50, 70]),
        element("Risposta", returns_data[index], [90, 92.5, 96]),
        width="100%",
        flex="1 1 45%",
    )


def shots_item(team_idx, shots, left_side) -> rx.Component:
    return rx.hstack(
        base_pie_chart("flame", "Tiri totali", shots),
        base_pie_chart("circle-arrow-left", "Lato sinistro", left_side, ": %"),
        width="100%",
        wrap="wrap",
    )


def serves_returns_item(team_idx, serves, returns) -> rx.Component:
    def player_team(player_index):
        player_id = TeamState.match.players_ids[player_index]
        name = TeamState.match.players[player_index]
        return player_item(player_id, name)

    return rx.vstack(
        rx.hstack(
            rx.foreach(team_idx, player_team),
            justify="center",
            width="100%",
            spacing="7",
            wrap="wrap",
        ),
        rx.divider(margin_bottom="0.25rem"),
        rx.hstack(
            rx.vstack(
                base_pie_chart("arrow-up-from-line", "Servizi", serves[0], ": %"),
                quality_item("Qualità", serves[1]),
                deep_item("Profondità", serves[2]),
                width="100%",
                flex="1 1 45%",
            ),
            rx.vstack(
                base_pie_chart("arrow-down-from-line", "Risposte", returns[0], ": %"),
                quality_item("Qualità", returns[1]),
                deep_item("Profondità", returns[2]),
                width="100%",
                flex="1 1 45%",
            ),
            spacing="6",
            width="100%",
            wrap="wrap",
        ),
        width="100%",
    )


def thirds_item(team_idx, thirds_data, thirds_quality) -> rx.Component:
    def player_team(player_index):
        player_id = TeamState.match.players_ids[player_index]
        name = TeamState.match.players[player_index]
        return player_item(player_id, name)

    return rx.vstack(
        rx.hstack(
            rx.foreach(team_idx, player_team),
            justify="center",
            width="100%",
            spacing="7",
            wrap="wrap",
        ),
        rx.divider(margin_bottom="0.25rem"),
        rx.vstack(
            base_pie_chart("dice-3", "Terzo colpo", thirds_data),
            rx.cond(
                thirds_quality[0] != 0, quality_item("Qualità Drive", thirds_quality[0])
            ),
            rx.cond(
                thirds_quality[1] != 0, quality_item("Qualità Drop", thirds_quality[1])
            ),
            rx.cond(
                thirds_quality[2] != 0,
                quality_item("Qualità Pallonetto", thirds_quality[2]),
            ),
            width="100%",
        ),
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
                flex="1 1 49%",
            ),
            card(
                kitchen_item(
                    TeamState.match.team2_idx,
                    TeamState.team2_serving,
                    TeamState.team2_receiving,
                    TeamState.team2_distance,
                ),
                width="100%",
                flex="1 1 49%",
            ),
            width="100%",
            wrap="wrap",
        ),
        rx.cond(
            TeamState.match.is_double,
            rx.hstack(
                card(
                    shots_item(
                        TeamState.match.team1_idx,
                        TeamState.team1_shots,
                        TeamState.team1_left_side,
                    ),
                    width="100%",
                    flex="1 1 49%",
                ),
                card(
                    shots_item(
                        TeamState.match.team2_idx,
                        TeamState.team2_shots,
                        TeamState.team2_left_side,
                    ),
                    width="100%",
                    flex="1 1 49%",
                ),
                width="100%",
                wrap="wrap",
            ),
        ),
        rx.hstack(
            card(
                serves_returns_item(
                    TeamState.match.team1_idx,
                    TeamState.team1_serves,
                    TeamState.team1_returns,
                ),
                width="100%",
                flex="1 1 49%",
            ),
            card(
                serves_returns_item(
                    TeamState.match.team2_idx,
                    TeamState.team2_serves,
                    TeamState.team2_returns,
                ),
                width="100%",
                flex="1 1 49%",
            ),
            width="100%",
            wrap="wrap",
        ),
        rx.hstack(
            card(
                thirds_item(
                    TeamState.match.team1_idx,
                    TeamState.team1_thirds_pie,
                    TeamState.team1_thirds_quality,
                ),
                width="100%",
                flex="1 1 49%",
            ),
            card(
                thirds_item(
                    TeamState.match.team2_idx,
                    TeamState.team2_thirds_pie,
                    TeamState.team2_thirds_quality,
                ),
                width="100%",
                flex="1 1 49%",
            ),
            width="100%",
            wrap="wrap",
        ),
        spacing="5",
        width="100%",
    )
    return rx.cond(OverviewState.is_match_found, page, match_not_found())
