import reflex as rx
from app.templates import template
from app.templates.base import State


class IndexState(State):
    @rx.event
    def on_load(self):
        self.is_header_open = False


@template(route="/", title="Home", on_load=IndexState.on_load)
def index_page() -> rx.Component:
    return rx.vstack(
        rx.text("Ciao"),
        rx.text("Questo è il portale coach di pickleball e bla bla bla"),
        rx.button("Analizzami", on_click=rx.redirect("/matches"), cursor="pointer"),
        width="60%",
        margin_inline="auto",
    )
