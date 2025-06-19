import reflex as rx

sidebar_width = "16em"
sidebar_close_width = "3em"
max_width = "calc(100% - 16em)"
max_width_close = "calc(100% - 3em)"

base_style = {
    "font_family": "Inter",
    "font_size": "1.5rem",
}

base_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
    # "styles.css",
]

template_page_style = {
    "padding_top": ["1em", "1em", "1em"],
    "padding_x": ["auto", "auto", "2em"],
}

template_content_style = {
    "padding": "1em",
    "margin_bottom": "2em",
    "min_height": "90vh",
}
# ---------- COLORS -----------


def card_style(is_dark: rx.Var[bool]) -> rx.Var[str]:
    return rx.cond(
        is_dark,
        "bg-gray-800 rounded-xl shadow-lg p-6 w-full text-gray-200",
        "bg-white rounded-xl shadow-lg p-6 w-full text-gray-800",
    )
