from os import path

import reflex as rx
from app.database.data import calculate_ratings, shots_name_italian, to_metric
from app.states.overview import OverviewState

# ---- MODELS


class Shot(rx.Base):
    name: str
    count: int
    quality: float
    success: float
    out: float
    net: float
    baseline_distance: float
    net_height: int
    speed: int
    fastest: int
    is_reverse_deep: bool = False
    pie_inout: list[dict]


def shot_stats(player_data, shot_name, reverse_deep=False):
    data = player_data.get(shot_name)
    outcome = data.get("outcome_stats", {})
    speed = data.get("speed_stats", {})
    out_p = outcome.get("out_fault_percentage", 0)
    net_p = outcome.get("net_fault_percentage", 0)
    success_p = max(100 - (out_p + net_p), 0)
    return Shot(
        name=shots_name_italian(shot_name, str_type=True),
        count=data.get("count"),
        quality=round(data.get("average_quality", 0) * 100),
        success=success_p,
        out=out_p,
        net=net_p,
        baseline_distance=round(to_metric(data.get("average_baseline_distance", 0)), 2),
        net_height=int(to_metric(data.get("average_height_above_net", 0)) * 100),
        speed=round(to_metric(speed.get("average", 0), velocity=True)),
        fastest=round(to_metric(speed.get("fastest", 0), velocity=True)),
        is_reverse_deep=reverse_deep,
        pie_inout=to_pie_data_inout(success_p, out_p, net_p),
    )


class Advice(rx.Base):
    type: str
    relevance: float
    value: float
    rank: tuple[float, float]


def parse_advice(advice_data, version):
    rank_data = advice_data.get("rank_ci" if version == "2.9.0" else "ci")
    return Advice(
        type=advice_data.get("kind"),
        relevance=round(advice_data.get("relevance"), 2),
        value=round(advice_data.get("value"), 2),
        rank=(round(rank_data[0], 2), round(rank_data[1], 2)),
    )


# ----- STATE


def to_pie_data_inout(success, out, net):
    return [
        {
            "name": ["Dentro", "Fuori", "Rete"][i],
            "value": round(value),
            "fill": rx.color(["green", "red", "crimson"][i], 8),
            "stroke": None,
        }
        for i, value in enumerate([success, out, net])
        if value
    ]


def to_pie_data_multiple(colors, *shots):
    return [
        {
            "name": shot.name,
            "value": int(shot.count),
            "fill": rx.color(colors[i], 8),
            "stroke": None,
        }
        for i, shot in enumerate(shots)
        if shot.count
    ]


class PlayerState(OverviewState):
    colors: list[str] = ["blue", "tomato", "plum"]
    player_name: str = ""
    distance: int
    shots: int
    shots_total: int
    quality: float
    faults: float
    serves: Shot = None
    serves_inout: list[dict] = []
    returns: Shot = None
    returns_inout: list[dict] = []
    drives: Shot = None
    drops: Shot = None
    dinks: Shot = None
    lobs: Shot = None
    smashes: Shot = None
    third_drives: Shot = None
    third_drops: Shot = None
    third_lobs: Shot = None
    thirds: list[dict] = []
    resets: Shot = None
    speedups: Shot = None
    passing: Shot = None
    poaches: Shot = None
    forehands: Shot = None
    backhands: Shot = None
    hands: list[dict] = []
    advices: list[Advice] = []
    ratings: dict[str, float] = {}
    # ---- page
    avatar_id: int
    info_shots: list[Shot] = []
    zero_shots: list[Shot] = []
    current_shot: Shot | None = None
    current_advice: str = ""

    @rx.var
    def partial_image_url(self) -> str:
        if not self.match or not self.match.id:
            return ""
        google_url = "https://storage.googleapis.com/pbv-pro"
        return f"{google_url}/{self.match.id}/141/player{self.avatar_id}"

    @rx.event
    def change_shot(self, shot: Shot):
        self.current_shot = shot

    @rx.event
    def change_advice(self, advice: Advice):
        advice_path = path.join("assets/advices", f"{advice.type}.md")
        if not path.exists(advice_path):
            self.current_advice = "Mi spiace, **campione**.. Ora non sono disponibile."
            return
        self.current_advice = open(advice_path).read()

    @rx.event
    def on_load(self):
        player_id = int(self.player_id)
        self.player_name = self.match.players_full[player_id]
        # v_stats = self.match_stats.get("version")  # not used
        v_insights = self.match_insights.get("version")
        player_insights = self.match_insights.get("player_data")[player_id]
        self.avatar_id = player_insights.get("avatar_id", -1)
        # player ranking
        self.ratings = dict()
        if ratings_data := player_insights.get("trends", {}).get("ratings"):
            self.ratings = calculate_ratings(ratings_data)
        # player stats
        data = self.match_stats.get("players")[player_id]
        self.distance = int(to_metric(data.get("total_distance_covered")))
        self.shots = data.get("shot_count")
        team_index = (
            self.match.team1_idx
            if player_id in self.match.team1_idx
            else self.match.team2_idx
        )
        team_index = team_index if self.match.is_double else [player_id]
        self.shots_total = sum(
            p_data.get("shot_count")
            for p_data in [self.match_stats.get("players")[p_id] for p_id in team_index]
        )
        self.faults = round(
            sum(data.get(f"{attr}_fault_percentage") for attr in ("net", "out"))
        )
        self.quality = round(data.get("average_shot_quality") * 100)
        # shots stats
        self.serves = shot_stats(data, "serves")
        self.returns = shot_stats(data, "returns")
        self.drives = shot_stats(data, "drives")
        self.drops = shot_stats(data, "drops", reverse_deep=True)
        self.dinks = shot_stats(data, "dinks", reverse_deep=True)
        self.lobs = shot_stats(data, "lobs")
        self.smashes = shot_stats(data, "smashes")
        self.third_drives = shot_stats(data, "third_drives")
        self.third_drops = shot_stats(data, "third_drops", reverse_deep=True)
        self.third_lobs = shot_stats(data, "third_lobs")
        self.thirds = to_pie_data_multiple(
            self.colors, self.third_drives, self.third_drops, self.third_lobs
        )
        self.resets = shot_stats(data, "resets", reverse_deep=True)
        self.speedups = shot_stats(data, "speedups")
        self.passing = shot_stats(data, "passing")
        self.poaches = shot_stats(data, "poaches")
        self.forehands = shot_stats(data, "forehands")
        self.backhands = shot_stats(data, "backhands")
        self.hands = to_pie_data_multiple(self.colors, self.forehands, self.backhands)
        advices_data = [
            parse_advice(data, v_insights)
            for data in self.match_insights.get("coach_advice")[player_id].get("advice")
        ]
        self.advices = sorted(advices_data, key=lambda el: -el.relevance)[:2]

        # ---- page
        self.current_shot = self.serves
        info_shots = [
            self.serves,
            self.returns,
            self.drives,
            self.drops,
            self.dinks,
            self.lobs,
            self.smashes,
            self.resets,
            self.speedups,
            self.passing,
            self.poaches,
            self.forehands,
            self.backhands,
        ]
        self.info_shots = sorted(info_shots, key=lambda el: -el.quality)
        self.zero_shots = [shot for shot in info_shots if shot.count == 0]
        self.change_advice(self.advices[0])


class PlayersState(OverviewState):
    @rx.event
    def on_load(self):
        if not self.match_stats:
            return
