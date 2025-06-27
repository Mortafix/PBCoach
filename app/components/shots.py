import reflex as rx
from app.database.data import color_quality


def base_item(text, value):
    return element_stat(text, value, "gray")


def custom_item(text, value, elem_type, scale=None, reverse_scale=False):
    color = color_quality(value, scale, reverse_scale)
    return element_stat(text, value, color, elem_type)


def quality_item(text, value, with_color=True):
    color = color_quality(value) if with_color else "gray"
    return element_stat(text, value, color, "quality")


def velocity_item(text, value, with_color=True):
    color = color_quality(value, [30, 40, 50]) if with_color else "gray"
    return element_stat(text, value, color, "velocity")


def deep_item(text, value, with_color=True, reverse=False):
    color = color_quality(value, [4.55, 3, 1.55], reverse=~reverse)
    text_value = rx.cond(
        ~reverse,
        rx.match(
            color,
            ("green", "Fondocampo"),
            ("amber", "Lungo"),
            ("orange", "In mezzo"),
            ("red", "Kitchen"),
            "",
        ),
        rx.match(
            color,
            ("green", "Kitchen"),
            ("amber", "In mezzo"),
            ("orange", "Lungo"),
            ("red", "Fondocampo"),
            "",
        ),
    )
    color = color if with_color else "gray"
    return element_stat(text, text_value, color, "deep", tooltip=value.to(str))


def height_item(text, value, color=False):
    color = color_quality(value) if color else "gray"
    return element_stat(text, value, color, "net")


# ---- base


def element_stat(text, value, color, elem_type=None, tooltip=None):
    units = {"quality": "%", "velocity": " km/h", "deep": " m", "net": " cm"}
    return rx.hstack(
        rx.text(text, color_scheme="gray"),
        rx.cond(
            tooltip,
            rx.tooltip(
                rx.badge(value, color_scheme=color, size="3"),
                content=f"{tooltip}{units.get(elem_type, '')}",
            ),
            rx.badge(
                f"{value}{units.get(elem_type, '')}", color_scheme=color, size="3"
            ),
        ),
        cursor="default",
        align="center",
        justify="between",
        width="100%",
    )
