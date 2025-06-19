import reflex as rx

field_style = {"width": "100%", "size": "3"}


def std_input(icon, label, rx_input, **params) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon(icon, size=16, stroke_width=1.5),
            rx.text(label),
            width="100%",
            align="center",
            spacing="2",
        ),
        rx_input,
        direction="column",
        **{"spacing": "1", "width": "100%"} | params,
    )


def form_header(icon, title, subtitle):
    return rx.hstack(
        rx.badge(rx.icon(icon, size=32), radius="full", padding="0.65rem"),
        rx.vstack(
            rx.heading(title, size="4", weight="bold"),
            rx.text(subtitle, size="2"),
            spacing="1",
            height="100%",
            align_items="start",
        ),
        height="100%",
        spacing="4",
        align_items="center",
        width="100%",
    )


# ---- BUTTONS


def btn_icon(icon, icon_size=16, icon_w=3, **params):
    return rx.button(
        rx.icon(icon, size=icon_size, stroke_width=icon_w), cursor="pointer", **params
    )


def btn_text_icon(
    icon, text="", text_size="3", icon_size=16, icon_w=3, spacing="3", **params
):
    return rx.button(
        rx.hstack(
            rx.icon(icon, size=icon_size, stroke_width=icon_w),
            rx.text(text, size=text_size),
            align="center",
            spacing=spacing,
        ),
        cursor="pointer",
        **params,
    )
