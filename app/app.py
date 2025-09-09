import reflex as rx
from app import styles
from app.components.header import header
from app.components.sidebar import sidebar
from app.pages import (extra, index, matches, overview, player, player_stats,
                       players, team, upload, video)
from app.services.api import test_token, update_players_avatar
from fastapi import FastAPI

# endpoint routes
fastapi_app = FastAPI()
fastapi_app.add_api_route("/test", test_token)
fastapi_app.add_api_route("/update-avatars", update_players_avatar)

# reflex app
app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
    api_transformer=fastapi_app,
)
app.add_page(
    extra.not_found_page(),
    route="/404",
    title="Pagina non trovata",
    description="Pagina non trovata",
)
