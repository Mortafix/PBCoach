from __future__ import annotations

from typing import Callable

import reflex as rx
from app import styles
from app.components.header import header
from app.components.sidebar import sidebar
from app.templates.base import State

# meta tags
default_meta = [
    {
        "name": "viewport",
        "content": "width=device-width, shrink-to-fit=no, initial-scale=1",
    },
]


class ThemeState(rx.State):
    accent_color: str = "amber"
    gray_color: str = "gray"
    radius: str = "large"
    scaling: str = "100%"


def template(
    route: str | None = None,
    title: str | None = None,
    description: str | None = None,
    meta: str | None = None,
    script_tags: list[rx.Component] | None = None,
    on_load: rx.event.EventHandler | list[rx.event.EventHandler] | None = None,
) -> Callable[[Callable[[], rx.Component]], rx.Component]:
    def decorator(page_content: Callable[[], rx.Component]) -> rx.Component:
        all_meta = [*default_meta, *(meta or [])]
        page_on_load = (
            (on_load if isinstance(on_load, list) else [on_load]) if on_load else []
        )
        all_on_load = [State.on_load, *page_on_load]

        def templated_page():
            return rx.vstack(
                header(State),
                rx.flex(
                    rx.cond(State.is_in_match, sidebar(State)),
                    rx.flex(
                        rx.toast.provider(visible_toasts=10),
                        rx.vstack(
                            page_content(),
                            align="center",
                            width="100%",
                            **styles.template_content_style,
                        ),
                        width="100%",
                        **styles.template_page_style,
                        max_width=[
                            "100%",
                            "100%",
                            "100%",
                            "100%",
                            "100%",
                            rx.cond(
                                State.is_sidebar_open,
                                styles.max_width,
                                styles.max_width_close,
                            ),
                        ],
                        justify="center",
                        margin_inline="auto",
                    ),
                    flex_direction=[
                        "column",
                        "column",
                        "column",
                        "column",
                        "column",
                        "row",
                    ],
                    font_size="1.25rem",
                    width="100%",
                    margin="auto",
                    position="relative",
                ),
                width="100%",
                spacing="0",
            )

        @rx.page(
            route=route,
            title=f"PB Coach • {title}",
            description=description,
            meta=all_meta,
            script_tags=script_tags,
            on_load=all_on_load,
        )
        def theme_wrap():
            return rx.theme(
                templated_page(),
                has_background=True,
                accent_color=ThemeState.accent_color,
                gray_color=ThemeState.gray_color,
                radius=ThemeState.radius,
                scaling=ThemeState.scaling,
            )

        return theme_wrap

    return decorator
