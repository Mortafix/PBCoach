import reflex as rx
from app.database.data import to_metric
from app.states.overview import OverviewState


"""
    [X][X] arrivo in kitchen del team: su servizio e su ricezione
    [X][X] distanza totale percorsa
    [X][ ] quanti tiri sono andati a uno piuttosto che all'altro | torta
    [X][ ] quanto i giocatori sono stati da una parte del campo (sx/dx) | torta
    [X][ ] Percentuale team servizi in e profondità
    [X][ ] Percentuale team risposte in e profondità
    [X][ ] Percentuale terzi colpi tra drop, drive, lob con percentuale successo
"""


def percentage_role(data, attribute):
    roles = [
        [
            counts.get("kitchen_arrival") / counts.get("total")
            for attr in ("oneself", "partner")
            if (counts := player_data.get("role_stats").get(attribute).get(attr))
            and counts.get("total")
        ]
        for player_data in data
    ]
    return [int(sum(role) / len(role) * 100) for role in roles]


def shot_stats(data, shot_type):
    players_shot_data = [p_data.get(shot_type) for p_data in data]
    players_shot_attrs = [
        (
            shot_data.get("outcome_stats").get("success_percentage"),
            shot_data.get("average_quality"),
            to_metric(shot_data.get("average_baseline_distance")),
        )
        for shot_data in players_shot_data
    ]
    return [sum(attr_data) / len(attr_data) for attr_data in zip(*players_shot_attrs)]


def thirds_stats(data):
    thirds = list()
    for shot_type in ("third_drives", "third_drops", "third_lobs"):
        players_shots = [p_data.get(shot_type) for p_data in data]
        shots_stats = [
            (
                p_shots.get("count"),
                p_shots.get("outcome_stats").get("success_percentage"),
                p_shots.get("average_quality"),
            )
            for p_shots in players_shots
            if p_shots.get("count")
        ]
        stats = [
            sum(attr_data) / (len(attr_data) if i > 0 else 1)
            for i, attr_data in enumerate(zip(*shots_stats))
        ]
        thirds.append(stats)
    return thirds


class TeamState(OverviewState):
    team1_serving: list[int]
    team2_serving: list[int]
    team1_receiving: list[int]
    team2_receiving: list[int]
    team1_distance: int
    team2_distance: int
    team1_shots: list[float]
    team2_shots: list[float]
    team1_left_side: list[float]
    team2_left_side: list[float]
    team1_serves: list[float]
    team2_serves: list[float]
    team1_returns: list[float]
    team2_returns: list[float]
    team1_thirds: list[list[float]]
    team2_thirds: list[list[float]]

    @rx.event
    def on_load(self):
        players_stats = [p for p in self.match_stats.get("players") if p]
        team1_stats = [players_stats[i] for i in self.match.team1_idx]
        team2_stats = [players_stats[i] for i in self.match.team2_idx]
        self.team1_serving = percentage_role(team1_stats, "serving")
        self.team2_serving = percentage_role(team2_stats, "serving")
        self.team1_receiving = percentage_role(team1_stats, "receiving")
        self.team2_receiving = percentage_role(team2_stats, "receiving")
        self.team1_distance = int(
            to_metric(sum(data.get("total_distance_covered") for data in team1_stats))
        )
        self.team2_distance = int(
            to_metric(sum(data.get("total_distance_covered") for data in team2_stats))
        )
        self.team1_shots = [data.get("team_shot_percentage") for data in team1_stats]
        self.team2_shots = [data.get("team_shot_percentage") for data in team2_stats]
        self.team1_left_side = [d.get("team_left_side_percentage") for d in team1_stats]
        self.team2_left_side = [d.get("team_left_side_percentage") for d in team2_stats]
        print(self.team1_shots, self.team1_left_side)
        self.team1_serves = shot_stats(team1_stats, "serves")
        self.team2_serves = shot_stats(team2_stats, "serves")
        self.team1_returns = shot_stats(team1_stats, "returns")
        self.team2_returns = shot_stats(team2_stats, "returns")
        self.team1_thirds = thirds_stats(team1_stats)
        self.team2_thirds = thirds_stats(team2_stats)
