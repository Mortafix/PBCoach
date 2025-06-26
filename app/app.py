import reflex as rx
from app import styles
from app.components.header import header
from app.components.sidebar import sidebar
from app.pages import (extra, index, matches, overview, player_stats, players,
                       team, upload)

app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
)
app.add_page(
    extra.not_found_page(),
    route="/404",
    title="Pagina non trovata",
    description="Pagina non trovata",
)
