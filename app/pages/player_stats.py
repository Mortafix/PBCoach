import reflex as rx
from app.components.cards import card
from app.components.charts import base_pie_chart
from app.components.extra import page_loading, page_title
from app.components.shots import (base_item, deep_item, height_item,
                                  quality_item, velocity_item)
from app.database.data import color_quality
from app.pages.overview import info_item
from app.states.overview import OverviewState
from app.states.player_stats import PlayerState, Shot
from app.templates import template


def single_shot_item(icon, title, shot: Shot) -> rx.Component:
    return rx.vstack(
        base_pie_chart(icon, title, shot.pie_inout, ": %"),
        quality_item("Qualità", shot.quality),
        velocity_item("Velocità media", shot.speed),
        deep_item("Profondità", shot.baseline_distance),
        width="100%",
        flex="1 1 45%",
    )


def multiple_shot_item(icon, title, data, shots: list[Shot]) -> rx.Component:
    def shot_element(shot: Shot):
        el = quality_item(f"Qualità {shot.name}", shot.quality)
        return rx.cond(shot.count > 0, el, None)

    return rx.vstack(
        base_pie_chart(icon, title, data),
        rx.foreach(shots, shot_element),
        width="100%",
        flex="1 1 45%",
    )


def shot_select(shot: Shot) -> rx.Component:
    qual_shot_color = color_quality(shot.quality)
    btn = rx.button(
        rx.hstack(
            shot.name,
            rx.icon(
                "dot",
                size=50,
                color=rx.color(qual_shot_color, 9),
                margin_inline="-1rem",
            ),
            spacing="0",
            align="center",
        ),
        variant="soft",
        color_scheme="gray",
        cursor="pointer",
        on_click=PlayerState.change_shot(shot),
    )
    return rx.cond(shot.count > 0, btn, None)


def info_element(shot: Shot) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("chart-area", size=24),
            rx.text("Analisi ", rx.code(shot.name, color_scheme="gray"), size="6"),
            align="center",
            spacing="2",
        ),
        rx.hstack(
            base_pie_chart(data=shot.pie_inout, fmt=": %"),
            rx.vstack(
                base_item("Colpi totali", shot.count),
                quality_item("Qualità", shot.quality),
                deep_item(
                    "Profondità", shot.baseline_distance, reverse=shot.is_reverse_deep
                ),
                height_item("Altezza", shot.net_height),
                velocity_item("Velocità media", shot.speed),
                velocity_item("Velocità massima", shot.fastest, with_color=False),
            ),
            justify_content="space-evenly",
            width="100%",
        ),
        width="100%",
    )


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
        rx.hstack(
            card(
                rx.hstack(
                    single_shot_item(
                        "arrow-up-from-line", "Servizi", PlayerState.serves
                    ),
                    single_shot_item(
                        "arrow-down-from-line", "Risposte", PlayerState.returns
                    ),
                    spacing="5",
                    align="center",
                    justify="between",
                    width="100%",
                    wrap="wrap",
                ),
                width="100%",
            ),
            card(
                rx.hstack(
                    multiple_shot_item(
                        "dice-3",
                        "Terzo colpo",
                        PlayerState.thirds,
                        [
                            PlayerState.third_drives,
                            PlayerState.third_drops,
                            PlayerState.third_lobs,
                        ],
                    ),
                    multiple_shot_item(
                        "flame",
                        "Colpi",
                        PlayerState.hands,
                        [PlayerState.forehands, PlayerState.backhands],
                    ),
                    spacing="5",
                    align="start",
                    justify="between",
                    width="100%",
                    wrap="wrap",
                ),
                width="100%",
            ),
            width="100%",
        ),
        card(
            rx.vstack(
                rx.hstack(
                    rx.foreach(PlayerState.info_shots, shot_select),
                    width="100%",
                    wrap="wrap",
                    align="center",
                ),
                rx.hstack(
                    rx.text("Colpi ", rx.text.strong("non"), " eseguiti: "),
                    rx.foreach(
                        PlayerState.zero_shots,
                        lambda shot: rx.badge(shot.name, color_scheme="gray"),
                    ),
                    spacing="1",
                    align="center",
                ),
                rx.cond(
                    PlayerState.current_shot,
                    rx.vstack(
                        rx.divider(),
                        info_element(PlayerState.current_shot),
                        width="100%",
                    ),
                ),
                width="100%",
            ),
            width="100%",
        ),
        spacing="5",
        width="100%",
    )
    return rx.cond(PlayerState.match, page, page_loading())
