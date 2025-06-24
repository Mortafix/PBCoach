import reflex as rx


def color_quality(value, scale=[59.5, 72.5, 84.5]):
    return rx.cond(
        value > scale[2],
        "green",
        rx.cond(value > scale[1], "amber", rx.cond(value > scale[0], "orange", "red")),
    )


def shots_name_italian(shot):
    return rx.match(
        shot,
        ("serves", "Servizio"),
        ("returns", "Risposta"),
        ("drives", "Drive"),
        ("drops", "Drop"),
        ("dinks", "Dink"),
        ("lobs", "Pallonetto"),
        ("smashes", "Smash"),
        ("third_drives", "Terzo drive"),
        ("third_drops", "Terzo drop"),
        ("third_lobs", "Terzo pallonetto"),
        ("resets", "Reset"),
        ("speedups", "Velocizzazione"),
        ("passing", "Passante"),
        ("poaches", "Anticipo"),
        ("forehands", "Dritto"),
        ("backhands", "Rovescio"),
        ("thirds", "Tero colpo"),
        ("fourths", "Quarto colpo"),
        ("fifths", "Quinto colpo"),
        "Sconosciuto",
    )


def to_metric(imperial_value):
    return imperial_value * 0.3048
