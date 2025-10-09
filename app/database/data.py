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


def color_quality_float(value, scale, reverse=False):
    if reverse:
        scale = scale[::-1]
    if (reverse and value < scale[0]) or (not reverse and value > scale[2]):
        return "green"
    if (reverse and value < scale[1]) or (not reverse and value > scale[1]):
        return "amber"
    if (reverse and value < scale[2]) or (not reverse and value > scale[0]):
        return "orange"
    return "red"


def to_metric(imperial_value, velocity=False):
    if velocity:
        return imperial_value * 1.609344
    return imperial_value * 0.3048


# ---- RATINGS


def calculate_ratings(data):
    def to_real_rating(value):
        return round(value * 6 + 2, 1)  # [0,1] -> [2,8]

    if not data:
        return {}
    return {
        "Servizio": to_real_rating(data.get("serve")),
        "Risposta": to_real_rating(data.get("return")),
        "Attacco": to_real_rating(data.get("offense")),
        "Difesa": to_real_rating(data.get("defense")),
        "Agilità": to_real_rating(data.get("agility")),
        "Consistenza": to_real_rating(data.get("consistency")),
        "Generale": to_real_rating(data.get("overall")),
    }


# ---- ITALIAN


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


def highlights_name_italian(event, str_type=True):
    events_name = {
        "Long Battle": "Lunga Battaglia",
        "Exciting Exchange": "Scambio Eccitante",
        "Firefight": "Battaglia di Fuoco",
        "Firefight and Long Battle": "Battaglia Lunga di Fuoco",
        "Firefight and Smash": "Battaglia di Smash",
        "Passing Shot": "Passante",
        "Poach": "Anticipo",
        "Smash": "Smash",
        "Smashes": "Smash Ovunque",
        "ATP": "ATP",
    }
    if str_type:
        return events_name.get(event, "Punto Incredibile")
    return rx.match(event, *(tuple(events_name.items())), "Punto Incredibile")


def highlights_icons(event):
    if not event:
        return "sparkles"
    event = event.lower()
    if "smash" in event:
        return "bomb"
    if "battle" in event:
        return "swords"
    if "exchange" in event:
        return "git-compare-arrows"
    if "firefight" in event:
        return "flame"
    return "sparkles"


# ---- SINGLE SHOTS

SINGLE_SHOTS = [
    "serves",
    "returns",
    "drives",
    "drops",
    "dinks",
    "lobs",
    "smashes",
    "third_drives",
    "third_drops",
    "third_lobs",
    "resets",
    "speedups",
    "passing",
    "poaches",
]

REVERSE_DEEP_SHOTS = ["drops", "dinks", "third_drops", "resets"]
AGGRESSIVE_SHOTS = ["drives", "poaches", "third_drives", "speedups", "poaches"]
DEFENSIVE_SHOTS = ["drops", "dinks", "third_drops", "resets", "lobs"]

# ---- COURTS

COURTS = [
    "Cemento",
    "Resina",
    "Asfalto",
    "Gomma",
    "Legno",
    "PVC",
    "Tappeto portatile",
]
