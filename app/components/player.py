import reflex as rx


def player_item(player_id, name) -> rx.Component:
    name = rx.cond(name, name, "")
    return rx.hstack(
        rx.avatar(
            src=f"/players/{player_id}.jpg",
            radius="full",
            fallback=name[:2],
            border="3px solid white",
        ),
        rx.cond(name, rx.text(name)),
        align="center",
    )
