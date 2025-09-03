import reflex as rx
from app.components.player import player_item_small


def match_title(partita, title_size="8", **attributes):
    def tag_badge(text):
        return rx.badge(text, color_scheme="gray")

    return rx.vstack(
        rx.text(partita.name, size=title_size, weight="bold", align="center"),
        rx.text(partita.date_str, color_scheme="gray", align="center"),
        rx.hstack(
            tag_badge(partita.type),
            tag_badge(partita.location),
            rx.cond(partita.location_court, tag_badge(partita.location_court)),
            tag_badge(partita.location_type),
            rx.cond(partita.location_type == "Outdoor", tag_badge(partita.weather)),
            align="center",
            justify="center",
            width="100%",
            wrap="wrap",
        ),
        width="100%",
        align="center",
        **attributes,
    )


def match_score(partita, active: str = "", **attributes):
    def player_elem(index) -> rx.Component:
        name = partita.players[index]
        player_id = partita.players_ids[index]
        return rx.box(
            player_item_small(player_id, name),
            padding="0.2em 0.4em",
            border_radius="2em",
            bg=rx.cond(
                partita.players_ids_str[index] == active, rx.color("gray", 4), None
            ),
        )

    trophy_badge = rx.badge(
        rx.icon("trophy", size=18), color_scheme="amber", radius="full", size="2"
    )
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.foreach(partita.team1_idx, player_elem),
                    spacing="0",
                    width="100%",
                    align="center",
                    justify="start",
                    wrap="wrap",
                ),
                rx.hstack(
                    rx.cond(partita.win_team1, trophy_badge),
                    rx.text(
                        partita.score[0],
                        size="6",
                        weight=rx.cond(partita.win_team1, "bold", "normal"),
                    ),
                    align="center",
                    spacing="2",
                ),
                align="center",
                width="100%",
                justify="between",
            ),
            rx.divider(),
            rx.hstack(
                rx.hstack(
                    rx.foreach(partita.team2_idx, player_elem),
                    spacing="0",
                    width="100%",
                    align="center",
                    justify="start",
                    wrap="wrap",
                ),
                rx.hstack(
                    rx.cond(partita.win_team2, trophy_badge),
                    rx.text(
                        partita.score[1],
                        size="6",
                        weight=rx.cond(partita.win_team2, "bold", "normal"),
                    ),
                    align="center",
                    spacing="2",
                ),
                align="center",
                width="100%",
                justify="between",
            ),
            width="100%",
        ),
        width="100%",
        **attributes,
    )
