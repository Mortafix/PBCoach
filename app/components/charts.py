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


def base_area_chart(
    icon="", title="", data=None, fmt=": ", size=250, trend=False
) -> rx.Component:
    start_val, end_val = data[0].get("value"), data[-1].get("value")
    return rx.vstack(
        rx.cond(
            title, rx.hstack(chart_title(icon, title), width="100%", justify="center")
        ),
        rx.recharts.area_chart(
            rx.recharts.area(data_key="value", name="Qualità"),
            rx.recharts.x_axis(data_key="name", tick=False),
            rx.recharts.y_axis(domain=[0, 100]),
            rx.recharts.graphing_tooltip(separator=f" {fmt}"),
            rx.recharts.legend(),
            rx.recharts.reference_line(
                segment=[
                    {"x": 0, "y": start_val},
                    {"x": data.length() - 1, "y": end_val},
                ],
                stroke_width=2,
                stroke=rx.color(
                    rx.cond(end_val.to(int) > start_val.to(int), "green", "red"), 10
                ),
                label="Trend",
            ),
            data=data,
            width="100%",
            height=size,
        ),
        width="100%",
        flex="1 1 45%",
        align="center",
        min_width="30rem",
    )


def accuracy_area_chart(
    icon="", title="", data=None, names=None, fmt=": ", size=250
) -> rx.Component:
    return rx.vstack(
        rx.cond(
            title, rx.hstack(chart_title(icon, title), width="100%", justify="center")
        ),
        rx.recharts.area_chart(
            rx.recharts.area(
                data_key="out",
                name="Fuori",
                stack_id="1",
                stroke=rx.color("red", 9),
                fill=rx.color("red", 8),
            ),
            rx.recharts.area(
                data_key="net",
                name="Rete",
                stack_id="1",
                stroke=rx.color("plum", 9),
                fill=rx.color("plum", 8),
            ),
            rx.recharts.area(
                data_key="in",
                name="Dentro",
                stack_id="1",
                stroke=rx.color("green", 9),
                fill=rx.color("green", 8),
            ),
            rx.recharts.x_axis(tick=False),
            rx.recharts.y_axis(domain=[0, 100]),
            rx.recharts.graphing_tooltip(separator=f" {fmt}"),
            rx.recharts.legend(),
            data=data,
            stack_offset="none",
            width="100%",
            height=size,
        ),
        width="100%",
        flex="1 1 45%",
        align="center",
        min_width="30rem",
    )
