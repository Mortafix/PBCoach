import reflex as rx
from app.components.input import btn_text_icon


def header_button(text: str, href: str) -> rx.Component:
    return rx.button(text, on_click=rx.redirect(href), cursor="pointer")


def header(state) -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.icon("bar-chart-big"), rx.text("MPC Coach", size="7"), align="center"
        ),
        rx.hstack(
            header_button("Partite", "#"),
            header_button("Giocatori", "#"),
            btn_text_icon(
                "cloud-upload",
                "Carica statistiche",
                variant="soft",
                on_click=rx.redirect("/upload"),
            ),
            align="center",
        ),
        rx.button(
            rx.icon("menu"),
            visibility=[
                "visible",
                "visible",
                "visible",
                "visible",
                "visible",
                "hidden",
            ],
            color_scheme="gray",
            variant="ghost",
            cursor="pointer",
            on_click=state.toggle_sidebar_force,
        ),
        align="center",
        justify="between",
        width="100%",
        height="5dvh",
        min_height="3rem",
        padding_inline="1em",
        bg=rx.color("gray", 2),
    )
