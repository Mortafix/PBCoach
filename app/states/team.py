import reflex as rx
from app.database.data import to_metric
from app.states.overview import OverviewState


"""
    [X][X] arrivo in kitchen del team: su servizio e su ricezione
    [X][X] distanza totale percorsa
    [X][X] quanti tiri sono andati a uno piuttosto che all'altro | torta
    [X][X] quanto i giocatori sono stati da una parte del campo (sx/dx) | torta
    [X][X] Percentuale team servizi in e profondità
    [X][X] Percentuale team risposte in e profondità
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
            shot_data.get("average_quality") * 100,
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
    colors: list[str] = ["blue", "tomato", "bronze"]
    colors_inout: list[str] = ["green", "red"]
    team1_serving: list[int]
    team2_serving: list[int]
    team1_receiving: list[int]
    team2_receiving: list[int]
    team1_distance: int
    team2_distance: int
    team1_shots: list[dict]
    team2_shots: list[dict]
    team1_left_side: list[dict]
    team2_left_side: list[dict]
    team1_serves: tuple[list, float, float]
    team2_serves: tuple[list, float, float]
    team1_returns: tuple[list, float, float]
    team2_returns: tuple[list, float, float]
    team1_thirds: list[list[float]]
    team2_thirds: list[list[float]]

    def _to_pie_data(self, data, indexes):
        return [
            {
                "name": self.match.players[player_idx],
                "value": round(value),
                "fill": rx.color(self.colors[i], 8),
                "stroke": None,
            }
            for i, (player_idx, value) in enumerate(zip(indexes, data))
        ]

    def _to_pie_data_inout(self, in_perc):
        return [
            {
                "name": "Dentro" if i == 0 else "Fuori",
                "value": round(value),
                "fill": rx.color(self.colors_inout[i], 8),
                "stroke": None,
            }
            for i, value in enumerate([in_perc, 100 - in_perc])
        ]

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
            to_metric(
                sum(p_stats.get("total_distance_covered") for p_stats in team1_stats)
            )
        )
        self.team2_distance = int(
            to_metric(
                sum(p_stats.get("total_distance_covered") for p_stats in team2_stats)
            )
        )
        total_shots = sum(data.get("shot_count") for data in team1_stats)
        data = [
            int(p_stats.get("team_shot_percentage") / 100 * total_shots)
            for p_stats in team1_stats
        ]
        self.team1_shots = self._to_pie_data(data, self.match.team1_idx)
        total_shots = sum(data.get("shot_count") for data in team2_stats)
        data = [
            int(p_stats.get("team_shot_percentage") / 100 * total_shots)
            for p_stats in team2_stats
        ]
        self.team2_shots = self._to_pie_data(data, self.match.team2_idx)
        data = [d.get("team_left_side_percentage") for d in team1_stats]
        self.team1_left_side = self._to_pie_data(data, self.match.team1_idx)
        data = [d.get("team_left_side_percentage") for d in team2_stats]
        self.team2_left_side = self._to_pie_data(data, self.match.team2_idx)
        data = shot_stats(team1_stats, "serves")
        self.team1_serves = (self._to_pie_data_inout(data[0]), *data[1:])
        data = shot_stats(team2_stats, "serves")
        self.team2_serves = (self._to_pie_data_inout(data[0]), *data[1:])
        data = shot_stats(team1_stats, "returns")
        self.team1_returns = (self._to_pie_data_inout(data[0]), *data[1:])
        data = shot_stats(team2_stats, "returns")
        self.team2_returns = (self._to_pie_data_inout(data[0]), *data[1:])
        self.team1_thirds = thirds_stats(team1_stats)
        print(self.team1_thirds)
        self.team2_thirds = thirds_stats(team2_stats)
