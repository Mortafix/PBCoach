from typing import Literal, TypedDict, cast

import reflex as rx


class Player(TypedDict):
    id: int
    name: str
    avatar: str


class Team(TypedDict):
    id: int
    name: str
    players: list[Player]
    score: int


class RallyHighlight(TypedDict):
    name: str
    type: str
    timestamp: int


class Shot(TypedDict):
    time: str
    type: str
    speed: str
    player_avatar: str
    timestamp: int


class Rally(TypedDict):
    name: str
    shots: list[Shot]


class PlayerPerformance(TypedDict):
    name: str
    p1: int
    p2: int
    p3: int
    p4: int


class DepthData(TypedDict):
    name: str
    value: int


class PlayerDetailStats(TypedDict):
    id: int
    name: str
    total_shots: int
    shot_accuracy: int
    avg_serve_speed: int
    top_serve_speed: int
    avg_drive_speed: int
    top_drive_speed: int
    serves_in: int
    serves_total: int
    returns_in: int
    returns_total: int
    serve_depth_data: list[DepthData]
    return_depth_data: list[DepthData]


class KitchenArrivalStat(TypedDict):
    player: int
    value: int


class ShotDistributionDetail(TypedDict):
    team_a: int
    team_b: int


class ShotDistribution(TypedDict):
    shot_distribution: list[ShotDistributionDetail]
    left_side: list[ShotDistributionDetail]
    speedups: list[ShotDistributionDetail]


class TeamStatsData(TypedDict):
    kitchen_arrival_serving: list[KitchenArrivalStat]
    kitchen_arrival_returning: list[KitchenArrivalStat]
    shot_distribution: ShotDistribution


class State(rx.State):
    """The application state."""

    active_page: str = "Home"
    theme: Literal["light", "dark"] = "light"
    sidebar_open: bool = False
    teams: list[Team] = [
        {
            "id": 1,
            "name": "Team A",
            "score": 8,
            "players": [
                {
                    "id": 1,
                    "name": "Player 1",
                    "avatar": "https://api.dicebear.com/9.x/initials/svg?seed=Player 1",
                },
                {
                    "id": 2,
                    "name": "Player 2",
                    "avatar": "https://api.dicebear.com/9.x/initials/svg?seed=Player 2",
                },
            ],
        },
        {
            "id": 2,
            "name": "Team B",
            "score": 11,
            "players": [
                {
                    "id": 3,
                    "name": "Player 3",
                    "avatar": "https://api.dicebear.com/9.x/initials/svg?seed=Player 3",
                },
                {
                    "id": 4,
                    "name": "Player 4",
                    "avatar": "https://api.dicebear.com/9.x/initials/svg?seed=Player 4",
                },
            ],
        },
    ]
    selected_player_id: int = 1
    highlights: list[RallyHighlight] = [
        {
            "name": "Long Rally #1",
            "type": "rally",
            "timestamp": 10,
        },
        {
            "name": "Poach #1",
            "type": "poach",
            "timestamp": 25,
        },
        {
            "name": "Poach #2",
            "type": "poach",
            "timestamp": 40,
        },
        {
            "name": "Long Rally #2",
            "type": "rally",
            "timestamp": 55,
        },
        {
            "name": "Long Rally #3",
            "type": "rally",
            "timestamp": 70,
        },
    ]
    rallies: list[Rally] = [
        {
            "name": "Rally #1",
            "shots": [
                {
                    "time": "00:01",
                    "type": "Serve",
                    "speed": "83 mph",
                    "player_avatar": "https://api.dicebear.com/9.x/initials/svg?seed=Player 1",
                    "timestamp": 1,
                },
                {
                    "time": "00:02",
                    "type": "Return",
                    "speed": "67 mph",
                    "player_avatar": "https://api.dicebear.com/9.x/initials/svg?seed=Player 3",
                    "timestamp": 2,
                },
                {
                    "time": "00:03",
                    "type": "Unknown",
                    "speed": "",
                    "player_avatar": "https://api.dicebear.com/9.x/initials/svg?seed=Player 2",
                    "timestamp": 3,
                },
            ],
        },
        {
            "name": "Rally #2",
            "shots": [
                {
                    "time": "00:22",
                    "type": "Serve",
                    "speed": "91 mph",
                    "player_avatar": "https://api.dicebear.com/9.x/initials/svg?seed=Player 1",
                    "timestamp": 22,
                },
                {
                    "time": "00:24",
                    "type": "Return",
                    "speed": "67 mph",
                    "player_avatar": "https://api.dicebear.com/9.x/initials/svg?seed=Player 4",
                    "timestamp": 24,
                },
                {
                    "time": "00:25",
                    "type": "3rd shot Drop",
                    "speed": "",
                    "player_avatar": "https://api.dicebear.com/9.x/initials/svg?seed=Player 2",
                    "timestamp": 25,
                },
                {
                    "time": "00:26",
                    "type": "Volley Drive",
                    "speed": "78 mph",
                    "player_avatar": "https://api.dicebear.com/9.x/initials/svg?seed=Player 3",
                    "timestamp": 26,
                },
            ],
        },
    ]
    performance_data: list[PlayerPerformance] = [
        {
            "name": "Metric 1",
            "p1": 40,
            "p2": 30,
            "p3": 20,
            "p4": 10,
        },
        {
            "name": "Metric 2",
            "p1": 20,
            "p2": 25,
            "p3": 35,
            "p4": 20,
        },
        {
            "name": "Metric 3",
            "p1": 30,
            "p2": 35,
            "p3": 15,
            "p4": 20,
        },
        {
            "name": "Metric 4",
            "p1": 10,
            "p2": 10,
            "p3": 30,
            "p4": 50,
        },
    ]
    player_stats: list[PlayerDetailStats] = [
        {
            "id": 1,
            "name": "Player 1",
            "total_shots": 62,
            "shot_accuracy": 38,
            "avg_serve_speed": 35,
            "top_serve_speed": 37,
            "avg_drive_speed": 39,
            "top_drive_speed": 52,
            "serves_in": 11,
            "serves_total": 11,
            "returns_in": 10,
            "returns_total": 12,
            "serve_depth_data": [
                {"name": "In", "value": 81},
                {"name": "Out", "value": 19},
            ],
            "return_depth_data": [
                {"name": "In", "value": 48},
                {"name": "Out", "value": 52},
            ],
        },
        {
            "id": 2,
            "name": "Player 2",
            "total_shots": 58,
            "shot_accuracy": 72,
            "avg_serve_speed": 40,
            "top_serve_speed": 45,
            "avg_drive_speed": 42,
            "top_drive_speed": 55,
            "serves_in": 10,
            "serves_total": 11,
            "returns_in": 11,
            "returns_total": 12,
            "serve_depth_data": [
                {"name": "In", "value": 90},
                {"name": "Out", "value": 10},
            ],
            "return_depth_data": [
                {"name": "In", "value": 60},
                {"name": "Out", "value": 40},
            ],
        },
        {
            "id": 3,
            "name": "Player 3",
            "total_shots": 71,
            "shot_accuracy": 55,
            "avg_serve_speed": 38,
            "top_serve_speed": 41,
            "avg_drive_speed": 44,
            "top_drive_speed": 58,
            "serves_in": 9,
            "serves_total": 11,
            "returns_in": 9,
            "returns_total": 12,
            "serve_depth_data": [
                {"name": "In", "value": 75},
                {"name": "Out", "value": 25},
            ],
            "return_depth_data": [
                {"name": "In", "value": 55},
                {"name": "Out", "value": 45},
            ],
        },
        {
            "id": 4,
            "name": "Player 4",
            "total_shots": 65,
            "shot_accuracy": 65,
            "avg_serve_speed": 36,
            "top_serve_speed": 39,
            "avg_drive_speed": 41,
            "top_drive_speed": 53,
            "serves_in": 11,
            "serves_total": 11,
            "returns_in": 12,
            "returns_total": 12,
            "serve_depth_data": [
                {"name": "In", "value": 85},
                {"name": "Out", "value": 15},
            ],
            "return_depth_data": [
                {"name": "In", "value": 65},
                {"name": "Out", "value": 35},
            ],
        },
    ]
    team_stats_data: TeamStatsData = {
        "kitchen_arrival_serving": [
            {"player": 1, "value": 35},
            {"player": 2, "value": 31},
            {"player": 3, "value": 48},
            {"player": 4, "value": 52},
        ],
        "kitchen_arrival_returning": [
            {"player": 1, "value": 100},
            {"player": 2, "value": 92},
            {"player": 3, "value": 98},
            {"player": 4, "value": 96},
        ],
        "shot_distribution": {
            "shot_distribution": [
                {"team_a": 57, "team_b": 52},
                {"team_a": 43, "team_b": 48},
            ],
            "left_side": [
                {"team_a": 42, "team_b": 36},
                {"team_a": 58, "team_b": 64},
            ],
            "speedups": [
                {"team_a": 17, "team_b": 17},
                {"team_a": 83, "team_b": 83},
            ],
        },
    }

    def set_active_page(self, page: str):
        self.active_page = page
        self.sidebar_open = False

    def select_player(self, player_id: int):
        self.selected_player_id = player_id
        self.active_page = f"Player {player_id}"
        self.sidebar_open = False

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"

    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    def seek_video(self, time: int):
        return rx.call_script(
            f"document.getElementById('video-player').currentTime = {time}; document.getElementById('video-player').play()"
        )

    @rx.var
    def all_players(self) -> list[Player]:
        return self.teams[0]["players"] + self.teams[1]["players"]

    @rx.var
    def get_player_by_id(self) -> Player | None:
        for p in self.all_players:
            if p["id"] == self.selected_player_id:
                return p
        return None

    @rx.var
    def get_player_stats_by_id(
        self,
    ) -> PlayerDetailStats | None:
        for p_stats in self.player_stats:
            if p_stats["id"] == self.selected_player_id:
                return p_stats
        return None

    @rx.var
    def court_arrival_zones(
        self,
    ) -> dict[str, dict[str, int]]:
        zones = {}
        for key in [
            "kitchen_arrival_serving",
            "kitchen_arrival_returning",
        ]:
            stats_list = cast(
                list[KitchenArrivalStat],
                self.team_stats_data[key],
            )
            zones[key] = {
                "team_a_left": next(
                    (s["value"] for s in stats_list if s["player"] == 1),
                    0,
                ),
                "team_a_right": next(
                    (s["value"] for s in stats_list if s["player"] == 2),
                    0,
                ),
                "team_b_left": next(
                    (s["value"] for s in stats_list if s["player"] == 3),
                    0,
                ),
                "team_b_right": next(
                    (s["value"] for s in stats_list if s["player"] == 4),
                    0,
                ),
            }
        return zones

    @rx.var
    def base_styles(self) -> dict:
        bg_color = "#111827" if self.theme == "dark" else "#F9FAFB"
        color = "#F3F4F6" if self.theme == "dark" else "#1F2937"
        return {"background_color": bg_color, "color": color}

    @rx.event
    def download_excel(self):
        return rx.download(
            data="This is a dummy Excel file.",
            filename="stats.xlsx",
        )

    @rx.event
    def download_raw_data(self):
        return rx.download(
            data="This is a dummy raw data file.",
            filename="raw_data.txt",
        )
