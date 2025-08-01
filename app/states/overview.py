from locale import LC_TIME, setlocale

import reflex as rx
from app.database.data import to_metric
from app.database.matches import parse_model
from app.database.stats import get_match_insights, get_match_stats
from app.templates.base import State

setlocale(LC_TIME, "it_IT.UTF-8")


class OverviewState(State):
    is_match_found: bool
    rally_total: int = 0
    rally_kitchen: int = 0
    rally_avg: float = 0
    rally_longest: int = 0
    top_runner: tuple[int, int] = (0, 0)
    top_quality: tuple[int, float] = (0, 0)
    top_shooter: tuple[int, int] = (0, 0)
    top_finisher: tuple[int, int] = (0, 0)
    wrost_misser: tuple[int, float] = (0, 0)
    players_quality: list[tuple[int, str]] = []

    @rx.event
    def on_load(self):
        self.is_sidebar_open = True
        self.is_in_match = True
        self.match_stats = get_match_stats(self.match_id)
        if not self.match_stats:
            self.is_sidebar_open = False
            self.is_match_found = False
            return
        self.match_insights = get_match_insights(self.match_id)
        self.match = parse_model(self.match_stats)
        self.is_match_found = True
        # overview info
        game = self.match_stats.get("game", {})
        self.rally_total = len(self.match_insights.get("rallies"))
        self.rally_kitchen = game.get("kitchen_rallies")
        self.rally_avg = game.get("avg_shots")
        self.rally_longest = game.get("longest_rally").get("num_shots")
        players_stats = [p or {} for p in self.match_stats.get("players")]
        runners = [pl.get("total_distance_covered", 0) for pl in players_stats]
        self.top_runner = (runners.index(max(runners)), int(to_metric(max(runners))))
        qualities = [pl.get("average_shot_quality", 0) for pl in players_stats]
        self.top_quality = (qualities.index(max(qualities)), int(max(qualities) * 100))
        shooters = [pl.get("shot_count", 0) for pl in players_stats]
        self.top_shooter = (shooters.index(max(shooters)), max(shooters))
        finishers = [pl.get("final_shot_count", 0) for pl in players_stats]
        self.top_finisher = (finishers.index(max(finishers)), max(finishers))
        missers = [
            pl.get("net_fault_percentage", 0) + pl.get("out_fault_percentage", 0)
            for pl in players_stats
        ]
        self.wrost_misser = (missers.index(max(missers)), int(max(missers)))
        self.players_quality = [self.calculate_quality(data) for data in players_stats]

    @rx.var
    def players_description(self) -> str:
        if not self.match:
            return ""
        team1 = " - ".join(self.match.players[index] for index in self.match.team1_idx)
        team2 = " - ".join(self.match.players[index] for index in self.match.team2_idx)
        return f"{team1} VS {team2}"

    @rx.event
    def calculate_quality(self, data):
        if not data:
            return 0, ""
        attributes = [
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
        qualities = {
            attr: (data.get(attr).get("count"), quality)
            for attr in attributes
            if (quality := data.get(attr).get("average_quality"))
        }
        total_weight = sum(count for count, _ in qualities.values())
        weighted_sum = sum(count * perc for count, perc in qualities.values())
        weighted_mean = weighted_sum / total_weight if total_weight else 0
        shots_ql = sorted(qualities, key=lambda el: qualities.get(el)[1])
        return int(weighted_mean * 100), shots_ql[0], shots_ql[-1]
