import reflex as rx
from app.components.cards import card
from app.components.charts import (accuracy_area_chart, base_pie_chart,
                                   quality_area_chart)
from app.components.expanders import expander
from app.components.extra import page_loading
from app.components.input import btn_text_icon
from app.components.match import match_score, match_title
from app.components.player import gender_color, player_item
from app.states.player import PlayerState
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


def render_sel_event(event, index):
    return base_event(
        event, index, bg=rx.color("accent", 4), on_click=PlayerState.remove_event(index)
    )


def render_event(event, index):
    return base_event(
        event, index, bg=rx.color("gray", 4), on_click=PlayerState.add_event(index)
    )


def base_event(event, index, **attributes):
    return rx.hstack(
        rx.text.strong(event[0]),
        rx.hstack(
            rx.text(event[1][0].date_str_shortest, color_scheme="gray"),
            rx.cond(
                event[1][0].date_str_shortest != event[1][-1].date_str_shortest,
                rx.hstack(
                    rx.icon("move_right", color="gray"),
                    rx.text(event[1][-1].date_str_shortest, color_scheme="gray"),
                    align="center",
                    spacing="1",
                ),
            ),
            align="center",
            spacing="1",
        ),
        align="center",
        spacing="4",
        padding="0.5rem 1rem",
        cursor="pointer",
        border_radius="2rem",
        _hover={"opacity": 0.8},
        **attributes,
    )


def render_keyword(keyword):
    return rx.text(
        keyword,
        size="3",
        padding="0.2em 0.6em",
        border_radius="2em",
        bg=rx.color("gray", 3),
        cursor="pointer",
        on_click=lambda: PlayerState.set_event_search(keyword),
    )


def render_type_badge(player_type):
    def badge(color):
        return rx.badge(rx.text(player_type, size="5"), color_scheme=color, size="3")

    return (
        rx.match(
            player_type,
            ("Bilanciato", badge("purple")),
            ("Aggressivo", badge("indigo")),
            ("Difensivo", badge("crimson")),
        ),
    )


def render_teammate(player):
    return rx.hstack(
        rx.box(
            player_item(player[0], PlayerState.player.teammates_name.get(player[0])),
            on_click=rx.redirect(f"/player/{player[0]}"),
            cursor="pointer",
            padding="0.2em 0.5em",
            border_radius="1em",
            _hover={"bg": rx.color("gray", 3)},
        ),
        rx.text(
            rx.code(player[1], color_scheme="gray"),
            rx.cond(player[1] > 1, " partite", " partita"),
        ),
        width="100%",
        align="center",
        justify="between",
    )


def match_preview(partita):
    return card(
        rx.flex(
            match_title(
                partita,
                title_size="7",
                margin_right=[0, 0, "1.5em"],
                margin_bottom=["1.5em", "1.5em", 0],
            ),
            match_score(partita, active=PlayerState.player_id),
            flex_direction=["column", "column", "row"],
            align="center",
            justify="center",
            width="100%",
        ),
        width="100%",
        border="2px solid transparent",
        cursor="pointer",
        _hover={"border": "2px solid", "border-color": rx.color("amber", 9)},
        on_click=rx.redirect(f"/match/{partita.code}/overview"),
    )


# ---- PAGE


@template(
    route="/player/[player_id]",
    title="Pagina giocatore",
    description="Analisi del Coach Dinky di un giocatore",
    on_load=PlayerState.on_load,
)
def players_selection() -> rx.Component:
    player = PlayerState.player
    color = gender_color(PlayerState.player_gender)
    page = rx.vstack(
        rx.hstack(
            card(
                rx.hstack(
                    rx.vstack(
                        rx.avatar(
                            src=f"/players/{PlayerState.player_id}.jpg",
                            radius="full",
                            fallback=PlayerState.player_name[:2],
                            border="3px solid white",
                            size="8",
                            color_scheme=color,
                        ),
                        rx.badge(
                            rx.text(PlayerState.player_name, size="6"),
                            color_scheme=color,
                        ),
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
                min_width="18rem",
                flex="1 1 45%",
            ),
            card(
                rx.vstack(
                    rx.text("Filtra per Evento", size="6"),
                    rx.hstack(
                        rx.icon("search"),
                        rx.input(
                            placeholder="Cerca evento",
                            on_change=PlayerState.set_event_search,
                            value=PlayerState.event_search,
                            size="3",
                            width="100%",
                        ),
                        rx.cond(
                            PlayerState.events_selected,
                            btn_text_icon(
                                "circle-x",
                                "Rimuovi tutti",
                                variant="soft",
                                spacing="2",
                                color_scheme="red",
                                on_click=PlayerState.remove_all_events,
                            ),
                        ),
                        align="center",
                        width="100%",
                    ),
                    rx.cond(
                        ~PlayerState.event_search,
                        rx.hstack(
                            rx.foreach(PlayerState.keywords, render_keyword),
                            spacing="2",
                            align="center",
                            justify="center",
                            width="100%",
                            wrap="wrap",
                        ),
                    ),
                    rx.cond(
                        PlayerState.event_loading,
                        rx.hstack(
                            rx.spinner(size="3"),
                            rx.text("Ricerca in corso", color_scheme="gray"),
                            align="center",
                            spacing="2",
                        ),
                    ),
                    rx.vstack(
                        rx.foreach(PlayerState.events_selected, render_sel_event)
                    ),
                    rx.vstack(rx.foreach(PlayerState.events, render_event)),
                    width="100%",
                ),
                width="100%",
                flex="1 1 45%",
            ),
            width="100%",
            justify_content="space-evenly",
            wrap="wrap",
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
        expander(
            rx.hstack(
                rx.icon("trophy", size=28, stroke_width=2),
                rx.heading("Partite giocate", size="7"),
                align="center",
            ),
            rx.vstack(rx.foreach(PlayerState.matches, match_preview), width="100%"),
            size="3",
            width="100%",
        ),
        spacing="5",
        width="100%",
    )
    return rx.cond(player, page, page_loading())
