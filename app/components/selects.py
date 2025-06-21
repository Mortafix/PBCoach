import reflex as rx
from app.database.locations import get_all_locations
from app.database.players import get_all_players

# ---- ITEM RENDER


def select_item(item) -> rx.Component:
    return rx.select.item(item[1], value=item[0])


def select_item_full(item) -> rx.Component:
    return rx.select.item(f"{item[0]} • {item[1]}", value=item[0])


def select_item_same(item) -> rx.Component:
    return rx.select.item(item[0], value=item[0])


# ---- SELECTS


def player_select(state, placeholder, trigger_params=None, root_params=None):
    root_params = root_params or dict()
    trigger_params = trigger_params or dict()

    class PlayerState(state):
        @rx.var(cache=False)
        def players(self) -> list[tuple[str, str]]:
            entries = {
                str(player.get("id")): f"{player.get('name')} {player.get('surname')}"
                for player in get_all_players(sort=[("name", 1)])
            }
            return list(entries.items())

    return rx.select.root(
        rx.select.trigger(placeholder=placeholder, **trigger_params),
        rx.select.content(
            rx.select.group(rx.foreach(PlayerState.players, select_item))
        ),
        name=placeholder.lower().replace(" ", "_"),
        **root_params,
    )


def location_select(state, trigger_params=None, root_params=None):
    root_params = root_params or dict()
    trigger_params = trigger_params or dict()

    class LocationState(state):
        @rx.var(cache=False)
        def locations(self) -> list[tuple[str, str]]:
            entries = {
                str(location.get("id")): location.get("name")
                for location in get_all_locations(sort=[("name", 1)])
            }
            return list(entries.items())

    return rx.select.root(
        rx.select.trigger(placeholder="Campo di gioco", **trigger_params),
        rx.select.content(
            rx.select.group(rx.foreach(LocationState.locations, select_item))
        ),
        name="location",
        **root_params,
    )
