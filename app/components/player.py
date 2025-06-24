import reflex as rx


def player_item(player_id, name) -> rx.Component:
    # TODO: cerca l'immagine per player_id
    return rx.hstack(
        rx.avatar(name, radius="full", fallback=name[:2], border="3px solid white"),
        rx.cond(name, rx.text(name)),
        align="center",
    )
