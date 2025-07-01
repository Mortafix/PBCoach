import reflex as rx
from app.templates.base import State

chip_props = {
    "radius": "full",
    "variant": "soft",
    "size": "3",
    "cursor": "pointer",
    "style": {"_hover": {"opacity": 0.75}},
}


class ChipsState(State):
    @rx.event
    def toggle_item(self, item, key):
        if key not in self.selected_items:
            self.selected_items[key] = [item]
            return
        if item in self.selected_items[key]:
            self.selected_items[key].remove(item)
            return
        self.selected_items[key].append(item)


def unselected_item(state, item: str, key: str) -> rx.Component:
    return rx.badge(
        item[1],
        color_scheme="gray",
        **chip_props,
        on_click=[ChipsState.toggle_item(item[0], key), state.chips_update],
    )


def selected_item(state, item: str, key: str) -> rx.Component:
    return rx.badge(
        rx.icon("check", size=18),
        item[1],
        color_scheme="amber",
        **chip_props,
        on_click=[ChipsState.toggle_item(item[0], key), state.chips_update],
    )


def item_chip(state, item: str, key="str") -> rx.Component:
    return rx.cond(
        ChipsState.selected_items.get(key, []).contains(item[0]),
        selected_item(state, item, key),
        unselected_item(state, item, key),
    )


def chips(state, available_items, key="") -> rx.Component:
    return rx.hstack(
        rx.foreach(available_items, lambda el: item_chip(state, el, key)),
        wrap="wrap",
        spacing="2",
    )
