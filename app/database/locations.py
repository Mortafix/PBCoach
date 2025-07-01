import reflex as rx
from app.database.connection import DB


class Location(rx.Base):
    id: str
    name: str


def parse_model(data):
    return Location(id=data.get("id"), name=data.get("name"))


def get_all_locations(
    filters=None, sort=None, limit=10**10, names=False, parse=False
):
    locations = DB.locations.find(filters, sort=sort or [("id", 1)], limit=limit)
    if names:
        return [location.get("name") for location in locations]
    if parse:
        return [parse_model(location) for location in locations]
    return list(locations)


def get_last_id():
    entry = list(get_all_locations(sort=[("id", -1)], limit=1))
    return entry[0].get("id") if entry else 0


def add_location_to_db(name):
    data = {"id": get_last_id() + 1, "name": name}
    return DB.locations.insert_one(data)


def get_location_name(location_id, dfu="..."):
    location = DB.locations.find_one({"id": location_id})
    return location.get("name") if location else dfu
