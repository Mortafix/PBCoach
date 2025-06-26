import reflex as rx


def color_quality(value, scale=[59.5, 72.5, 84.5], reverse=False):
    return rx.cond(
        value > scale[2] if not reverse else value < scale[0],
        "green",
        rx.cond(
            value > scale[1] if not reverse else value < scale[1],
            "amber",
            rx.cond(
                value > scale[0] if not reverse else value < scale[2], "orange", "red"
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
        "third_drives": "Terzo drive",
        "third_drops": "Terzo drop",
        "third_lobs": "Terzo pallonetto",
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
