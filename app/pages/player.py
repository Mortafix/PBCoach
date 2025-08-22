import reflex as rx
from app.components.cards import card
from app.components.charts import (accuracy_area_chart, base_pie_chart,
                                   quality_area_chart)
from app.components.extra import page_loading
from app.components.player import player_item
from app.states.player_page import PlayerState
from app.templates import template

# ---- UI


def badge_title(icon, title, **attributes):
    return rx.badge(
        rx.icon(icon or "star", size=20),
        rx.text(title, size="4"),
        color_scheme="gray",
        size="3",
        **attributes,
    )


def info_field(text, value, fmt="", is_content=False):
    return rx.hstack(
        rx.text(text),
        rx.cond(is_content, value, rx.code(f"{value}{fmt}", color_scheme="gray")),
        width="100%",
        align="center",
        justify="between",
    )


def render_type_badge(player_type):
    def badge(color):
        return rx.badge(rx.text(player_type, size="5"), color_scheme=color, size="3")

    return (
        rx.match(
            player_type,
            ("Bilanciato", badge("purple")),
            ("Aggressivo", badge("indigo")),
            ("Bilanciato", badge("crimson")),
        ),
    )


def render_teammate(player):
    return rx.hstack(
        player_item(player[0], PlayerState.player.teammates_name.get(player[0])),
        rx.text(
            rx.code(player[1], color_scheme="gray"),
            rx.cond(player[1] > 1, " partite", " partita"),
        ),
        width="100%",
        align="center",
        justify="between",
    )


@template(
    route="/player/[player_id]",
    title="Pagina giocatore",
    description="Analisi del Coach Dinky di un giocatore",
    on_load=PlayerState.on_load,
)
def players_selection() -> rx.Component:
    player = PlayerState.player
    page = rx.vstack(
        card(
            rx.hstack(
                rx.vstack(
                    rx.avatar(
                        src=f"/players/{PlayerState.player_id}.jpg",
                        radius="full",
                        fallback=PlayerState.player_name[:2],
                        border="3px solid white",
                        size="8",
                    ),
                    rx.badge(rx.text(PlayerState.player_name, size="6")),
                    spacing="5",
                    align="center",
                    width="100%",
                    flex="1 1 45%",
                ),
                rx.vstack(
                    info_field("Partite giocate", player.matches),
                    info_field("Allenamenti", player.allenamenti),
                    info_field("Distanza", player.distance_str),
                    info_field(
                        "Tipo di giocatore",
                        render_type_badge(player.player_type),
                        is_content=True,
                    ),
                    spacing="4",
                    width="100%",
                    flex="1 1 45%",
                ),
                spacing="7",
                width="100%",
                justify_content="space-evenly",
                wrap="wrap",
            ),
            width="100%",
            max_width="60rem",
            margin_inline="auto",
        ),
        card(
            rx.vstack(
                rx.hstack(
                    rx.hstack(
                        base_pie_chart("trophy", "Partite", player.pie_matches),
                        base_pie_chart("arrow-right-left", "Rally", player.pie_rallies),
                        flex="1 1 64%",
                        justify_content="space-evenly",
                        wrap="wrap",
                    ),
                    rx.vstack(
                        badge_title("users", "Compagni", margin_bottom="1em"),
                        rx.foreach(player.teammates, render_teammate),
                        flex="1 1 31%",
                        spacing="5",
                        align="center",
                    ),
                    align="center",
                    width="100%",
                    justify_content="space-evenly",
                    wrap="wrap",
                ),
                rx.hstack(
                    base_pie_chart("scale", "Tipo dei tiri", player.pie_shots_type),
                    base_pie_chart("flame", "Tiri", player.pie_shots, size=300),
                    width="100%",
                    align="center",
                    justify_content="space-evenly",
                    wrap="wrap",
                ),
                width="100%",
                spacing="7",
            ),
            width="100%",
        ),
        rx.cond(
            player.matches > 1,
            card(
                rx.hstack(
                    quality_area_chart(
                        "shield-check", "Qualità", player.area_quality, PlayerState
                    ),
                    accuracy_area_chart(
                        "target", "Accuratezza", player.area_accuracy, PlayerState
                    ),
                    width="100%",
                    align="center",
                    justify_content="space-evenly",
                    wrap="wrap",
                ),
                width="100%",
            ),
        ),
        spacing="5",
        width="100%",
    )
    return rx.cond(player, page, page_loading())
