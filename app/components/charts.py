import reflex as rx


def chart_title(icon, title):
    return rx.badge(
        rx.icon(icon or "star", size=20),
        rx.text(title, size="4"),
        color_scheme="gray",
        size="3",
    )


# ---- CHARTS


def base_pie_chart(icon="", title="", data=None, fmt=": ", size=250) -> rx.Component:
    return rx.vstack(
        rx.cond(
            title, rx.hstack(chart_title(icon, title), width="100%", justify="center")
        ),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=data,
                data_key="value",
                name_key="name",
                padding_angle=7,
                inner_radius=60,
            ),
            rx.recharts.graphing_tooltip(separator=f" {fmt}"),
            rx.recharts.legend(),
            width=size,
            height=size,
        ),
        width="100%",
        flex="1 1 45%",
        align="center",
    )


def quality_area_chart(icon="", title="", data=None, state=None) -> rx.Component:
    start_val, end_val = data[0].get("value"), data[-1].get("value")
    return rx.vstack(
        rx.cond(
            title, rx.hstack(chart_title(icon, title), width="100%", justify="center")
        ),
        rx.hstack(
            rx.switch(cursor="pointer", on_change=state.set_quality_trend),
            rx.text("Trend"),
            align="center",
            justify="start",
            width="100%",
            margin_left="7em",
        ),
        rx.recharts.area_chart(
            rx.recharts.area(data_key="value", name="Qualità"),
            rx.recharts.x_axis(data_key="name", tick=False),
            rx.recharts.y_axis(domain=[0, 100]),
            rx.recharts.graphing_tooltip(separator=" : "),
            rx.recharts.legend(),
            rx.cond(
                state.show_quality_trend,
                rx.recharts.reference_line(
                    segment=[
                        {"x": 0, "y": start_val},
                        {"x": data.length() - 1, "y": end_val},
                    ],
                    stroke_width=2,
                    stroke=rx.color(
                        rx.cond(end_val.to(int) > start_val.to(int), "green", "red"), 10
                    ),
                    if_overflow="extendDomain",
                ),
            ),
            data=data,
            width="100%",
            height=250,
        ),
        width="100%",
        flex="1 1 45%",
        align="center",
        min_width="15rem",
    )


def accuracy_area_chart(icon="", title="", data=None, state=None) -> rx.Component:
    area_in = rx.recharts.area(
        data_key="in",
        name="Dentro",
        stack_id="1",
        stroke=rx.color("green", 9),
        fill=rx.color("green", 8),
    )
    return rx.vstack(
        rx.cond(
            title, rx.hstack(chart_title(icon, title), width="100%", justify="center")
        ),
        rx.hstack(
            rx.switch(
                cursor="pointer",
                on_change=state.set_accuracy_stack,
                default_checked=True,
            ),
            rx.text("Accumulato"),
            align="center",
            justify="start",
            width="100%",
            margin_left="7em",
        ),
        rx.recharts.area_chart(
            rx.cond(~state.stack_accuracy, area_in),
            rx.recharts.area(
                data_key="out",
                name="Fuori",
                stack_id=rx.cond(state.stack_accuracy, "1", "2"),
                stroke=rx.color("red", 9),
                fill=rx.color("red", 8),
            ),
            rx.recharts.area(
                data_key="net",
                name="Rete",
                stack_id=rx.cond(state.stack_accuracy, "1", "3"),
                stroke=rx.color("plum", 9),
                fill=rx.color("plum", 8),
            ),
            rx.cond(state.stack_accuracy, area_in),
            rx.recharts.x_axis(tick=False),
            rx.recharts.y_axis(domain=[0, 100]),
            rx.recharts.graphing_tooltip(separator=" : "),
            rx.recharts.legend(),
            data=data,
            stack_offset="none",
            width="100%",
            height=250,
        ),
        width="100%",
        flex="1 1 45%",
        align="center",
        min_width="15rem",
    )


def base_bar_chart(icon="", title="", data=None):
    return rx.vstack(
        rx.cond(
            title, rx.hstack(chart_title(icon, title), width="100%", justify="center")
        ),
        rx.recharts.bar_chart(
            rx.recharts.bar(data_key="value", name="Arrivo in Kitchen"),
            rx.recharts.x_axis(data_key="name", tick=False),
            rx.recharts.y_axis(domain=[0, 100]),
            rx.recharts.graphing_tooltip(separator=" : %"),
            data=data,
            stack_offset="none",
            width="100%",
            height=250,
        ),
        width="100%",
        flex="1 1 45%",
        align="center",
        min_width="15rem",
    )
