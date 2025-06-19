from app.database.connection import DB


def get_match_stats(code):
    return DB.stats.find_one({"code": code})


def get_match_insights(code):
    return DB.insights.find_one({"code": code})


def upload_match(stats, insights):
    if DB.stats.insert_one(stats):
        return DB.insights.insert_one(insights)
    return False


def update_match_info(code, data, players_n):
    data = {
        "match_name": data.get("name"),
        "players_ids": [
            int(data.get(f"giocatore_{i+1}", -1)) for i in range(players_n)
        ],
    }
    return DB.stats.update_one({"code": code}, {"$set": data})
