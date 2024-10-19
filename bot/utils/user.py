import sqlite3
import lightbulb

from utils.google import SheetsAPI

class User:
    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db

    def get_bancho_user_id(self, ctx: lightbulb.Context) -> int:
        cur = self.db.cursor()
        res = cur.execute("SELECT bancho_id FROM users WHERE discord_id=(?)", (ctx.author.id,))
        return res.fetchone()[0]

    def get_woc_user(self, user_id: int, sheets_api: SheetsAPI) -> dict[str, str] | None:
        data = sheets_api.get_data()
        keys: list = data["values"][0]
        user_id_column = keys.index("USER ID")
        woc_user = None
        for row in data["values"][2:]:
            if row[user_id_column] == str(user_id):
                woc_user = {k: v for k, v in zip(keys, row)}

        return woc_user
