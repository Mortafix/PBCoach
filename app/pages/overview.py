import reflex as rx
from app.components.cards import card
from app.components.extra import page_loading
from app.states.overview import OverviewState
from app.templates import template


def player_item(index) -> rx.Component:
    name = OverviewState.match_players[index]
    return rx.hstack(
        rx.avatar(
            name,
            radius="full",
            fallback=name[:2],
            # color_scheme=rx.cond(opponent, "tomato", "indigo"),
            border="3px solid white",
            # border_color=rx.cond(
            #     opponent, rx.color("tomato", 6), rx.color("indigo", 6)
            # ),
        ),
        rx.cond(name, rx.text(name)),
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
        player_item(player_idx),
        rx.hstack(
            rx.text(value, size="8"),
            rx.text(description, color_scheme="gray"),
            spacing="1",
            align="baseline",
        ),
        spacing="4",
        align="center",
    )


@template(
    route="/[match_id]/overview",
    title="Home",
    on_load=OverviewState.on_load,
)
def home_page() -> rx.Component:
    page = rx.vstack(
        card(
            rx.flex(
                rx.flex(
                    rx.foreach(OverviewState.team1_idx, player_item),
                    align="center",
                    spacing="3",
                    flex_direction=["row", "row", "column"],
                ),
                rx.hstack(
                    rx.cond(
                        OverviewState.win_team1,
                        rx.icon("trophy", size=30, color=rx.color("amber", 9)),
                    ),
                    rx.text(OverviewState.score[0], size="9", weigth="bold"),
                    rx.text("-", size="8", weigth="bold", opacity=0.5),
                    rx.text(OverviewState.score[1], size="9", weigth="bold"),
                    rx.cond(
                        ~OverviewState.win_team1,
                        rx.icon("trophy", size=30, color=rx.color("amber", 9)),
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.flex(
                    rx.foreach(OverviewState.team2_idx, player_item),
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
                achiever_item("RUNNER", OverviewState.top_runner, "m percorsi"),
                achiever_item(
                    "MISTER QUALITÀ", OverviewState.top_quality, "% colpi ottimi"
                ),
                achiever_item("TUTTE MIE", OverviewState.top_shooter, " colpi"),
                achiever_item("FATALITY", OverviewState.top_finisher, " colpi finali"),
                achiever_item(
                    "SARÀ PER LA PROSSIMA",
                    OverviewState.wrost_misser,
                    "% colpi sbagliati",
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
    return rx.cond(OverviewState.match_players, page, page_loading())
