import reflex as rx
from app.database.players import get_player_name
from app.database.stats import get_match_insights, get_match_stats
from app.templates.base import State


class OverviewState(State):
    match_stats: dict = {}
    match_insights: dict = {}
    players: list[str] = []
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
        self.match_name = self.match_stats.get("match_name")
        self.match_players = [
            get_player_name(p_id, short=True)
            for p_id in self.match_stats.get("players_ids")
        ]
        self.match_is_double = len(self.match_players) == 4
        self.team1_idx = [0, 1] if self.match_is_double else [0]
        self.team2_idx = [2, 3] if self.match_is_double else [1]
        self.score = game.get("game_outcome")
        self.win_team1 = self.score[0] > self.score[1]
        self.rally_total = 53  # TODO: prendere quello vero
        self.rally_kitchen = game.get("kitchen_rallies")
        self.rally_avg = game.get("avg_shots")
        self.rally_longest = game.get("longest_rally").get("num_shots")
        runners = [
            pl.get("total_distance_covered") for pl in self.match_stats.get("players")
        ]
        self.top_runner = (runners.index(max(runners)), int(max(runners) * 0.3048))
        qualities = [
            pl.get("average_shot_quality") for pl in self.match_stats.get("players")
        ]
        self.top_quality = (qualities.index(max(qualities)), int(max(qualities) * 100))
        shooters = [pl.get("shot_count") for pl in self.match_stats.get("players")]
        self.top_shooter = (shooters.index(max(shooters)), max(shooters))
        finishers = [
            pl.get("final_shot_count") for pl in self.match_stats.get("players")
        ]
        self.top_finisher = (finishers.index(max(finishers)), max(finishers))
        missers = [
            pl.get("net_fault_percentage") + pl.get("out_fault_percentage")
            for pl in self.match_stats.get("players")
        ]
        self.wrost_misser = (missers.index(max(missers)), int(max(missers)))
