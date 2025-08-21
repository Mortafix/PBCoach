import reflex as rx
from app.components.cards import card
from app.components.extra import page_title
from app.components.input import btn_icon
from app.database.data import color_quality
from app.database.players import Player
from app.states.players import PlayersState
from app.templates import template


def player_item(giocatore: Player):
    def element_item(text, value=None, content=None, color="gray"):
        return (
            rx.hstack(
                rx.text(text, size="5"),
                rx.cond(
                    value is not None,
                    rx.code(value, size="5", color_scheme=color),
                    content,
                ),
                align="center",
                justify="between",
                width="100%",
            ),
        )

    def chart_trend():
        return rx.recharts.line_chart(
            rx.recharts.line(
                data_key="y",
                stroke=rx.color(trend_color, 9),
                stroke_width=3,
                dot=False,
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="x", hide=True),
            rx.recharts.y_axis(hide=True),
            data=PlayersState.players_quality_chart_data.get(giocatore.id, []),
            width="100%",
            height=50,
            margin={
                "top": 10,
                "right": 0,
                "left": 20,
                "bottom": -30,
            },
        )

    partite_giocate = PlayersState.players_played.get(giocatore.id, 0)
    quality = PlayersState.players_quality.get(giocatore.id, 0)
    quality_history = PlayersState.players_quality_history.get(giocatore.id, [])
    trend_color = rx.cond(quality_history[0] > quality_history[-1], "red", "green")
    trend_icon = rx.cond(
        quality_history[0] > quality_history[-1], "trending-down", "trending-up"
    )
    return card(
        rx.vstack(
            rx.code(giocatore.short_name, size="7"),
            rx.avatar(
                src=f"/players/{giocatore.id}.jpg",
                radius="full",
                fallback=giocatore.name[:2],
                border="4px solid white",
                size="8",
            ),
            rx.cond(
                partite_giocate,
                rx.vstack(
                    element_item("Partite", partite_giocate),
                    element_item(
                        "Qualità",
                        content=rx.hstack(
                            rx.code(
                                f"{quality}%",
                                size="5",
                                color_scheme=color_quality(quality),
                            ),
                            rx.cond(
                                partite_giocate > 1,
                                rx.code(rx.icon(trend_icon), color_scheme=trend_color),
                            ),
                            align="center",
                        ),
                    ),
                    rx.cond(
                        partite_giocate > 1,
                        element_item("Trend", content=chart_trend()),
                        None,
                    ),
                    spacing="2",
                    width="100%",
                ),
                element_item("Partite", partite_giocate),
            ),
            spacing="4",
            width="100%",
            align="center",
            justify="center",
        ),
        flex=["100%", "100%", "45%", "30%", "20%", "17%"],
        cursor="pointer",
        max_width="28rem",
        border="2px solid transparent",
        _hover={"border": "2px solid", "border-color": rx.color("amber", 9)},
        on_click=rx.redirect(f"/player/{giocatore.id}"),
    )


@template(
    route="/players",
    title="Giocatori",
    on_load=PlayersState.on_load,
    meta=[
        {"property": "og:title", "content": "Giocatori del Coach Dinky"},
        {"property": "og:description", "content": "Tutti i giocatori del Coach Dinky"},
    ],
)
def matches_page() -> rx.Component:
    return rx.vstack(
        page_title("users", "Giocatori"),
        rx.hstack(
            rx.icon("search", size=28, stroke_width=1.5),
            rx.input(
                placeholder="Cerca...",
                on_change=PlayersState.search.debounce(300),
                size="3",
                width="100%",
                value=PlayersState.search_text,
            ),
            rx.cond(
                PlayersState.is_search_active,
                btn_icon(
                    "x",
                    color_scheme="red",
                    variant="soft",
                    on_click=PlayersState.reset_search,
                ),
            ),
            width="100%",
            align="center",
            spacing="2",
        ),
        rx.hstack(
            rx.foreach(PlayersState.players, player_item),
            align="center",
            width="100%",
            justify_content="space-evenly",
            wrap="wrap",
        ),
        spacing="4",
        width="100%",
    )
