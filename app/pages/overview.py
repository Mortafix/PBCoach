import reflex as rx
from app.components.cards import card
from app.components.extra import page_loading, page_title
from app.components.player import player_item
from app.database.data import color_quality, shots_name_italian
from app.states.overview import OverviewState
from app.templates import template


def player_elem(index, full_index=True) -> rx.Component:
    name = OverviewState.match.players[index]
    player_id = OverviewState.match.players_ids[index]
    return player_item(player_id, name)


def info_item(name, icon, value) -> rx.Component:
    return rx.vstack(
        rx.hstack(rx.icon(icon), rx.text(name), align="center", opacity=0.75),
        rx.text(value, size="8"),
        align="center",
    )


def stat_item(name, icon, value) -> rx.Component:
    return rx.vstack(
        rx.hstack(rx.icon(icon), rx.text(name), align="center", opacity=0.75),
        rx.text(value, size="8"),
        align="center",
    )


def achiever_item(title, achiever, description) -> rx.Component:
    player_idx, value = achiever[0], achiever[1]
    return rx.vstack(
        rx.badge(
            rx.text(title, size="6"),
            color_scheme="gray",
            variant="soft",
            high_contrast=True,
            size="3",
        ),
        player_elem(player_idx),
        rx.hstack(
            rx.text(value, size="8"),
            rx.text(description, color_scheme="gray"),
            spacing="1",
            align="baseline",
        ),
        spacing="4",
        align="center",
    )


def quality_item(data, player_index):
    def quality_element(text, value):
        return rx.hstack(
            rx.text(text, color_scheme="gray"),
            value,
            align="center",
            justify="between",
            width="100%",
        )

    element = rx.vstack(
        player_elem(player_index),
        rx.progress(
            value=data[0],
            size="3",
            variant="soft",
            color_scheme=color_quality(data[0]),
        ),
        quality_element(
            "Qualità",
            rx.badge(f"{data[0]}%", color_scheme=color_quality(data[0]), size="3"),
        ),
        quality_element(
            "Migliore",
            rx.badge(shots_name_italian(data[2]), color_scheme="gray", size="3"),
        ),
        quality_element(
            "Peggiore",
            rx.badge(shots_name_italian(data[1]), color_scheme="gray", size="3"),
        ),
        spacing="2",
        align="center",
        min_width="20%",
    )
    return rx.cond(data[0] > 0, element, None)


@template(
    route="/[match_id]/overview",
    title="Home",
    on_load=OverviewState.on_load,
)
def home_page() -> rx.Component:
    page = rx.vstack(
        rx.cond(
            OverviewState.is_sidebar_open,
            page_title("medal", "Riepilogo"),
            page_title("medal", f"Riepilogo • {OverviewState.match.name}"),
        ),
        card(
            rx.flex(
                rx.flex(
                    rx.foreach(OverviewState.match.team1_idx, player_elem),
                    align="center",
                    spacing="3",
                    flex_direction=["row", "row", "column"],
                ),
                rx.hstack(
                    rx.cond(
                        OverviewState.match.win_team1,
                        rx.icon("trophy", size=30, color=rx.color("amber", 9)),
                    ),
                    rx.text(OverviewState.match.score[0], size="9", weigth="bold"),
                    rx.text("-", size="8", weigth="bold", opacity=0.5),
                    rx.text(OverviewState.match.score[1], size="9", weigth="bold"),
                    rx.cond(
                        ~OverviewState.match.win_team1,
                        rx.icon("trophy", size=30, color=rx.color("amber", 9)),
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.flex(
                    rx.foreach(OverviewState.match.team2_idx, player_elem),
                    align="center",
                    spacing="3",
                    flex_direction=["row", "row", "column"],
                ),
                spacing="4",
                flex_direction=["column", "column", "row"],
                width="100%",
                align="center",
                justify="between",
                wrap="wrap",
            ),
            width="100%",
        ),
        card(
            rx.hstack(
                info_item("Tipo", "biceps-flexed", OverviewState.match.type),
                info_item("Location", "map-pin", OverviewState.match.location),
                info_item("Campo", "warehouse", OverviewState.match.location_type),
                rx.cond(
                    OverviewState.match.location_type == "Outdoor",
                    info_item("Meteo", "cloud-sun", OverviewState.match.weather),
                ),
                align="center",
                justify="between",
                width="100%",
                wrap="wrap",
            ),
            width="100%",
        ),
        card(
            rx.hstack(
                stat_item("Rally totali", "circle-plus", OverviewState.rally_total),
                stat_item("Rally in Kitchen", "chef-hat", OverviewState.rally_kitchen),
                stat_item("Media colpi", "sigma", OverviewState.rally_avg),
                stat_item("Rally più lungo", "maximize-2", OverviewState.rally_longest),
                align="center",
                justify="between",
                width="100%",
                wrap="wrap",
            ),
            width="100%",
        ),
        card(
            rx.hstack(
                rx.foreach(OverviewState.players_quality, quality_item),
                align="center",
                justify="between",
                width="100%",
            ),
            width="100%",
        ),
        card(
            rx.hstack(
                achiever_item("RUNNER", OverviewState.top_runner, "m percorsi"),
                achiever_item(
                    "MISTER QUALITÀ", OverviewState.top_quality, "% colpi ottimi"
                ),
                achiever_item("TUTTE MIE", OverviewState.top_shooter, " colpi"),
                achiever_item("FATALITY", OverviewState.top_finisher, " colpi finali"),
                achiever_item(
                    "SARÀ PER LA PROSSIMA",
                    OverviewState.wrost_misser,
                    "% errori",
                ),
                align="center",
                justify_content=["center", "center", "center", "space-between"],
                gap=["4rem", "4rem", "4rem", 0],
                width="100%",
                wrap="wrap",
            ),
            width="100%",
        ),
        spacing="5",
        width="100%",
    )
    return rx.cond(OverviewState.match, page, page_loading())
