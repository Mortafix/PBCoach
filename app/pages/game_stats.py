import reflex as rx
from app.states.state import State
from app.styles import card_style
from app.templates import template


def player_performance_chart() -> rx.Component:
    is_dark = State.theme == "dark"
    return rx.el.div(
        rx.el.h2(
            "Player Performance",
            class_name="text-xl font-bold mb-4",
        ),
        rx.el.div(
            rx.foreach(
                State.all_players,
                lambda player: rx.el.div(
                    rx.recharts.bar_chart(
                        rx.recharts.bar(
                            data_key=f"p{player['id']}",
                            stack_id="a",
                            fill="#8884d8",
                        ),
                        data=State.performance_data,
                        layout="vertical",
                        bar_category_gap=0,
                        bar_gap=0,
                        width=150,
                        height=200,
                        margin={
                            "top": 0,
                            "right": 0,
                            "bottom": 0,
                            "left": 0,
                        },
                    ),
                    rx.el.div(
                        rx.el.img(
                            src=player["avatar"],
                            class_name="w-12 h-12 rounded-full border-2 border-white shadow-md",
                        ),
                        rx.el.span(
                            player["name"],
                            class_name="mt-2 text-sm font-semibold",
                        ),
                        class_name="flex flex-col items-center",
                    ),
                    class_name="flex flex-col items-center",
                ),
            ),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-4",
        ),
        class_name=card_style(is_dark),
    )


def score_display() -> rx.Component:
    is_dark = State.theme == "dark"
    return rx.el.div(
        rx.el.div(
            rx.foreach(
                State.teams[0]["players"],
                lambda p: rx.el.div(
                    rx.el.img(
                        src=p["avatar"],
                        class_name="w-10 h-10 rounded-full",
                    ),
                    rx.el.span(
                        p["name"],
                        class_name="text-sm font-medium",
                    ),
                    rx.icon(
                        tag="disc_3",
                        size=14,
                        color="#9CA3AF",
                    ),
                    class_name="flex items-center gap-2",
                ),
            ),
            class_name="flex flex-col gap-2 items-start",
        ),
        rx.el.div(
            rx.el.h3(
                "Score",
                class_name="text-sm text-gray-500 dark:text-gray-400",
            ),
            rx.el.div(
                rx.el.span(
                    State.teams[0]["score"],
                    class_name="text-3xl font-bold",
                ),
                rx.el.span(
                    "-",
                    class_name="text-3xl font-bold text-gray-300 dark:text-gray-600",
                ),
                rx.el.span(
                    State.teams[1]["score"],
                    class_name="text-3xl font-bold",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex flex-col items-center",
        ),
        rx.el.div(
            rx.foreach(
                State.teams[1]["players"],
                lambda p: rx.el.div(
                    rx.icon(
                        tag="disc_3",
                        size=14,
                        color="#9CA3AF",
                    ),
                    rx.el.span(
                        p["name"],
                        class_name="text-sm font-medium",
                    ),
                    rx.el.img(
                        src=p["avatar"],
                        class_name="w-10 h-10 rounded-full",
                    ),
                    class_name="flex items-center gap-2 justify-end",
                ),
            ),
            class_name="flex flex-col gap-2 items-end",
        ),
        class_name=rx.cond(
            is_dark,
            "flex justify-between items-center bg-gray-800 rounded-xl shadow-lg p-6 w-full text-gray-200",
            "flex justify-between items-center bg-white rounded-xl shadow-lg p-6 w-full text-gray-800",
        ),
    )


def data_nerds_section() -> rx.Component:
    is_dark = State.theme == "dark"
    button_class = rx.cond(
        is_dark,
        "bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-sm font-semibold hover:bg-gray-600 flex items-center gap-2",
        "bg-white border border-gray-300 rounded-lg px-4 py-2 text-sm font-semibold hover:bg-gray-50 flex items-center gap-2",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "For data nerds only",
                class_name="font-bold",
            ),
            rx.el.p(
                "Access advanced stats! Download an Excel or Raw data file for any video."
            ),
        ),
        rx.el.div(
            rx.el.button(
                "Download Excel Data",
                on_click=State.download_excel,
                class_name=button_class,
            ),
            rx.el.button(
                "Download Raw Data",
                on_click=State.download_raw_data,
                class_name=button_class,
            ),
            class_name="flex flex-col sm:flex-row gap-2",
        ),
        class_name=rx.cond(
            is_dark,
            "flex flex-col md:flex-row justify-between items-center gap-4 bg-gray-800 rounded-xl shadow-lg p-6 w-full text-gray-200",
            "flex flex-col md:flex-row justify-between items-center gap-4 bg-white rounded-xl shadow-lg p-6 w-full text-gray-800",
        ),
    )


def summary_stats() -> rx.Component:
    is_dark = State.theme == "dark"
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Total Rallies",
                class_name="text-sm text-gray-500 dark:text-gray-400",
            ),
            rx.el.h3("53", class_name="text-2xl font-bold"),
            class_name="text-center",
        ),
        rx.el.div(
            rx.el.p(
                "Kitchen Rallies",
                class_name="text-sm text-gray-500 dark:text-gray-400",
            ),
            rx.el.h3("18", class_name="text-2xl font-bold"),
            class_name="text-center",
        ),
        rx.el.div(
            rx.el.p(
                "Avg Shots per Rally",
                class_name="text-sm text-gray-500 dark:text-gray-400",
            ),
            rx.el.h3("5.57", class_name="text-2xl font-bold"),
            class_name="text-center",
        ),
        rx.el.div(
            rx.el.p(
                "Longest Rally",
                class_name="text-sm text-gray-500 dark:text-gray-400",
            ),
            rx.el.h3("19 shots", class_name="text-2xl font-bold"),
            class_name="text-center",
        ),
        class_name=rx.cond(
            is_dark,
            "grid grid-cols-2 md:grid-cols-4 gap-4 bg-gray-800 rounded-xl shadow-lg p-6 w-full text-gray-200",
            "grid grid-cols-2 md:grid-cols-4 gap-4 bg-white rounded-xl shadow-lg p-6 w-full text-gray-800",
        ),
    )


@template(
    route="/[match_id]/game",
    title="Statistiche Partita",
    # on_load=ActivationState.on_load,
)
def game_stats_page() -> rx.Component:
    return rx.vstack(
        player_performance_chart(),
        score_display(),
        data_nerds_section(),
        summary_stats(),
        width="100%",
        spacing="5",
    )
