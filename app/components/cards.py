import reflex as rx


def card(content, **attributes) -> rx.Component:
    return rx.card(
        content,
        size="4",
        border=0,
        style={"::after": {"box-shadow": "0 0 0 0"}, **attributes},
    )


base_attributes = {
    # "box_shadow": styles.box_shadow_style,
    "size": "3",
    "width": "100%",
    "_before": {"background-color": rx.color_mode_cond("#f3f3f3", "#18191b")},
}

form_attributes = {"min_width": "50vw", "max_width": "90vw"}


def form_card(*children, **props):
    return rx.card(*children, **form_attributes | base_attributes | props)
