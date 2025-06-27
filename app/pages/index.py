import reflex as rx
from app.templates import template
from app.templates.base import State


class IndexState(State):
    @rx.event
    def on_load(self):
        self.is_header_open = False


def background() -> rx.Component:
    return rx.box(
        position="absolute",
        top=0,
        left=0,
        width="100%",
        height="100dvh",
        filter="blur(8px)",
        background_image="url('/images/pickleball_field.webp')",
        background_position="center",
        background_repeat="no-repeat",
        background_size="cover",
        z_index=-1,
    )


@template(route="/", title="Home", on_load=IndexState.on_load)
def index_page() -> rx.Component:
    return rx.vstack(
        background(),
        rx.image(src="/logo/logo_text.png", width="35rem"),
        rx.image(src="/images/coach_happy.webp", width="30rem"),
        rx.vstack(
            rx.text(
                "Nel pickleball non serve essere i più forti, ma i più intelligenti!",
                size="5",
                text_align="center",
            ),
            padding="1rem 2rem",
            align="center",
            bg="#1D1D1DEB",
        ),
        rx.button(
            rx.hstack(
                rx.text("Analizza", size="7"),
                rx.icon("arrow-right", size=30),
                align="center",
                spacing="2",
            ),
            size="4",
            cursor="pointer",
            on_click=rx.redirect("/matches"),
        ),
        width=["90%", "80%", "60%"],
        height="90%",
        align="center",
        justify="between",
        margin="auto auto",
        z_index=100,
    )
