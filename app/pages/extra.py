import reflex as rx
from app.components.input import btn_text_icon
from app.templates import template
from app.templates.base import State


class ExtraState(State):
    @rx.event
    def on_load(self):
        self.is_in_match = False
        self.match_stats = None


@template(title="404", on_load=ExtraState.on_load)
def not_found_page() -> rx.Component:
    return rx.vstack(
        rx.text("Pagina non trovata", size="9", weight="medium"),
        rx.callout(
            "Non è stata trovata nessuna pagina a questo indirizzo.. "
            "controlla e riprova",
            icon="info",
            size="2",
            color_scheme="yellow",
        ),
        rx.link(
            btn_text_icon("move_left", "Home", spacing="2", variant="soft"), href="/"
        ),
        justify="center",
        align="center",
        height="80%",
        spacing="5",
    )


def match_not_found() -> rx.Component:
    return rx.vstack(
        rx.text("Match non trovato", size="9", weight="medium"),
        rx.callout(
            "Non è stata trovata nessuna pagina a questo indirizzo.. "
            "controlla e riprova",
            icon="info",
            size="2",
            color_scheme="yellow",
        ),
        rx.link(
            btn_text_icon("move_left", "Partite", spacing="2", variant="soft"),
            href="/matches",
        ),
        justify="center",
        align="center",
        height="80%",
        spacing="5",
    )
