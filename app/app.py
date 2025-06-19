import reflex as rx
from app import styles
from app.components.header import header
from app.components.sidebar import sidebar
from app.pages import (game_stats, overview, player_stats, shot_explorer,
                       team_stats, upload)

app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
)
