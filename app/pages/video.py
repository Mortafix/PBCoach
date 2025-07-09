import reflex as rx
from app.components.extra import page_link, page_title
from app.components.input import btn_icon, btn_text_icon
from app.pages.extra import match_not_found
from app.states.overview import OverviewState
from app.states.video import VideoState
from app.templates import template


def no_video() -> rx.Component:
    return rx.vstack(
        rx.callout("Mi dispiace, ma il video non è presente..", icon="frown", size="2"),
        width="100%",
    )


def scoreboard() -> rx.Component:
    players = VideoState.players_description.split(" VS ")
    score = VideoState.current_score
    return rx.vstack(
        rx.hstack(
            rx.text(players[0]),
            rx.code(
                score[0], color_scheme=rx.cond(score[0] > score[1], "green", "gray")
            ),
            align="center",
            justify="between",
            width="100%",
            padding_bottom="0.2rem",
            border_bottom="1px solid #FFFFFF6a",
        ),
        rx.hstack(
            rx.text(players[1]),
            rx.code(
                score[1], color_scheme=rx.cond(score[1] > score[0], "green", "gray")
            ),
            align="center",
            justify="between",
            width="100%",
        ),
        spacing="1",
        width="max-content",
    )


def highlight_button(data):
    return btn_text_icon(
        data[2],
        data[1],
        icon_size=18,
        icon_w=1.5,
        spacing="2",
        variant="solid",
        on_click=lambda: VideoState.go_to_rally(data[0]),
    )


@template(
    title="Video",
    route="/[match_id]/video",
    on_load=[OverviewState.on_load, VideoState.on_load],
    description="Video della partita",
)
def video_page():
    video_id = VideoState.match.video_id
    video_player = rx.vstack(
        rx.cond(
            VideoState.is_sidebar_open,
            page_title("video", "Video della Partita"),
            page_title("video", f"Video della Partita • {VideoState.match.name}"),
        ),
        rx.box(
            rx.cond(
                VideoState.show_scoreboard,
                rx.box(
                    scoreboard(),
                    bg="#000000bf",
                    position="absolute",
                    top="0.5rem",
                    left="0.5rem",
                    z_index=4,
                    padding="0.15rem 0.6rem",
                ),
            ),
            rx.video(
                id="match-video",
                url=f"https://stream.mux.com/{video_id}.m3u8?redundant_streams=true",
                width="100%",
                controls=True,
                playing=True,
                on_progress=VideoState.on_progress,
            ),
            width="100%",
            position="relative",
        ),
        rx.hstack(
            rx.hstack(
                btn_icon(
                    "chevron-left",
                    variant="soft",
                    disabled=VideoState.is_first_rally,
                    on_click=VideoState.prev_rally,
                ),
                rx.text("Rally ", rx.code(VideoState.current_rally)),
                btn_icon(
                    "chevron-right",
                    variant="soft",
                    disabled=VideoState.is_last_rally,
                    on_click=VideoState.next_rally,
                ),
                align="center",
            ),
            rx.hstack(
                rx.hstack(
                    rx.text("Punteggio"),
                    rx.switch(
                        size="3",
                        color_scheme="green",
                        cursor="pointer",
                        checked=VideoState.show_scoreboard,
                        on_change=VideoState.set_show_scoreboard,
                    ),
                    align="center",
                    padding="0.25rem 0.5rem",
                    border_radius="0.5rem",
                    bg=rx.color_mode_cond("#f3f3f3", "#18191b"),
                ),
                rx.hstack(
                    rx.text("Solo partita"),
                    rx.switch(
                        size="3",
                        color_scheme="green",
                        cursor="pointer",
                        checked=VideoState.skipping,
                        on_change=VideoState.set_skipping,
                    ),
                    align="center",
                    padding="0.25rem 0.5rem",
                    border_radius="0.5rem",
                    bg=rx.color_mode_cond("#f3f3f3", "#18191b"),
                ),
                align="center",
                justify="center",
                wrap="wrap",
            ),
            width="100%",
            justify_content=[
                "center",
                "space-between",
                "space-between",
                "space-between",
            ],
            wrap="wrap",
        ),
        rx.cond(
            VideoState.highlights,
            rx.vstack(
                rx.divider(),
                rx.hstack(
                    rx.text("Highlights:"),
                    rx.foreach(VideoState.highlights, highlight_button),
                    width="100%",
                    wrap="wrap",
                ),
                width="100%",
            ),
        ),
        rx.divider(),
        rx.hstack(
            page_link("Riepilogo della Partita", f"/{VideoState.match_id}/overview"),
            page_link("Statistiche dei Team", f"/{VideoState.match_id}/team"),
            page_link("Statistiche dei Giocatori", f"/{VideoState.match_id}/players"),
            width="100%",
            wrap="wrap",
        ),
        width="100%",
    )
    return rx.cond(
        VideoState.is_match_found,
        rx.cond(video_id, video_player, no_video()),
        match_not_found(),
    )
