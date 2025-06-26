import reflex as rx
from app.database.data import shots_name_italian, to_metric
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


def shot_stats(player_data, shot_name):
    data = player_data.get(shot_name)
    outcome = data.get("outcome_stats", {})
    speed = data.get("speed_stats", {})
    return Shot(
        name=shots_name_italian(shot_name, str_type=True),
        count=data.get("count"),
        quality=data.get("average_quality", 0),
        success=outcome.get("success_percentage", 0),
        out=outcome.get("out_fault_percentage", 0),
        net=outcome.get("net_fault_percentage", 0),
        baseline_distance=round(to_metric(data.get("average_baseline_distance", 0)), 2),
        net_height=int(to_metric(data.get("average_height_above_net", 0)) * 100),
        speed=round(to_metric(speed.get("average", 0), velocity=True)),
        fastest=round(to_metric(speed.get("fastest", 0), velocity=True)),
    )


class Advice(rx.Base):
    type: str
    relevance: float
    value: float
    rank: tuple[float, float]


def parse_advice(advice_data):
    rank_data = advice_data.get("rank_ci")
    return Advice(
        type=advice_data.get("kind"),
        relevance=round(advice_data.get("relevance"), 2),
        value=round(advice_data.get("value"), 2),
        rank=(round(rank_data[0], 2), round(rank_data[1], 2)),
    )


# ----- STATE


class PlayerState(OverviewState):
    player_name: str = ""
    distance: int
    shots: int
    shots_total: int
    quality: float
    faults: float
    serves: Shot = None
    returns: Shot = None
    drives: Shot = None
    drops: Shot = None
    dinks: Shot = None
    lobs: Shot = None
    smashes: Shot = None
    third_drives: Shot = None
    third_drops: Shot = None
    third_lobs: Shot = None
    resets: Shot = None
    speedups: Shot = None
    passing: Shot = None
    poaches: Shot = None
    forehands: Shot = None
    backhands: Shot = None
    advices: list[Advice] = []

    @rx.event
    def on_load(self):
        player_id = int(self.player_id)
        self.player_name = self.match.players[player_id]
        # player stats
        data = self.match_stats.get("players")[player_id]
        self.distance = int(to_metric(data.get("total_distance_covered")))
        self.shots = data.get("shot_count")
        team_index = (
            self.match.team1_idx
            if player_id in self.match.team1_idx
            else self.match.team2_idx
        )
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
        self.drops = shot_stats(data, "drops")
        self.dinks = shot_stats(data, "dinks")
        self.lobs = shot_stats(data, "lobs")
        self.smashes = shot_stats(data, "smashes")
        self.third_drives = shot_stats(data, "third_drives")
        self.third_drops = shot_stats(data, "third_drops")
        self.third_lobs = shot_stats(data, "third_lobs")
        self.resets = shot_stats(data, "resets")
        self.speedups = shot_stats(data, "speedups")
        self.passing = shot_stats(data, "passing")
        self.poaches = shot_stats(data, "poaches")
        self.forehands = shot_stats(data, "forehands")
        self.backhands = shot_stats(data, "backhands")
        self.advices = [
            parse_advice(data)
            for data in self.match_insights.get("coach_advice")[player_id].get("advice")
        ]
        print(self.advices)
