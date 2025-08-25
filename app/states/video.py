from os import path, remove
from tempfile import NamedTemporaryFile

import reflex as rx
from app.database.data import highlights_icons, highlights_name_italian
from app.database.video import download_clip
from app.states.overview import OverviewState
from reflex.utils.format import format_ref


class VideoState(OverviewState):
    current_seconds: float = 0
    show_scoreboard: bool = True
    with_score: bool = True
    skipping: bool = True
    rallies_score: list[tuple[int, int]] = []
    rallies: list[tuple[float, float]] = []
    skip_segments: list[tuple[float, float]] = []
    highlights: list[tuple[int, str, str]] = []
    video_downloading: bool = False

    @rx.event
    def on_load(self):
        self.current_seconds = 0
        self.video_downloading = False
        self.rallies_score = [
            tuple(rally_score)
            for rally in self.match_insights.get("rallies")
            if (rally_score := rally.get("scoring_info", {}).get("running_score"))
        ]
        self.with_score = True
        if not self.rallies_score:
            self.with_score = False
        self.rallies = [
            (rally.get("start_ms") / 1000, rally.get("end_ms") / 1000)
            for rally in self.match_insights.get("rallies")
        ]
        # skip segments
        self.skip_segments = []
        end_prev = 0
        for start_curr, end_curr in self.rallies:
            skip = (end_prev, start_curr)
            self.skip_segments.append(skip)
            end_prev = end_curr
        # highlights
        self.highlights = []
        highlights_name = {}
        for event in sorted(
            self.match_insights.get("highlights", []),
            key=lambda el: el.get("score"),
            reverse=True,
        ):
            if event.get("score") <= 7:
                continue
            name = highlights_name_italian(event.get("short_description"))
            icon_name = highlights_icons(event.get("short_description"))
            name_idx = highlights_name.get(name, 0) + 1
            highlights_name[name] = highlights_name.get(name, 0) + 1
            highlight = (event.get("rally_idx") + 1, f"{name} #{name_idx}", icon_name)
            self.highlights.append(highlight)
        self.go_to_rally(1)

    @rx.var
    def current_rally(self) -> int:
        for idx, (start_rally, end_rally) in enumerate(self.rallies, 1):
            if self.current_seconds < start_rally:
                return idx - 1
            if start_rally <= self.current_seconds < end_rally:
                return idx
        return len(self.rallies)

    @rx.var
    def current_score(self) -> tuple[int, int]:
        if not self.rallies_score:
            return (0, 0)
        return self.rallies_score[max(self.current_rally - 1, 0)]

    @rx.event
    def on_progress(self, progress):
        if not self.skipping:
            return
        self.current_seconds = progress.get("playedSeconds", 0)
        for start, end in self.skip_segments:
            if start <= self.current_seconds < end:
                return self.go_to(end)

    @rx.event
    def go_to(self, seconds: float):
        return rx.run_script(
            rx.Var(format_ref("match-video"))
            ._as_ref()
            .to(dict)
            .current.to(dict)
            .seekTo.to(rx.vars.FunctionVar)
            .call(seconds)
        )

    # ---- rally controls

    @rx.var
    def is_first_rally(self) -> bool:
        return self.current_rally <= 1

    @rx.var
    def is_last_rally(self) -> bool:
        return self.current_rally >= len(self.rallies)

    @rx.event
    def next_rally(self):
        if self.current_rally >= len(self.rallies):
            return
        start_next_rally = self.rallies[self.current_rally][0]
        return self.go_to(start_next_rally)

    @rx.event
    def prev_rally(self):
        if self.current_rally <= 1:
            return
        start_prev_rally = self.rallies[self.current_rally - 2][0]
        return self.go_to(start_prev_rally)

    @rx.event
    def go_to_rally(self, rally_n):
        start_rally = self.rallies[max(rally_n - 1, 0)][0]
        return self.go_to(start_rally)

    # ---- video download

    @rx.event(background=True)
    async def download_rally(self):
        async with self:
            self.video_downloading = True
        start, end = self.rallies[max(self.current_rally - 1, 0)]
        temp_f = NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_f.close()
        await download_clip(self.match.video_id, start - 5, end + 3, temp_f.name)
        with open(temp_f.name, "rb") as f:
            video_bytes = f.read()
        match_name = self.match.name.lower().replace(" ", "_")
        filename = f"{match_name}-rally#{self.current_rally}"
        yield rx.download(data=video_bytes, filename=f"{filename}.mp4")
        async with self:
            self.video_downloading = False
        if path.exists(temp_f.name):
            remove(temp_f.name)
