import reflex as rx
from app.components.cards import card
from app.templates.base import State


def expander(
    title, content, side=None, size="1", opened=None, click_func=None, **params
) -> rx.Component:
    class ExpanderState(State):
        @rx.event
        def click(self):
            self.expander_is_open = not self.expander_is_open

    click_func = click_func or ExpanderState.click

    return card(
        rx.vstack(
            rx.hstack(
                title,
                rx.hstack(
                    rx.cond(side is not None, rx.hstack(side or rx.text(""))),
                    rx.icon(
                        "chevron-up",
                        rotate=rx.cond(
                            opened | ExpanderState.expander_is_open, "0deg", "180deg"
                        ),
                        transition="rotate 0.3s ease-out",
                    ),
                    align="center",
                ),
                width="100%",
                align="center",
                justify="between",
                on_click=click_func,
                cursor="pointer",
            ),
            rx.cond(opened | ExpanderState.expander_is_open, content, None),
            margin_bottom=rx.cond(opened | ExpanderState.expander_is_open, "0.25em", 0),
        ),
        size=size,
        padding="0.4em 0.7em",
        **params
    )
