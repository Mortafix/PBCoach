import reflex as rx
from app.components.cards import card
from app.components.extra import page_title
from app.database.matches import Partita
from app.states.matches import MatchesState
from app.templates import template


def match_item(partita: Partita):
    def player_item(index) -> rx.Component:
        name = partita.players[index]
        return rx.hstack(
            rx.avatar(name, radius="full", fallback=name[:2], border="3px solid white"),
            rx.cond(name, rx.text(name)),
            spacing="2",
            align="center",
        )

    return card(
        rx.vstack(
            rx.text(partita.name, size="8", weight="bold", align="center"),
            rx.text(partita.date_str, color_scheme="gray", align="center"),
            rx.hstack(
                rx.badge(partita.type, color_scheme="gray"),
                rx.badge(partita.location, color_scheme="gray"),
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
                rx.foreach(partita.team1_idx, player_item),
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
                    ~partita.win_team1,
                    rx.icon("trophy", size=24, color=rx.color("amber", 9)),
                ),
                spacing="3",
                align="center",
            ),
            rx.hstack(
                rx.foreach(partita.team2_idx, player_item),
                width="100%",
                align="center",
                justify="center",
                spacing="4",
            ),
            align="center",
            justify="center",
            width="100%",
        ),
        width="30%",
        border="2px solid transparent",
        cursor="pointer",
        _hover={"border": "2px solid", "border-color": rx.color("amber", 9)},
        on_click=rx.redirect(f"/{partita.code}/overview"),
    )


@template(
    route="/matches",
    title="Partite",
    on_load=MatchesState.on_load,
)
def matches_page() -> rx.Component:
    return rx.vstack(
        page_title("medal", "Partite"),
        rx.hstack(
            rx.foreach(MatchesState.matches, match_item),
            align="center",
            width="100%",
            wrap="wrap",
        ),
        spacing="5",
        width="100%",
    )
