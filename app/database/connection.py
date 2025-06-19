from os import getenv

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
mongo_user = getenv("mongo-user")
mongo_pwd = getenv("mongo-password")
mongo_ip = getenv("mongo-ip")
mongo_production = getenv("mongo-production") == "true"

# ---- database


def init_connection():
    max_idle_time = 3  # minutes
    max_server_select_time = 2  # seconds
    auth = f"{mongo_user}:{mongo_pwd}@" if mongo_user else ""
    connection = (
        f"mongodb://{auth}{mongo_ip}:27017/"
        "?directConnection=true&retryWrites=true&w=majority"
        f"&serverSelectionTimeoutMS={max_server_select_time * 1000}"
        f"&maxIdleTimeMS={max_idle_time * 60000}"
    )
    return MongoClient(connection)


DB_INSTANCE = init_connection()
DB = DB_INSTANCE.pb_coach if mongo_production else DB_INSTANCE.pb_coach_dev
