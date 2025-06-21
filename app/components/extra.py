from random import choice

import reflex as rx
from app.database.connection import DB


def code_generator(length=5):
    def generate():
        letters = "ABCDEFGHIJKLMNOPQRSTUVWYXZ"
        return "".join(choice(letters) for i in range(length))

    code = generate()
    while DB.stats.count_documents({"code": code}) > 0:
        code = generate()
    return code


def page_loading():
    return rx.vstack(
        rx.skeleton(rx.button("loading", width="90%"), height="100px"),
        rx.skeleton(rx.button("loading", width="90%"), height="20px"),
        rx.skeleton(rx.button("loading", width="90%"), height="50px"),
        rx.skeleton(rx.button("loading", width="90%"), height="200px"),
        width="100%",
        align="center",
    )


def page_title(icon, text):
    return rx.box(
        rx.hstack(
            rx.icon(icon, size=45, stroke_width=1.5),
            rx.heading(text, size="8"),
            spacing="4",
            align="center",
        ),
        background_color=rx.color("gray", 4),
        padding="0.5em 1em",
        border_radius="0.5em",
    )


def form_divider(icon, title):
    return rx.hstack(
        rx.divider(),
        rx.icon(icon, size=45),
        rx.text(title, size="6"),
        rx.divider(),
        align="center",
        width="100%",
    )
