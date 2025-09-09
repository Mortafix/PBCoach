import reflex as rx


def gender_color(gender):
    return rx.match(gender, ("Maschio", "indigo"), ("Femmina", "pink"), "green")


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


def player_item_small(player_id, name) -> rx.Component:
    name = rx.cond(name, name, "")
    return rx.hstack(
        rx.avatar(
            src=f"/players/{player_id}.jpg",
            radius="full",
            fallback=name[:2],
            border="2px solid white",
            size="2",
        ),
        rx.cond(name, rx.text(name, size="4")),
        align="center",
        spacing="1",
    )
