import reflex as rx


def base_pie_chart(icon="", title="", data=None, fmt=": ", size=250) -> rx.Component:
    return rx.vstack(
        rx.cond(
            title,
            rx.hstack(
                rx.badge(
                    rx.icon(icon or "star", size=20),
                    rx.text(title, size="4"),
                    color_scheme="gray",
                    size="3",
                ),
                width="100%",
                justify="center",
            ),
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
