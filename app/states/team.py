import reflex as rx
from app.database.data import to_metric
from app.states.overview import OverviewState


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
            round(to_metric(shot_data.get("average_baseline_distance")), 2),
        )
        for shot_data in players_shot_data
    ]
    data = [sum(attr_data) / len(attr_data) for attr_data in zip(*players_shot_attrs)]
    return [data[0], int(data[1]), round(data[2], 2)]


def thirds_stats(data):
    thirds = list()
    for shot_type in ("third_drives", "third_drops", "third_lobs"):
        players_shots = [p_data.get(shot_type) for p_data in data]
        shots_stats = [
            (p_shots.get("count", 0), p_shots.get("average_quality", 0))
            for p_shots in players_shots
        ]
        stats = [
            sum(attr_data) / (len(attr_data) if i > 0 else 1)
            for i, attr_data in enumerate(zip(*shots_stats))
        ]
        thirds.append(stats)
    return thirds


class TeamState(OverviewState):
    colors: list[str] = ["blue", "tomato", "plum"]
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
    team1_serves: tuple[list, int, float]
    team2_serves: tuple[list, int, float]
    team1_returns: tuple[list, int, float]
    team2_returns: tuple[list, int, float]
    team1_thirds_pie: list[dict]
    team1_thirds_quality: list[int]
    team2_thirds_pie: list[dict]
    team2_thirds_quality: list[int]

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

    def _to_pie_data_thirds(self, thirds):
        third_names = ["Drive", "Drop", "Pallonetto"]
        return [
            {
                "name": third_names[i],
                "value": int(value),
                "fill": rx.color(self.colors[i], 8),
                "stroke": None,
            }
            for i, (value, _) in enumerate(thirds)
            if value
        ]

    @rx.event
    def on_load(self):
        if not self.match_stats:
            return
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
        data = thirds_stats(team1_stats)
        self.team1_thirds_pie = self._to_pie_data_thirds(data)
        self.team1_thirds_quality = [int(el[1] * 100) for el in data]
        data = thirds_stats(team2_stats)
        self.team2_thirds_pie = self._to_pie_data_thirds(data)
        self.team2_thirds_quality = [int(el[1] * 100) for el in data]
