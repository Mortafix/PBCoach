import reflex as rx
from app.components.pickleball_court import pickleball_court_svg
from app.states.state import State
from app.styles import card_style
from app.templates import template


def court_arrival_view(title: str, data_key: str) -> rx.Component:
    is_dark = State.theme == "dark"
    return rx.el.div(
        rx.el.h3(
            title,
            class_name="text-lg font-bold text-center mb-4",
        ),
        pickleball_court_svg(data_key),
        class_name=card_style(is_dark),
    )


def distribution_bar(
    label: str,
    team_a_val: rx.Var[int],
    team_b_val: rx.Var[int],
) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            label,
            class_name="w-1/4 text-sm font-medium text-gray-600 dark:text-gray-300",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    f"{team_a_val}%",
                    class_name="text-white font-bold text-sm text-right pr-2",
                ),
                style={"width": team_a_val.to_string() + "%"},
                class_name="bg-blue-500 h-full rounded-l-md",
            ),
            rx.el.div(
                rx.el.div(
                    f"{100 - team_a_val}%",
                    class_name="text-gray-700 font-bold text-sm text-left pl-2",
                ),
                style={"width": (100 - team_a_val).to_string() + "%"},
                class_name="bg-cyan-300 h-full rounded-r-md",
            ),
            class_name="w-full flex h-8 rounded-md",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    f"{team_b_val}%",
                    class_name="text-white font-bold text-sm text-right pr-2",
                ),
                style={"width": team_b_val.to_string() + "%"},
                class_name="bg-yellow-400 h-full rounded-l-md",
            ),
            rx.el.div(
                rx.el.div(
                    f"{100 - team_b_val}%",
                    class_name="text-gray-700 font-bold text-sm text-left pl-2",
                ),
                style={"width": (100 - team_b_val).to_string() + "%"},
                class_name="bg-orange-400 h-full rounded-r-md",
            ),
            class_name="w-full flex h-8 rounded-md",
        ),
        class_name="flex items-center gap-4 w-full",
    )


@template(
    route="/[match_id]/team",
    title="Statistiche Team",
    # on_load=ActivationState.on_load,
)
def team_stats_page() -> rx.Component:
    is_dark = State.theme == "dark"
    dist = State.team_stats_data["shot_distribution"]
    return rx.el.div(
        court_arrival_view(
            "Kitchen Arrival: When Serving",
            "kitchen_arrival_serving",
        ),
        court_arrival_view(
            "Kitchen Arrival: When Returning",
            "kitchen_arrival_returning",
        ),
        rx.el.div(
            rx.el.h3(
                "Shot Distribution and Stacking",
                class_name="text-lg font-bold mb-4",
            ),
            distribution_bar(
                "Shot Distribution",
                dist["shot_distribution"][0]["team_a"],
                dist["shot_distribution"][0]["team_b"],
            ),
            distribution_bar(
                "Left side",
                dist["left_side"][0]["team_a"],
                dist["left_side"][0]["team_b"],
            ),
            distribution_bar(
                "Speedups",
                dist["speedups"][0]["team_a"],
                dist["speedups"][0]["team_b"],
            ),
            class_name=rx.cond(
                is_dark,
                "flex flex-col gap-4 bg-gray-800 rounded-xl shadow-lg p-6 w-full text-gray-200",
                "flex flex-col gap-4 bg-white rounded-xl shadow-lg p-6 w-full text-gray-800",
            ),
        ),
        class_name="flex flex-col gap-8",
    )
