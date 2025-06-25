import reflex as rx
from app.components.input import btn_icon, btn_text_icon

hamburger_visible = ["visible", "visible", "visible", "visible", "visible", "hidden"]
visible_mobile = ["flex", "flex", "flex", "none"]
hidden_mobile = ["none", "none", "none", "flex"]


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
        rx.hstack(
            rx.icon("bar-chart-big"), rx.text("MPC Coach", size="7"), align="center"
        ),
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
            display=hidden_mobile,
        ),
        # mobile menu
        rx.hstack(
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
                display=visible_mobile,
            ),
            rx.button(
                rx.icon("menu"),
                color_scheme="gray",
                variant="ghost",
                cursor="pointer",
                on_click=state.toggle_sidebar_force,
                visibility=hamburger_visible,
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
        padding_inline="1em",
        bg=rx.color("gray", 2),
    )
