from collections import Counter
from datetime import datetime
from re import split

import reflex as rx
from app.database.data import (AGGRESSIVE_SHOTS, DEFENSIVE_SHOTS,
                               REVERSE_DEEP_SHOTS, SINGLE_SHOTS,
                               calculate_ratings, color_quality_float,
                               shots_name_italian, to_metric)
from app.database.matches import Partita, get_all_matches
from app.database.players import get_player_gender_from_db, get_player_name
from app.database.stats import get_matches_insights, get_matches_stats
from app.states.player_stats import (Shot, shot_stats, to_pie_data_inout,
                                     to_pie_data_multiple)
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
    shots_data: dict[str, Shot]
    serves_kitchen: list[float]
    returns_kitchen: list[float]
    shots_aggressive: int
    shots_defensive: int
    player_type: str
    rallies_total: int
    rallies_won: int
    ratings: dict[str, float]
    ratings_count: int
    # pie data
    pie_matches: list[dict]
    pie_rallies: list[dict]
    pie_shots_type: list[dict]
    pie_shots: list[dict]
    pie_thirds: list[dict]
    pie_hands: list[dict]
    # area chart
    area_quality: list[dict]
    area_accuracy: list[dict[str, int]]
    area_rating: dict[str, list[dict]]
    # bar chart
    bar_kitchen_serves: list[dict]
    bar_kitchen_returns: list[dict]


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


def _unique_names(names):
    names_axis = list()
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
    return names_axis


def to_area_base(names, data, repeat_last=False):
    names_axis: list[str] = _unique_names(names)
    res = [{"name": name, "value": val} for name, val in zip(names_axis, data) if val]
    return res + ([res[-1]] if repeat_last else [])


def to_bar_base(names, data, scale):
    names_axis: list[str] = _unique_names(names)
    return [
        {
            "name": name,
            "value": value,
            "fill": rx.color(color_quality_float(value, scale=scale), 8),
            "stroke": None,
        }
        for name, value in zip(names_axis, data)
    ]


def to_area_accuracy(names, net_data, out_data):
    return [
        {"in": 100 - (round(net) + round(out)), "net": round(net), "out": round(out)}
        for _, net, out in zip(names, net_data, out_data)
    ]


# ---- model


def parse_model(names, matches, won, allenamenti, teammates, data):
    distance = sum(data.get("distance"))
    shots = {
        shot: data.get("shots_type").get(shot)
        for shot in sorted(
            data.get("shots_type"), key=lambda el: -data.get("shots_type").get(el)
        )
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
        shots_data=data.get("aggregate_shots"),
        serves_kitchen=data.get("serves_kitchen"),
        returns_kitchen=data.get("returns_kitchen"),
        shots_aggressive=data.get("shots_aggressive"),
        shots_defensive=data.get("shots_defensive"),
        player_type=(
            "Bilanciato"
            if abs(shots_type_diff / shots_count) < 0.125
            else ["Difensivo", "Aggressivo"][shots_type_diff > 0]
        ),
        rallies_total=data.get("rallies_total"),
        rallies_won=data.get("rallies_won"),
        ratings=data.get("ratings"),
        ratings_count=data.get("ratings_count"),
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
        pie_thirds=to_pie_data_multiple(
            ["blue", "tomato", "plum"],
            data.get("aggregate_shots").get("third_drives"),
            data.get("aggregate_shots").get("third_drops"),
            data.get("aggregate_shots").get("third_lobs"),
        ),
        pie_hands=to_pie_data_multiple(
            ["blue", "tomato"],
            data.get("aggregate_shots").get("forehands"),
            data.get("aggregate_shots").get("backhands"),
        ),
        area_quality=to_area_base(
            names, [round(q * 100) for q in data.get("quality")], repeat_last=True
        ),
        area_accuracy=to_area_accuracy(
            names, data.get("faults_net"), data.get("faults_out")
        ),
        area_rating={
            label: to_area_base(
                data.get("ratings_event"),
                [event.get(label) for event in data.get("ratings_history")],
            )
            for label in data.get("ratings")
        },
        bar_kitchen_serves=to_bar_base(names, data.get("serves_kitchen"), [40, 50, 70]),
        bar_kitchen_returns=to_bar_base(
            names, data.get("returns_kitchen"), [90, 92.5, 96]
        ),
    )


def aggregate_multiple_shots(shots):
    n = len(shots)
    out_p = round(sum(data.out for data in shots) / n)
    net_p = round(sum(data.net for data in shots) / n)
    success_p = max(100 - (out_p + net_p), 0)
    return Shot(
        name=shots[0].name,
        count=sum(data.count for data in shots),
        quality=round(sum(data.quality for data in shots) / n),
        success=success_p,
        out=out_p,
        net=net_p,
        baseline_distance=round(sum(data.baseline_distance for data in shots) / n, 2),
        net_height=int(sum(data.net_height for data in shots) / n),
        speed=round(sum(data.speed for data in shots) / n),
        fastest=max(data.fastest for data in shots),
        is_reverse_deep=shots[0].is_reverse_deep,
        pie_inout=to_pie_data_inout(success_p, out_p, net_p),
    )


# ---- STATE


class PlayerState(State):
    matches: list[Partita] = []
    player_name: str = ""
    base_db_filter: dict = {}
    player: PlayerPage | None
    player_gender: str = ""
    events: list[tuple[str, list[Partita]]]
    events_selected: list[tuple[str, list[Partita]]]
    event_search: str = ""
    event_loading: bool = False
    show_quality_trend: bool = False
    stack_accuracy: bool = True
    keywords: list[str] = []
    current_shot: Shot | None = None
    info_shots: list[Shot] = []
    zero_shots: list[Shot] = []
    current_rating_chart: str = ""

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
    def change_shot(self, shot: Shot):
        self.current_shot = shot

    @rx.event
    def set_event_search(self, value: str):
        self.event_search = value
        self.events = []
        if not value:
            self.events = []
            return
        self.event_loading = True
        yield
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
        self.event_loading = False

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
    def select_rating_chart(self, value):
        self.current_rating_chart = value

    @rx.event
    def on_load(self):
        self.player = None
        yield
        self.current_rating_chart = "Generale"
        self.matches = []
        self.player_gender = ""
        self.show_quality_trend = False
        self.stack_accuracy = True
        self.event_search = ""
        self.events = []
        self.events_selected = []
        self.event_loading = False
        self.keywords = []
        self.build_data()

    @rx.event
    def build_data(self):
        player_id = int(self.player_id)
        self.base_db_filter: dict = {"players_ids": int(self.player_id)}
        self.player_name = get_player_name(player_id)
        self.player_gender = get_player_gender_from_db(player_id)
        matches = [match for _, matches in self.events_selected for match in matches]
        if not matches:
            matches = get_all_matches(self.base_db_filter)
            keywords = Counter(
                word.lower()
                for match in matches
                for word in match.name.split(" ")
                if len(word) > 2
                and not word.isdigit()
                and word not in ("della", "dal", "per")
            )
            self.keywords = [word for word, _ in keywords.most_common(7)]
        self.matches = matches
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
        insights = {
            data.get("code"): data
            for data in get_matches_insights(filters, sort=[("info.date", 1)])
        }
        data = {
            "distance": [],
            "quality": [],
            "finals": [],
            "faults_net": [],
            "faults_out": [],
            "accuracy": [],
            "shots": [],
            "forehands": [],
            "backhands": [],
            "serves_kitchen": [],
            "returns_kitchen": [],
            "ratings": [],
        }
        rallies_won = []
        ratings = []
        ratings_event = []
        rating_match_count = 0
        for stat in stats:
            insight = insights.get(stat.get("code"))
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
                shots[shot] = shot_stats(p_stat, shot, shot in REVERSE_DEEP_SHOTS)
                if shot_accuracy := shots[shot].success:
                    accuracy.append(shot_accuracy)
            data["accuracy"].append(sum(accuracy) / len(accuracy))
            data["shots"].append(shots)
            data["forehands"].append(shot_stats(p_stat, "forehands"))
            data["backhands"].append(shot_stats(p_stat, "backhands"))
            # kitchen
            role_stats = p_stat.get("role_stats")
            serves_d = role_stats.get("serving").get("oneself")
            serves_kitchen_p = serves_d.get("kitchen_arrival") / serves_d.get("total")
            data["serves_kitchen"].append(round(serves_kitchen_p * 100))
            return_d = role_stats.get("receiving").get("oneself")
            returns_kitchen_p = return_d.get("kitchen_arrival") / return_d.get("total")
            data["returns_kitchen"].append(round(returns_kitchen_p * 100))
            # insights
            rallies = [
                rally.get("winning_team") == team_idx
                for rally in insight.get("rallies")
            ]
            rallies_won.extend(rallies)
            p_insight = insight.get("player_data")[player_idx]
            if rating := p_insight.get("trends", {}).get("ratings"):
                ratings.append(calculate_ratings(rating))
                ratings_event.append(stat.get("info").get("name"))
                rating_match_count += 1
        data["ratings_count"] = rating_match_count
        data["ratings_history"] = ratings
        data["ratings_event"] = ratings_event
        data["rallies_total"] = len(rallies_won)
        data["rallies_won"] = sum(rallies_won)
        if ratings:
            ratings_pesato = {
                attr: sum(data.get(attr) * w for w, data in enumerate(ratings, 1))
                / sum(range(1, len(ratings) + 1))
                for attr in ratings[0]
            }
            data["ratings"] = {el: round(val, 1) for el, val in ratings_pesato.items()}
        # aggregate shots
        aggregate_shots = {}
        for shot in SINGLE_SHOTS:
            aggregate_shots[shot] = aggregate_multiple_shots(
                [m_data[shot] for m_data in data.get("shots")]
            )
        aggregate_shots["forehands"] = aggregate_multiple_shots(data.get("forehands"))
        aggregate_shots["backhands"] = aggregate_multiple_shots(data.get("backhands"))
        data["aggregate_shots"] = aggregate_shots
        # shots type
        shots_count = Counter(
            [
                elem
                for single_match_data in data.get("shots", [])
                for shot, single_shot_data in single_match_data.items()
                for elem in [shot] * single_shot_data.count
            ]
        )
        data["shots_type"] = shots_count
        aggressive_shots = sum(shots_count.get(shot, 0) for shot in AGGRESSIVE_SHOTS)
        defensive_shots = sum(shots_count.get(shot, 0) for shot in DEFENSIVE_SHOTS)
        data["shots_aggressive"] = aggressive_shots
        data["shots_defensive"] = defensive_shots
        self.player = parse_model(
            names, matches_n, matches_won, allenamenti_n, teammates, data
        )
        # ---- single shot analysis
        self.current_shot = data["aggregate_shots"]["serves"]
        info_shots = [
            data["aggregate_shots"][shot]
            for shot in SINGLE_SHOTS + ["forehands", "backhands"]
        ]
        self.info_shots = sorted(info_shots, key=lambda el: -el.quality)
        self.zero_shots = [shot for shot in info_shots if shot.count == 0]
