import reflex as rx
from app.states.state import State
from app.styles import card_style
from app.templates import template


def shot_item(shot: rx.Var[dict]) -> rx.Component:
    is_dark = State.theme == "dark"
    return rx.el.div(
        rx.el.img(
            src=shot["player_avatar"],
            class_name="w-8 h-8 rounded-full",
        ),
        rx.el.div(
            rx.el.p(
                shot["time"],
                class_name="text-xs text-gray-500 dark:text-gray-400",
            ),
            rx.el.p(shot["type"], class_name="font-semibold"),
        ),
        rx.el.div(flex_grow=1),
        rx.el.span(
            shot["speed"],
            class_name="text-sm font-medium text-blue-600 dark:text-blue-400",
        ),
        rx.icon(tag="fold_vertical", size=20, color="#6B7280"),
        class_name=rx.cond(
            is_dark,
            "flex items-center gap-4 p-2 rounded-lg hover:bg-gray-700 cursor-pointer",
            "flex items-center gap-4 p-2 rounded-lg hover:bg-gray-100 cursor-pointer",
        ),
        on_click=State.seek_video(shot["timestamp"]),
    )


def rally_list_item(rally: rx.Var[dict]) -> rx.Component:
    is_dark = State.theme == "dark"
    return rx.el.div(
        rx.el.h4(rally["name"], class_name="font-bold px-2 pt-2"),
        rx.foreach(rally["shots"], shot_item),
        class_name=rx.cond(
            is_dark,
            "bg-gray-800/50 rounded-lg",
            "bg-gray-50 rounded-lg",
        ),
    )


@template(
    route="/[match_id]/shots",
    title="Esplora i Tiri",
    # on_load=ActivationState.on_load,
)
def shot_explorer_page() -> rx.Component:
    is_dark = State.theme == "dark"
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.video(
                    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    id="video-player",
                    class_name="w-full h-full object-cover rounded-xl",
                ),
                rx.el.img(
                    src="/placeholder.svg",
                    class_name="w-full h-64 object-cover rounded-xl bg-gray-200 dark:bg-gray-700 mt-4 border border-gray-200 dark:border-gray-600",
                ),
                class_name="w-full lg:w-2/3 flex flex-col gap-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Shots",
                        class_name="text-lg font-bold",
                    ),
                    rx.el.button(
                        "+ Filter",
                        class_name="bg-green-100 text-green-800 text-sm font-semibold px-3 py-1 rounded-md hover:bg-green-200",
                    ),
                    class_name="flex justify-between items-center mb-2",
                ),
                rx.el.div(
                    rx.foreach(
                        State.all_players,
                        lambda p: rx.el.button(
                            p["name"],
                            class_name=rx.cond(
                                is_dark,
                                "px-3 py-1 rounded-md text-sm bg-gray-700 hover:bg-gray-600",
                                "px-3 py-1 rounded-md text-sm bg-gray-200 hover:bg-gray-300",
                            ),
                        ),
                    ),
                    class_name="flex gap-2 mb-4 flex-wrap",
                ),
                rx.el.div(
                    rx.foreach(State.rallies, rally_list_item),
                    class_name="flex flex-col gap-4 overflow-y-auto h-[600px] pr-2",
                ),
                class_name=card_style(is_dark) + " w-full lg:w-1/3",
            ),
            class_name="flex flex-col lg:flex-row gap-8",
        )
    )
