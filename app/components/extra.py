from random import choice

import reflex as rx


def code_generator(length=5):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWYXZ"
    return "".join(choice(letters) for i in range(length))


def page_loading():
    return rx.vstack(
        rx.skeleton(rx.button("loading", width="90%"), height="100px"),
        rx.skeleton(rx.button("loading", width="90%"), height="20px"),
        rx.skeleton(rx.button("loading", width="90%"), height="50px"),
        rx.skeleton(rx.button("loading", width="90%"), height="200px"),
        width="100%",
        align="center",
    )
