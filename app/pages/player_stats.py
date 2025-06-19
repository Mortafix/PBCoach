import reflex as rx
from app.states.player import PlayerState
from app.states.state import State
from app.styles import card_style
from app.templates import template


def stat_bar(label: str, value: rx.Var[int], color: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            label,
            class_name="text-sm font-medium text-gray-600 dark:text-gray-300",
        ),
        rx.el.div(
            rx.el.div(
                style={
                    "width": value.to_string() + "%",
                    "background_color": color,
                },
                class_name="h-full rounded-full",
            ),
            class_name="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5",
        ),
        rx.el.p(
            value.to_string() + "%",
            class_name="text-sm font-semibold",
        ),
        class_name="flex items-center gap-4",
    )


def speed_stat(title: str, avg: rx.Var[int], top: rx.Var[int]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                title,
                class_name="text-sm font-medium text-gray-600 dark:text-gray-300",
            ),
            rx.el.p(f"{avg} mph", class_name="text-lg font-bold"),
        ),
        rx.el.div(
            rx.el.p(
                "Top",
                class_name="text-xs text-gray-500 dark:text-gray-400",
            ),
            rx.el.p(
                f"{top} mph",
                class_name="text-sm font-semibold",
            ),
        ),
        class_name="flex justify-between items-baseline",
    )


def donut_chart(
    title: str,
    data: rx.Var,
    in_val: rx.Var[int],
    total_val: rx.Var[int],
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(title, class_name="font-semibold"),
            rx.el.p(
                f"Total: {total_val}",
                class_name="text-sm text-gray-500 dark:text-gray-400",
            ),
            class_name="flex justify-between w-full",
        ),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                rx.recharts.cell(fill="#22C55E"),
                rx.recharts.cell(fill="#EF4444"),
                data=data,
                data_key="value",
                name_key="name",
                inner_radius="60%",
                outer_radius="80%",
                padding_angle=5,
                stroke="none",
            ),
            rx.recharts.legend(),
            width=200,
            height=200,
        ),
        class_name="flex flex-col gap-2 items-center",
    )


@template(
    route="/[match_id]/player/[player]",
    title="Statistiche Giocatore",
    # on_load=ActivationState.on_load,
)
def player_stats_page() -> rx.Component:
    is_dark = State.theme == "dark"
    player = State.get_player_by_id
    stats = State.get_player_stats_by_id
    return rx.cond(
        stats,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.img(
                            src=player["avatar"],
                            class_name="w-12 h-12 rounded-full",
                        ),
                        rx.el.h2(
                            PlayerState.player,
                            class_name="text-2xl font-bold",
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    rx.el.p(
                        f"Total Shots: {stats['total_shots']}",
                        class_name="font-medium",
                    ),
                    class_name="flex justify-between items-center",
                ),
                stat_bar(
                    "Shot Accuracy",
                    stats["shot_accuracy"],
                    "#22C55E",
                ),
                speed_stat(
                    "Serve",
                    stats["avg_serve_speed"],
                    stats["top_serve_speed"],
                ),
                speed_stat(
                    "Drive",
                    stats["avg_drive_speed"],
                    stats["top_drive_speed"],
                ),
                class_name=card_style(is_dark) + " flex flex-col gap-4",
            ),
            rx.el.div(
                rx.el.img(
                    src="/placeholder.svg",
                    class_name="w-full h-auto object-cover rounded-xl bg-gray-200",
                ),
                class_name=card_style(is_dark),
            ),
            rx.el.div(
                rx.el.h3(
                    "Court Coverage",
                    class_name="text-lg font-bold mb-2",
                ),
                rx.el.img(
                    src="/placeholder.svg",
                    class_name="w-full h-auto object-cover rounded-xl bg-gray-200",
                ),
                class_name=card_style(is_dark),
            ),
            rx.el.div(
                rx.el.h3(
                    "Serves & Returns",
                    class_name="text-lg font-bold mb-4 w-full text-center",
                ),
                rx.el.div(
                    donut_chart(
                        "Serves In / Out",
                        stats["serve_depth_data"],
                        stats["serves_in"],
                        stats["serves_total"],
                    ),
                    donut_chart(
                        "Returns In / Out",
                        stats["return_depth_data"],
                        stats["returns_in"],
                        stats["returns_total"],
                    ),
                    class_name="flex flex-col md:flex-row justify-around w-full",
                ),
                class_name=card_style(is_dark) + " flex flex-col items-center",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-8",
        ),
        rx.el.div(
            rx.el.p("Select a player to see their stats."),
            class_name="flex items-center justify-center h-full",
        ),
    )
