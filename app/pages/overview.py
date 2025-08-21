import reflex as rx
from app.components.cards import card
from app.components.extra import page_link, page_title
from app.components.player import player_item
from app.components.shots import base_item, quality_item
from app.database.data import color_quality, shots_name_italian
from app.pages.extra import match_not_found
from app.states.overview import OverviewState
from app.templates import template


def player_elem(index, full_index=False) -> rx.Component:
    name = rx.cond(
        full_index,
        OverviewState.match.players_full[index],
        OverviewState.match.players[index],
    )
    player_id = rx.cond(
        full_index,
        OverviewState.match.players_full_ids[index],
        OverviewState.match.players_ids[index],
    )
    return player_item(player_id, name)


def info_item(name, icon, value, add_info="", spacing="0") -> rx.Component:
    return rx.vstack(
        rx.hstack(rx.icon(icon), rx.text(name), align="center", opacity=0.75),
        rx.hstack(
            rx.text(value, size="8"),
            rx.text(add_info, color_scheme="gray", size="6"),
            align="end",
            spacing=spacing,
            text_align="center",
        ),
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
        player_elem(player_idx, full_index=True),
        rx.hstack(
            rx.text(value, size="8"),
            rx.text(description, color_scheme="gray"),
            spacing="1",
            align="baseline",
        ),
        spacing="4",
        align="center",
    )


def player_quality(data, player_index):
    element = rx.vstack(
        player_elem(player_index, full_index=True),
        rx.progress(
            value=data[0],
            size="3",
            variant="soft",
            color_scheme=color_quality(data[0]),
        ),
        quality_item("Qualità", data[0]),
        base_item("Migliore", shots_name_italian(data[2])),
        base_item("Peggiore", shots_name_italian(data[1])),
        spacing="2",
        align="center",
        flex=["100%", "100%", "45%", "45%", "20%", "20%"],
    )
    return rx.cond(data[0] > 0, element, None)


@template(
    route="/match/[match_id]/overview",
    title="Match",
    description="Analisi del Coach Dinky della partita",
    on_load=OverviewState.on_load,
    # meta=[
    #     {"property": "og:title", "content": OverviewState.match.name},
    #     {"property": "og:description", "content": OverviewState.players_description},
    # ],
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
                        OverviewState.match.win_team2,
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
                spacing="5",
                align="center",
                justify_content="space-evenly",
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
                justify_content="space-evenly",
                width="100%",
                wrap="wrap",
            ),
            width="100%",
        ),
        card(
            rx.hstack(
                rx.foreach(OverviewState.players_quality, player_quality),
                spacing="8",
                align="center",
                justify_content="space-evenly",
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
        rx.divider(),
        rx.hstack(
            page_link("Statistiche dei Team", f"/match/{OverviewState.match_id}/team"),
            page_link(
                "Statistiche dei Giocatori", f"/match/{OverviewState.match_id}/players"
            ),
            page_link("Video della Partita", f"/match/{OverviewState.match_id}/video"),
            width="100%",
            wrap="wrap",
        ),
        spacing="5",
        width="100%",
    )
    return rx.cond(OverviewState.is_match_found, page, match_not_found())


# ---- REDIRECT | only code


class RedirectCodeState(rx.State):
    @rx.event
    def go_to_page(self):
        return rx.redirect(f"/match/{self.match_id}/overview")


@template(
    route="/match/[match_id]",
    on_load=RedirectCodeState.go_to_page,
    description="Analisi del Coach Dinky della partita",
    # meta=[
    #     {"property": "og:title", "content": OverviewState.match.name},
    #     {"property": "og:description", "content": OverviewState.players_description},
    # ],
)
def redirect_match_code():
    return rx.text("Redirecting...")
