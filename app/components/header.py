import reflex as rx
from app.components.input import btn_icon, btn_text_icon


def header_button(text: str, icon: str, href: str) -> rx.Component:
    return rx.button(
        rx.icon(icon, size=16),
        rx.text(text, size="4"),
        align="center",
        spacing="1",
        on_click=rx.redirect(href),
        cursor="pointer",
        variant="ghost",
        color=rx.color("black", 9),
    )


def header(state) -> rx.Component:
    return rx.hstack(
        rx.link(
            rx.hstack(
                rx.image(src="/logo/logo.png", width="2rem"),
                rx.tablet_and_desktop(
                    rx.image(src="/logo/logo_text.png", height="2rem"),
                ),
                align="center",
            ),
            href="/",
        ),
        rx.desktop_only(
            rx.hstack(
                header_button("Partite", "medal", "/matches"),
                header_button("Giocatori", "users", "/players"),
                btn_text_icon(
                    "cloud-upload",
                    "Carica statistiche",
                    variant="soft",
                    on_click=rx.redirect("/upload"),
                ),
                wrap="wrap",
                spacing="5",
                align="center",
            ),
        ),
        # mobile menu
        rx.hstack(
            rx.mobile_and_tablet(
                rx.hstack(
                    btn_icon(
                        "medal",
                        color_scheme="gray",
                        variant="soft",
                        on_click=rx.redirect("/matches"),
                    ),
                    btn_icon(
                        "users",
                        color_scheme="gray",
                        variant="soft",
                        on_click=rx.redirect("/players"),
                    ),
                    btn_icon(
                        "cloud-upload", variant="soft", on_click=rx.redirect("/upload")
                    ),
                    align="center",
                ),
            ),
            rx.cond(
                state.is_hamburger_visible,
                rx.button(
                    rx.cond(state.is_sidebar_force_open, rx.icon("x"), rx.icon("menu")),
                    color_scheme="gray",
                    variant="ghost",
                    cursor="pointer",
                    on_click=state.toggle_sidebar_force,
                    visibility=[
                        "visible",
                        "visible",
                        "visible",
                        "visible",
                        "visible",
                        "hidden",
                    ],
                ),
            ),
            align="center",
        ),
        align="center",
        justify="between",
        width="100%",
        position="sticky",
        wrap="wrap",
        top="0px",
        left="0px",
        z_index=10,
        min_height="3rem",
        padding_inline=["0.5rem", "0.5rem", "1em"],
        bg=rx.color("gray", 2),
    )
