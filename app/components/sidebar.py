import reflex as rx
from app.styles import sidebar_close_width, sidebar_width


def sidebar_minimize(state) -> rx.Component:
    return rx.box(
        rx.button(
            rx.icon(rx.cond(state.is_sidebar_open, "chevron-left", "chevron-right")),
            color_scheme="gray",
            opacity=0.7,
            variant="ghost",
            cursor="pointer",
            size="1",
            padding="0.05rem",
            on_click=state.toggle_sidebar(),
        ),
        position="absolute",
        top=10,
        right=rx.cond(state.is_sidebar_open, 15, 25),
        padding=0,
    )


def sidebar_header(state) -> rx.Component:
    header = rx.vstack(
        rx.text(state.match.name, size="8", align="center"),
        rx.text(state.match.date_str, size="4", color_scheme="gray", align="center"),
        width="100%",
        align="center",
        justify="center",
        padding="0.35em",
        spacing="1",
    )
    return rx.cond(state.is_sidebar_open, header)


def sidebar_menu(state) -> rx.Component:
    match_id = getattr(state, "match_id", None)

    def nav_item(icon, text, href) -> rx.Component:
        is_active = rx.State.router.page.path.split("/")[-1] == href[1:]
        return rx.link(
            rx.hstack(
                rx.icon(icon, size=22, stroke_width=rx.cond(is_active, 2.5, 2)),
                rx.text(text, size="5", weight=rx.cond(is_active, "bold", "regular")),
                align="center",
            ),
            href=f"/match/{match_id}{href}",
            underline="none",
            color=rx.color("white", 7),
            padding="0.25em 0.7em",
            border_radius="1em",
            opacity=rx.cond(is_active, 1, 0.8),
            bg=rx.cond(is_active, rx.color("gray", 4), None),
            _hover={"bg": rx.color("gray", 5)},
        )

    def nav_item_icon(icon, href) -> rx.Component:
        is_active = rx.State.router.page.path.split("/")[-1] == href[1:]
        return rx.link(
            rx.icon(icon, size=22, stroke_width=rx.cond(is_active, 2.5, 2)),
            href=f"/match/{match_id}{href}",
            underline="none",
            color=rx.color("white", 7),
            padding="0.4em 0.4em",
            border_radius="1em",
            opacity=rx.cond(is_active, 1, 0.8),
            bg=rx.cond(is_active, rx.color("gray", 4), None),
            _hover={"bg": rx.color("gray", 5)},
        )

    menu_classic = rx.vstack(
        nav_item("home", "Riepilogo Partita", "/overview"),
        nav_item("users", "Statistiche Team", "/team"),
        rx.cond(
            state.match.video_id, nav_item("video", "Video Partita", "/video"), None
        ),
        spacing="1",
        width="100%",
        padding_left="1em",
    )

    menu_minimize = rx.vstack(
        nav_item_icon("home", "/overview"),
        nav_item_icon("users", "/team"),
        rx.cond(state.match.video_id, nav_item_icon("video", "/video"), None),
        spacing="1",
        width="100%",
        align="center",
        margin_top="1rem",
    )
    return rx.cond(state.is_sidebar_open, menu_classic, menu_minimize)


def sidebar_menu_players(state) -> rx.Component:
    def player_sidebar_item(name, idx, opponent=False, show_name=True) -> rx.Component:
        is_active = state.router.page.params.get("player_id").to(str) == idx.to_string()
        player_id = state.match.players_full_ids[idx]
        match_id = getattr(state, "match_id", None)
        return rx.link(
            rx.hstack(
                rx.avatar(
                    src=f"/players/{player_id}.jpg",
                    radius="full",
                    fallback=name[:2],
                    color_scheme=rx.cond(opponent, "tomato", "indigo"),
                    border="3px solid white",
                    border_color=rx.cond(
                        opponent, rx.color("tomato", 6), rx.color("indigo", 6)
                    ),
                ),
                rx.cond(
                    show_name,
                    rx.text(name, color_scheme=rx.cond(opponent, "tomato", "indigo")),
                ),
                align="center",
            ),
            href=f"/match/{match_id}/player/{idx}",
            underline="none",
            padding=rx.cond(state.is_sidebar_open, "0.4rem 0.8rem", "0.25rem 0.25rem"),
            border_radius="1em",
            bg=rx.cond(is_active, rx.color("gray", 4), None),
            _hover={"bg": rx.color("gray", 5)},
        )

    return rx.vstack(
        rx.cond(
            state.is_sidebar_open,
            rx.hstack(
                rx.text("Statische Giocatori", color_scheme="gray", opacity=0.7),
                width="100%",
                justify="center",
                padding_left="0",
            ),
        ),
        rx.vstack(
            rx.foreach(
                state.match.players_full,
                lambda el, idx: rx.cond(
                    el,
                    player_sidebar_item(
                        el,
                        idx,
                        opponent=rx.cond(state.match.is_double, idx >= 2, idx >= 1),
                        show_name=state.is_sidebar_open,
                    ),
                ),
            ),
            padding_left=rx.cond(state.is_sidebar_open, "1em", 0),
            width=rx.cond(state.is_sidebar_open, "auto", "100%"),
            align=rx.cond(state.is_sidebar_open, "left", "center"),
            spacing="0",
        ),
        spacing="1",
        width="100%",
    )


def sidebar_footer(state) -> rx.Component:
    match_id = getattr(state, "match_id", None)
    footer_classic = rx.hstack(
        rx.vstack(
            rx.button(
                rx.hstack(
                    rx.text(
                        "Condivi la Partita",
                        on_click=[
                            rx.set_clipboard(f"https://dinky.moris.dev/{match_id}"),
                            rx.toast.success("Link alla partita copiato!"),
                        ],
                    ),
                    rx.icon("share-2", size=18),
                ),
                align="center",
                cursor="pointer",
                variant="soft",
            ),
            spacing="1",
        ),
        rx.spacer(),
        rx.color_mode.button(style={"opacity": 0.8, "scale": 0.95}),
        justify="start",
        align="end",
        width="100%",
        padding="0.35em",
    )
    footer_minimize = rx.vstack(
        rx.button(
            rx.icon("share-2", size=18),
            align="center",
            cursor="pointer",
            variant="soft",
        ),
        rx.color_mode.button(style={"opacity": 0.8, "scale": 0.95}),
        width="100%",
        spacing="1",
        align="center",
        justify="center",
    )
    return rx.cond(state.is_sidebar_open, footer_classic, footer_minimize)


def sidebar(state) -> rx.Component:
    sidebar_elem = rx.flex(
        rx.vstack(
            rx.tablet_and_desktop(
                sidebar_minimize(state),
            ),
            sidebar_header(state),
            rx.cond(state.is_sidebar_open, rx.divider()),
            sidebar_menu(state),
            rx.divider(),
            sidebar_menu_players(state),
            rx.spacer(),
            sidebar_footer(state),
            position="fixed",
            overflow="auto",
            align="end",
            width=[
                rx.cond(state.is_sidebar_open, "100%", 0),
                rx.cond(state.is_sidebar_open, sidebar_width, sidebar_close_width),
                rx.cond(state.is_sidebar_open, sidebar_width, sidebar_close_width),
            ],
            height="96dvh",
            padding="1em",
            z_index=5,
            bg=rx.color("gray", 3),
            left=0,
            top="3rem",
        ),
        max_width=rx.cond(state.is_sidebar_open, sidebar_width, sidebar_close_width),
        display=[
            rx.cond(state.is_sidebar_force_open, "flex", "none"),
            rx.cond(state.is_sidebar_force_open, "flex", "none"),
            rx.cond(state.is_sidebar_force_open, "flex", "none"),
            rx.cond(state.is_sidebar_force_open, "flex", "none"),
            rx.cond(state.is_sidebar_force_open, "flex", "none"),
            rx.cond(state.is_sidebar_force_open, "flex", "flex"),
        ],
        width="auto",
        height="100dvh",
        position="sticky",
        justify="end",
        top="0px",
        left="0px",
        flex="1",
        z_index=5,
        bg=rx.color("gray", 3),
    )
    return rx.cond(state.match_stats, sidebar_elem, None)
