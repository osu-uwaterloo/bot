import sqlite3

from utils.google import SheetsAPI


class User:
    def __init__(self, db: sqlite3.Connection, user_id: int, bancho_id: int | None = None) -> None:
        """`user_id` refers to a Discord user ID"""
        self.db = db
        self.user_id = user_id
        self.bancho_id = bancho_id or self.__get_bancho_id()

    def __get_bancho_id(self) -> int | None:
        cur = self.db.cursor()
        cur.execute("SELECT bancho_id FROM users WHERE discord_id=(?)", (self.user_id,))
        bancho_id = cur.fetchone()
        if bancho_id:
            return bancho_id[0]

    def insert(self) -> int | None:
        cur = self.db.cursor()
        cur.execute("INSERT INTO users VALUES (?, ?)", (self.user_id, self.bancho_id))
        self.db.commit()

        cur.execute("SELECT * FROM users WHERE discord_id=(?) AND bancho_id=(?)", (self.user_id, self.bancho_id))
        res = cur.fetchone()
        if res:
            return cur.lastrowid

    def get_woc_user(self, sheets_api: SheetsAPI) -> dict[str, str] | None:
        data = sheets_api.get_data()
        keys: list = data["values"][0]
        user_id_column = keys.index("USER ID")
        woc_user = None
        for row in data["values"][2:]:
            if row[user_id_column] == str(self.bancho_id):
                woc_user = {k: v for k, v in zip(keys, row)}
        return woc_user
