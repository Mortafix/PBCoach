from json import dump, loads
from os import makedirs, path
from re import match, search

import reflex as rx
from app.components.extra import code_generator
from app.database.locations import add_location_to_db
from app.database.players import add_player_to_db
from app.database.stats import create_match
from app.templates.base import State
from requests import get, post

API_VIDEO_ID = "https://api-2o2klzx4pa-uc.a.run.app/video/get_by_id"
API_JSON = "https://storage.googleapis.com/pbv-pro"


class UploadState(State):
    phase: str = "url"
    info_found: bool = False
    info_not_found: bool = False
    loading_info: bool = False
    video_id: str = ""
    uploaded: bool = False
    uploading: bool = False
    players_n: int = 0
    progress: int = 0
    code: str | None = None
    player_name: str = ""
    player_surname: str = ""
    unknowns: list[bool] = []
    location_type: str = ""
    location_name: str = ""

    @rx.event
    def on_load(self):
        self.phase = "url"
        self.info_found = False
        self.info_not_found = False
        self.loading_info = False
        self.video_id = ""
        self.player_name = ""
        self.player_surname = ""
        self.uploaded = False
        self.players_n = 0
        self.unknowns = [False] * 4
        self.progress = 0
        self.uploading = False
        self.location_name: str = ""
        self.location_type = ""
        return rx.clear_selected_files("upload-form")

    @rx.event
    def search_info(self, form_data):
        self.info_not_found = False
        self.info_found = False
        self.loading_info = True
        yield
        match_url = form_data.get("url")
        if not (m := search(r"share\/(\w+)(\?rf)?", match_url)):
            self.info_not_found = True
            self.loading_info = False
            return
        pb_id = m.group(1)
        response = post(API_VIDEO_ID, json={"vid": pb_id}).json()
        self.video_id = response.get("mux", {}).get("playbackId")
        stats_json = get(f"{API_JSON}/{pb_id}/121/stats.json").json()
        insights_json = get(f"{API_JSON}/{pb_id}/121/insights.json").json()
        if not self.video_id or not stats_json or not insights_json:
            self.info_not_found = True
            return
        self.code = code_generator()
        self.players_n = stats_json.get("session", {}).get("num_players", 4)
        base_client_dir = path.join(rx.get_upload_dir(), self.code)
        if not path.exists(base_client_dir):
            makedirs(base_client_dir)
        data = {"code": self.code} | stats_json
        dump(data, open(path.join(base_client_dir, "stats.json"), "w+"))
        data = {"code": self.code} | insights_json
        dump(data, open(path.join(base_client_dir, "insights.json"), "w+"))
        self.loading_info = False
        self.info_found = True

    @rx.event
    def go_next_step(self):
        self.phase = "info"

    @rx.event
    def go_manual_upload(self):
        self.phase = "manual"

    @rx.event
    def clear_file(self):
        return rx.clear_selected_files("upload-form")

    @rx.event
    async def upload(self, files: list[rx.UploadFile]):
        try:
            if sorted([file.name for file in files]) != ["insights.json", "stats.json"]:
                return rx.toast.error(
                    "I file devono essere esattamente stats.json e insights.json",
                )
            self.code = code_generator()
            base_client_dir = path.join(rx.get_upload_dir(), self.code)
            if not path.exists(base_client_dir):
                makedirs(base_client_dir)
            for file in files:
                filepath = path.join(base_client_dir, file.name)
                upload_data = await file.read()
                if "stats" in file.name:
                    data = {"code": self.code} | loads(upload_data)
                    self.players_n = data.get("session", {}).get("num_players", 4)
                if "insights" in file.name:
                    data = {"code": self.code} | loads(upload_data)
                dump(data, open(filepath, "w+"))
            self.uploaded = True
            self.phase = "info"
            return
        except Exception:
            return rx.toast.error(
                "Errore nel caricamento dei file", position="top-center"
            )

    @rx.event
    def upload_progress(self, progress: dict):
        self.uploading = True
        self.progress = round(progress["progress"] * 100)
        if self.progress >= 100:
            self.uploading = False

    @rx.event
    def submit(self, form_data: dict):
        def check_players(attrs, n):
            n -= sum(self.unknowns)
            for index, is_unknown in enumerate(self.unknowns):
                if is_unknown:
                    attrs.remove(f"giocatore_{index+1}")
            if not all(form_data.get(a) for a in attrs):
                return False
            if len(set(form_data.get(p) for p in attrs if match("giocatore", p))) != n:
                return False
            return True

        base_attrs = [
            "name",
            "date",
            "time",
            "match-type",
            "location",
            "location-type",
            "score1",
            "score2",
        ]
        if form_data.get("location-type") == "Outdoor":
            base_attrs += ["weather"]
        attrs = base_attrs + ["giocatore_1", "giocatore_3"]
        if self.players_n == 2:
            if not check_players(attrs, 2):
                return rx.toast.error(
                    "Le info della partita sono obbligatorie e i giocatori "
                    "devono essere tutti diversi"
                )
        if self.players_n == 4:
            attrs += ["giocatore_2", "giocatore_4"]
            if not check_players(attrs, 4):
                return rx.toast.error(
                    "Le info della partita sono obbligatorie e i giocatori "
                    "devono essere tutti diversi"
                )
        if create_match(self.code, form_data, self.video_id, self.players_n):
            yield rx.toast.success("Info della partita aggiornate!")
            return rx.redirect(f"/match/{self.code}/overview")
        return rx.toast.error("Errore durante l'aggiornamento delle info")

    @rx.event
    def toggle_player(self, player_n):
        self.unknowns[player_n] = not self.unknowns[player_n]

    @rx.event
    def set_player_name(self, value):
        self.player_name = value

    @rx.event
    def set_player_surname(self, value):
        self.player_surname = value

    @rx.event
    def set_location_type(self, value):
        self.location_type = value

    @rx.event
    def set_location_name(self, value):
        self.location_name = value

    @rx.event
    def add_player(self):
        if not self.player_name:
            return rx.toast.error("Devi inserire almeno il nome")
        if add_player_to_db(self.player_name, self.player_surname):
            self.player_name = ""
            self.player_surname = ""
            return rx.toast.success("Giocatore aggiunto!")
        return rx.toast.error("Errore durante l'aggiunta del giocatore")

    @rx.event
    def add_location(self):
        if not self.location_name:
            return rx.toast.error("Devi inserire almeno il nome")
        if add_location_to_db(self.location_name):
            self.location_name = ""
            return rx.toast.success("Location aggiunto!")
        return rx.toast.error("Errore durante l'aggiunta della location")
