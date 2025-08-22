from collections import Counter
from datetime import datetime
from re import split

import reflex as rx
from app.database.data import (AGGRESSIVE_SHOTS, DEFENSIVE_SHOTS, SINGLE_SHOTS,
                               shots_name_italian, to_metric)
from app.database.matches import Partita, get_all_matches
from app.database.players import get_player_name
from app.database.stats import get_matches_insights, get_matches_stats
from app.templates.base import State


class PlayerPage(rx.Base):
    matches: int
    matches_names: list[str]
    matches_won: int
    allenamenti: int
    teammates: list[tuple[int, int]]
    teammates_name: dict[int, str]
    distance: int
    distance_str: str
    quality: list[float]
    finals: list[float]
    accuracy: list[float]
    faults_net: list[float]
    faults_out: list[float]
    shots: dict[str, int]
    serves_speed: list[float]
    serves_fastest: float
    serves_success: list[float]
    serves_net: list[float]
    serves_out: list[float]
    serves_deep: list[float]
    serves_kitchen: list[float]
    returns_success: list[float]
    returns_net: list[float]
    returns_out: list[float]
    returns_deep: list[float]
    returns_kitchen: list[float]
    shots_aggressive: int
    shots_defensive: int
    player_type: str
    rallies_total: int
    rallies_won: int
    # pie data
    pie_matches: list[dict]
    pie_rallies: list[dict]
    pie_shots_type: list[dict]
    pie_shots: list[dict]
    # area chart
    area_quality: list[dict]
    area_accuracy: list[dict[str, int]]


def to_pie_base(green_data, red_data, labels, colors=["green", "red"]):
    return [
        {
            "name": labels[i],
            "value": value,
            "fill": rx.color(colors[i], 8),
            "stroke": None,
        }
        for i, value in enumerate([green_data, red_data])
        if value
    ]


def to_pie_shot(shots):
    data = [
        shot
        for shot, value in shots.items()
        if value
        and shot not in ("serves", "returns", "passing")
        and "third" not in shot
    ]
    return [
        {
            "name": shots_name_italian(shot, str_type=True),
            "value": shots.get(shot),
            "fill": rx.color("crimson" if shot in DEFENSIVE_SHOTS else "indigo", 8),
            "stroke": None,
        }
        for i, shot in enumerate(data)
    ]


def to_area_base(names, data):
    names_axis: list[str] = list()
    already_seen = list()
    for name in names:
        unique_name = name
        if name in already_seen:
            count = already_seen.count(name)
            if count == 1:
                names_axis[already_seen.index(name)] += " (1)"
            unique_name = f"{name} ({count + 1})"
        names_axis.append(unique_name)
        already_seen.append(name)
    res = [{"name": name, "value": val} for name, val in zip(names_axis, data) if val]
    return res + [res[-1]]


def to_area_accuracy(names, net_data, out_data):
    return [
        {"in": 100 - (round(net) + round(out)), "net": round(net), "out": round(out)}
        for _, net, out in zip(names, net_data, out_data)
    ]


# ---- model


def parse_model(names, matches, won, allenamenti, teammates, data):
    distance = sum(data.get("distance"))
    shots = {
        shot: data.get("shots").get(shot)
        for shot in sorted(data.get("shots"), key=lambda el: -data.get("shots").get(el))
    }
    shots_count = data.get("shots_aggressive") + data.get("shots_defensive")
    shots_type_diff = data.get("shots_aggressive") - data.get("shots_defensive")
    return PlayerPage(
        matches=matches,
        matches_names=names,
        matches_won=sum(won),
        allenamenti=allenamenti,
        teammates=[
            (player, teammates.get(player))
            for player in sorted(teammates, key=lambda el: (-teammates.get(el), el))[:3]
        ],
        teammates_name={player: get_player_name(player) for player in teammates},
        distance=distance,
        distance_str=(
            f"{distance/1000:.2f} km" if distance > 1000 else f"{distance:.0f} m"
        ),
        quality=data.get("quality"),
        finals=data.get("finals"),
        accuracy=data.get("accuracy"),
        faults_net=data.get("faults_net"),
        faults_out=data.get("faults_out"),
        shots=shots,
        serves_speed=data.get("serves_speed"),
        serves_fastest=data.get("serves_fastest"),
        serves_success=data.get("serves_success"),
        serves_net=data.get("serves_net"),
        serves_out=data.get("serves_out"),
        serves_deep=data.get("serves_deep"),
        serves_kitchen=data.get("serves_kitchen"),
        returns_success=data.get("returns_success"),
        returns_net=data.get("returns_net"),
        returns_out=data.get("returns_out"),
        returns_deep=data.get("returns_deep"),
        returns_kitchen=data.get("returns_kitchen"),
        shots_aggressive=data.get("shots_aggressive"),
        shots_defensive=data.get("shots_defensive"),
        player_type=(
            "Bilanciato"
            if shots_type_diff / shots_count < 0.1
            else ["Difensivo", "Aggressivo"][shots_type_diff > 0]
        ),
        rallies_total=data.get("rallies_total"),
        rallies_won=data.get("rallies_won"),
        pie_matches=to_pie_base(
            sum(won), matches - sum(won), ["Vittoria", "Sconfitta"]
        ),
        pie_rallies=to_pie_base(
            data.get("rallies_won"),
            data.get("rallies_total") - data.get("rallies_won"),
            ["Vinti", "Persi"],
        ),
        pie_shots_type=to_pie_base(
            data.get("shots_aggressive"),
            data.get("shots_defensive"),
            ["Aggressivi", "Difensivi"],
            colors=["indigo", "crimson"],
        ),
        pie_shots=to_pie_shot(shots),
        area_quality=to_area_base(names, [round(q * 100) for q in data.get("quality")]),
        area_accuracy=to_area_accuracy(
            names, data.get("faults_net"), data.get("faults_out")
        ),
    )


# ---- STATE


class PlayerState(State):
    player_name: str = ""
    base_db_filter: dict = {}
    player: PlayerPage = None
    events: list[tuple[str, list[Partita]]]
    events_selected: list[tuple[str, list[Partita]]]
    event_search: str = ""
    show_quality_trend: bool = False
    stack_accuracy: bool = True

    def _get_unique_events(self, all_events):
        unique_event, prev_date, prev_norm = list(), datetime.min, ""
        for match in all_events:
            base_name = split(r"[-|]", match.name)[0].strip()
            day_in_s = 24 * 60 * 60
            if (
                not prev_norm
                or base_name != prev_norm
                or (match.date - prev_date).total_seconds() > day_in_s
            ):
                unique_event.append((base_name, [match]))
                prev_norm = base_name
                prev_date = match.date
            else:
                unique_event[-1][1].append(match)

        return unique_event

    @rx.event
    def set_event_search(self, value: str):
        self.events = []
        if not value:
            self.events = []
            return
        self.event_search = value
        matches_found = get_all_matches(
            self.base_db_filter
            | {
                "info.type": {"$ne": "Allenamento"},
                "info.name": {"$regex": f"(?i){value}"},
            }
        )
        for event in self._get_unique_events(matches_found):
            if event not in self.events_selected:
                self.events.append(event)

    @rx.event
    def add_event(self, event_idx: int):
        self.events_selected.append(self.events.pop(event_idx))
        self.build_data()
        if not self.events:
            self.event_search = ""

    @rx.event
    def remove_event(self, event_selected_ix: int):
        self.events_selected.pop(event_selected_ix)
        self.build_data()

    @rx.event
    def remove_all_events(self):
        self.events_selected = []
        self.events = []
        self.event_search = ""
        self.build_data()

    @rx.event
    def set_quality_trend(self, value: bool):
        self.show_quality_trend = value

    @rx.event
    def set_accuracy_stack(self, value: bool):
        self.stack_accuracy = value

    @rx.event
    def on_load(self):
        self.show_quality_trend = False
        self.stack_accuracy = True
        self.event_search = ""
        self.events = []
        self.events_selected = []
        self.build_data()

    @rx.event
    def build_data(self):
        player_id = int(self.player_id)
        self.base_db_filter: dict = {"players_ids": int(self.player_id)}
        self.player_name = get_player_name(player_id)
        matches = [match for _, matches in self.events_selected for match in matches]
        if not matches:
            matches = get_all_matches(self.base_db_filter)
        allenamenti_n = sum(match.is_allenamento for match in matches)
        matches_n = len(matches) - allenamenti_n
        teammates_history = [
            match.players_ids[idx]
            for match in matches
            for idx in (
                match.team1_idx
                if match.players_ids.index(player_id) in match.team1_idx
                else match.team2_idx
            )
            if match.is_double and match.players_ids[idx] != player_id
        ]
        teammates = Counter(teammates_history)
        matches_won = [
            (
                match.win_team1
                if match.players_ids.index(player_id) in match.team1_idx
                else match.win_team2
            )
            for match in matches
            if not match.is_allenamento
        ]
        names = [match.name for match in matches]
        # stats (sorted)
        codes = [match.code for match in matches if not match.is_allenamento]
        filters = {"code": {"$in": codes}}
        stats = get_matches_stats(filters, sort=[("info.date", 1)])
        insights = get_matches_insights(filters, sort=[("info.date", 1)])
        data = {
            "distance": [],
            "quality": [],
            "finals": [],
            "faults_net": [],
            "faults_out": [],
            "accuracy": [],
            "shots": [],
            "serves_speed": [],
            "serves_success": [],
            "serves_net": [],
            "serves_out": [],
            "serves_deep": [],
            "serves_kitchen": [],
            "returns_success": [],
            "returns_net": [],
            "returns_out": [],
            "returns_deep": [],
            "returns_kitchen": [],
        }
        for stat in stats:
            player_idx = stat.get("players_ids").index(player_id)
            if len(stat.get("players_ids")) == 2 and player_idx == 1:
                player_idx = 2
            team_idx = 0 if player_idx in [0, 1] else 1
            p_stat = stat.get("players")[player_idx]
            data["distance"].append(to_metric(p_stat.get("total_distance_covered")))
            data["quality"].append(p_stat.get("average_shot_quality"))
            data["finals"].append(
                p_stat.get("final_shot_count") / p_stat.get("shot_count")
            )
            data["faults_net"].append(p_stat.get("net_fault_percentage"))
            data["faults_out"].append(p_stat.get("out_fault_percentage"))
            accuracy = []
            shots = {}
            for shot in SINGLE_SHOTS:
                shot_data = p_stat.get(shot)
                shots[shot] = shot_data.get("count")
                outcome = shot_data.get("outcome_stats", {})
                shot_acc = outcome.get("success_percentage", 0)
                if not shot_acc:
                    continue
                accuracy.append(shot_acc)
            data["accuracy"].append(sum(accuracy) / len(accuracy))
            data["shots"].append(shots)
            serve_data = p_stat.get("serves")
            serve_speed_data = serve_data.get("speed_stats")
            data["serves_speed"].append(
                to_metric(serve_speed_data.get("average"), velocity=True)
            )
            data["serves_fastest"] = max(
                to_metric(serve_speed_data.get("fastest"), velocity=True),
                data.get("serves_fastest", 0),
            )
            serve_outcome = serve_data.get("outcome_stats")
            data["serves_success"].append(serve_outcome.get("success_percentage"))
            data["serves_out"].append(serve_outcome.get("out_fault_percentage"))
            data["serves_net"].append(serve_outcome.get("net_fault_percentage"))
            data["serves_deep"].append(
                to_metric(serve_data.get("average_baseline_distance"))
            )
            return_data = p_stat.get("returns")
            return_outcome = return_data.get("outcome_stats")
            data["returns_success"].append(return_outcome.get("success_percentage"))
            data["returns_out"].append(return_outcome.get("out_fault_percentage"))
            data["returns_net"].append(return_outcome.get("net_fault_percentage"))
            data["returns_deep"].append(
                to_metric(return_data.get("average_baseline_distance"))
            )
            role_stats = p_stat.get("role_stats")
            serve_kitchen = role_stats.get("serving").get("oneself")
            data["serves_kitchen"].append(
                serve_kitchen.get("kitchen_arrival") / serve_kitchen.get("total")
            )
            return_kitchen = role_stats.get("receiving").get("oneself")
            data["returns_kitchen"].append(
                return_kitchen.get("kitchen_arrival") / return_kitchen.get("total")
            )
        shots_count = Counter(
            [
                elem
                for shot_data in data.get("shots", [])
                for shot, count in shot_data.items()
                for elem in [shot] * count
            ]
        )
        data["shots"] = shots_count
        aggressive_shots = sum(shots_count.get(shot, 0) for shot in AGGRESSIVE_SHOTS)
        defensive_shots = sum(shots_count.get(shot, 0) for shot in DEFENSIVE_SHOTS)
        data["shots_aggressive"] = aggressive_shots
        data["shots_defensive"] = defensive_shots
        # insights (sorted)
        rallies_won = []
        for insight in insights:
            rallies = [
                rally.get("winning_team") == team_idx
                for rally in insight.get("rallies")
            ]
            rallies_won.extend(rallies)
        data["rallies_total"] = len(rallies_won)
        data["rallies_won"] = sum(rallies_won)
        self.player = parse_model(
            names, matches_n, matches_won, allenamenti_n, teammates, data
        )
