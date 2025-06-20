import reflex as rx


def color_quality(value):
    return rx.cond(
        value >= 85,
        "green",
        rx.cond(value > 72.5, "amber", rx.cond(value >= 60, "orange", "red")),
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
