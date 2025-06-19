from locale import LC_TIME, setlocale

import reflex as rx
from app.database.players import get_player_name
from app.database.stats import get_match_insights, get_match_stats
from app.templates.base import State

setlocale(LC_TIME, "it_IT.UTF-8")


class OverviewState(State):
    match_stats: dict = {}
    match_insights: dict = {}
    players: list[str] = []
    players_n: int = 0
    team1_idx: list[int] = []
    team2_idx: list[int] = []
    score: list[int] = []
    win_team1: bool | None = None
    rally_total: int = 0
    rally_kitchen: int = 0
    rally_avg: float = 0
    rally_longest: int = 0
    top_runner: tuple[int, int] = (0, 0)
    top_quality: tuple[int, float] = (0, 0)
    top_shooter: tuple[int, int] = (0, 0)
    top_finisher: tuple[int, int] = (0, 0)
    wrost_misser: tuple[int, float] = (0, 0)

    @rx.event
    def on_load(self):
        self.is_in_match = True
        self.match_stats = get_match_stats(self.match_id)
        self.match_insights = get_match_insights(self.match_id)
        game = self.match_stats.get("game", {})
        players_stats = [p or {} for p in self.match_stats.get("players")]
        self.match_name = self.match_stats.get("match_name")
        self.match_date_str = format(
            self.match_stats.get("match_date"), "%a ⋅ %d %b %Y ⋅ %H:%M"
        )
        self.match_players = [
            get_player_name(p_id, short=True) if stats else ""
            for stats, p_id in zip(players_stats, self.match_stats.get("players_ids"))
        ]
        self.players_n = self.match_stats.get("session", {}).get("num_players", 4)
        self.match_is_double = self.players_n == 4
        self.team1_idx = [0, 1] if self.match_is_double else [0]
        self.team2_idx = [2, 3] if self.match_is_double else [2]
        self.score = game.get("game_outcome")
        self.win_team1 = self.score[0] > self.score[1]
        self.rally_total = len(self.match_insights.get("rallies"))
        self.rally_kitchen = game.get("kitchen_rallies")
        self.rally_avg = game.get("avg_shots")
        self.rally_longest = game.get("longest_rally").get("num_shots")
        runners = [pl.get("total_distance_covered", 0) for pl in players_stats]
        self.top_runner = (runners.index(max(runners)), int(max(runners) * 0.3048))
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
