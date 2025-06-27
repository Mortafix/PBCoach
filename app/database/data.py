import reflex as rx


def color_quality(value, scale=[59.5, 72.5, 84.5], reverse=False):
    scale = rx.cond(reverse, scale[::-1], scale)
    return rx.cond(
        rx.cond(reverse, value < scale[0], value > scale[2]),
        "green",
        rx.cond(
            rx.cond(reverse, value < scale[1], value > scale[1]),
            "amber",
            rx.cond(
                rx.cond(reverse, value < scale[2], value > scale[0]), "orange", "red"
            ),
        ),
    )


def shots_name_italian(shot, str_type=False):
    shots_name = {
        "serves": "Servizio",
        "returns": "Risposta",
        "drives": "Drive",
        "drops": "Drop",
        "dinks": "Dink",
        "lobs": "Pallonetto",
        "smashes": "Smash",
        "third_drives": "Drive",
        "third_drops": "Drop",
        "third_lobs": "Pallonetto",
        "resets": "Reset",
        "speedups": "Velocizzazione",
        "passing": "Passante",
        "poaches": "Anticipo",
        "forehands": "Dritto",
        "backhands": "Rovescio",
        "thirds": "Tero colpo",
        "fourths": "Quarto colpo",
        "fifths": "Quinto colpo",
    }
    if str_type:
        return shots_name.get(shot, "Sconosciuto")
    return rx.match(shot, *(tuple(shots_name.items())), "Sconosciuto")


def to_metric(imperial_value, velocity=False):
    if velocity:
        return imperial_value * 1.609344
    return imperial_value * 0.3048
