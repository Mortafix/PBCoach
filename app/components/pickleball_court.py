import reflex as rx
from app.states.state import State


def pickleball_court_svg(data_key: str) -> rx.Component:
    is_dark = State.theme == "dark"
    zones = State.court_arrival_zones[data_key]
    return rx.el.svg(
        rx.el.defs(
            rx.el.linear_gradient(
                rx.el.stop(offset="0%", stop_color="#3b82f6"),
                rx.el.stop(offset="100%", stop_color="#2563eb"),
                id="teamA",
            ),
            rx.el.linear_gradient(
                rx.el.stop(offset="0%", stop_color="#f97316"),
                rx.el.stop(offset="100%", stop_color="#ea580c"),
                id="teamB",
            ),
        ),
        rx.el.rect(
            x="0",
            y="0",
            width="200",
            height="440",
            fill=rx.cond(is_dark, "#2a3b50", "#EBF4FF"),
        ),
        rx.el.rect(
            x="0",
            y="0",
            width="200",
            height="220",
            fill="url(#teamA)",
            opacity="0.6",
        ),
        rx.el.rect(
            x="0",
            y="220",
            width="200",
            height="220",
            fill="url(#teamB)",
            opacity="0.6",
        ),
        rx.el.rect(
            x="0",
            y="0",
            width="200",
            height="440",
            fill="none",
            stroke=rx.cond(is_dark, "white", "#4A5568"),
            stroke_width="2",
        ),
        rx.el.line(
            x1="100",
            y1="0",
            x2="100",
            y2="440",
            stroke=rx.cond(is_dark, "white", "#4A5568"),
            stroke_width="1",
        ),
        rx.el.line(
            x1="0",
            y1="220",
            x2="200",
            y2="220",
            stroke=rx.cond(is_dark, "white", "#4A5568"),
            stroke_width="2",
        ),
        rx.el.line(
            x1="0",
            y1="150",
            x2="200",
            y2="150",
            stroke=rx.cond(is_dark, "white", "#4A5568"),
            stroke_width="1",
        ),
        rx.el.line(
            x1="0",
            y1="290",
            x2="200",
            y2="290",
            stroke=rx.cond(is_dark, "white", "#4A5568"),
            stroke_width="1",
        ),
        rx.el.text(
            zones["team_a_left"].to_string() + "%",
            x="50",
            y="100",
            fill="white",
            font_size="24",
            font_weight="bold",
            text_anchor="middle",
        ),
        rx.el.text(
            zones["team_a_right"].to_string() + "%",
            x="150",
            y="100",
            fill="white",
            font_size="24",
            font_weight="bold",
            text_anchor="middle",
        ),
        rx.el.text(
            zones["team_b_left"].to_string() + "%",
            x="50",
            y="340",
            fill="white",
            font_size="24",
            font_weight="bold",
            text_anchor="middle",
        ),
        rx.el.text(
            zones["team_b_right"].to_string() + "%",
            x="150",
            y="340",
            fill="white",
            font_size="24",
            font_weight="bold",
            text_anchor="middle",
        ),
        view_box="0 0 200 440",
        class_name="rounded-lg w-full max-w-[200px] mx-auto",
    )
