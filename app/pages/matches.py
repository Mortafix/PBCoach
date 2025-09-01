import reflex as rx
from app.components.cards import card
from app.components.chips import chips
from app.components.expanders import expander
from app.components.extra import page_title
from app.components.input import btn_text_icon
from app.components.player import player_item
from app.database.matches import Partita
from app.states.matches import MatchesState
from app.templates import template


def match_item(partita: Partita):
    def player_elem(index) -> rx.Component:
        name = partita.players[index]
        player_id = partita.players_ids[index]
        return player_item(player_id, name)

    return card(
        rx.vstack(
            rx.text(partita.name, size="8", weight="bold", align="center"),
            rx.text(partita.date_str, color_scheme="gray", align="center"),
            rx.hstack(
                rx.badge(partita.type, color_scheme="gray"),
                rx.badge(partita.location, color_scheme="gray"),
                rx.cond(
                    partita.location_court,
                    rx.badge(partita.location_court, color_scheme="gray"),
                ),
                rx.badge(partita.location_type, color_scheme="gray"),
                rx.cond(
                    partita.location_type == "Outdoor",
                    rx.badge(partita.weather, color_scheme="gray"),
                ),
                align="center",
                justify="center",
                width="100%",
                wrap="wrap",
            ),
            rx.divider(),
            rx.hstack(
                rx.foreach(partita.team1_idx, player_elem),
                width="100%",
                align="center",
                justify="center",
                spacing="4",
            ),
            rx.hstack(
                rx.cond(
                    partita.win_team1,
                    rx.icon("trophy", size=24, color=rx.color("amber", 9)),
                ),
                rx.text(partita.score[0], size="8", weigth="bold"),
                rx.text("-", size="8", weigth="bold", opacity=0.5),
                rx.text(partita.score[1], size="8", weigth="bold"),
                rx.cond(
                    partita.win_team2,
                    rx.icon("trophy", size=24, color=rx.color("amber", 9)),
                ),
                spacing="3",
                align="center",
            ),
            rx.hstack(
                rx.foreach(partita.team2_idx, player_elem),
                width="100%",
                align="center",
                justify="center",
                spacing="4",
            ),
            align="center",
            justify="center",
            width="100%",
        ),
        flex=["100%", "100%", "48%", "48%", "30%", "25%"],
        border="2px solid transparent",
        cursor="pointer",
        _hover={"border": "2px solid", "border-color": rx.color("amber", 9)},
        on_click=rx.redirect(f"/match/{partita.code}/overview"),
    )


def filters_block(state) -> rx.Component:
    def filter_item(icon, title, content) -> rx.Component:
        return rx.vstack(
            rx.hstack(
                rx.icon(icon, color="gray", size=18),
                rx.text(title, color_scheme="gray", size="3"),
                spacing="2",
                align="center",
            ),
            content,
            width="100%",
            spacing="2",
        )

    return rx.vstack(
        filter_item(
            "map-pinned", "Location", chips(state, state.locations, "location")
        ),
        filter_item(
            "tree-pine",
            "Tipo di campo",
            chips(state, {"Indoor": "Indoor", "Outdoor": "Outdoor"}, "field"),
        ),
        filter_item(
            "trophy",
            "Tipo di partita",
            chips(
                state,
                {
                    "Allenamento": "Allenamento",
                    "Amichevole": "Amichevole",
                    "Torneo for fun": "Torneo for fun",
                    "Torneo 3.5": "Torneo 3.5",
                    "Torneo 4.0": "Torneo 4.0",
                    "Torneo open": "Torneo open",
                    "Torneo agonistico": "Torneo agonistico",
                },
                "type",
            ),
        ),
        filter_item(
            "user-search",
            "Mopdalità di Gioco",
            chips(state, {2: "Singolo", 4: "Doppio"}, "mode"),
        ),
        filter_item("users", "Giocatori", chips(state, state.players, "players")),
        filter_item(
            "calendar", "Data della partita", chips(state, state.months, "months")
        ),
        spacing="5",
        width="100%",
    )


@template(
    route="/matches",
    title="Partite",
    on_load=MatchesState.on_load,
    meta=[
        {"property": "og:title", "content": "Partite del Coach Dinky"},
        {
            "property": "og:description",
            "content": "Tutte le partite analizzate dal Coach Dinky",
        },
    ],
)
def matches_page() -> rx.Component:
    return rx.vstack(
        page_title("medal", "Partite"),
        expander(
            rx.hstack(
                rx.icon("sliders-horizontal"),
                rx.text("Filtri"),
                rx.cond(
                    MatchesState.are_filters_set,
                    btn_text_icon(
                        "x",
                        "Rimuovi Filtri",
                        text_size="2",
                        spacing="1",
                        variant="soft",
                        color_scheme="red",
                        on_click=MatchesState.reset_filters,
                    ),
                ),
                align="center",
            ),
            filters_block(MatchesState),
            width="100%",
            padding_inline="1rem",
        ),
        rx.hstack(
            rx.foreach(MatchesState.matches, match_item),
            align="center",
            width="100%",
            justify_content="space-evenly",
            wrap="wrap",
        ),
        spacing="5",
        width="100%",
    )
