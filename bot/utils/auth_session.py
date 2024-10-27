import sqlite3

from datetime import datetime, timedelta
import string
import random

from utils import config
from utils.exceptions import MaxSessionsExceededError


class AuthSession:
    def __init__(self, db: sqlite3.Connection, discord_uid: int, target_email: str, code_len: int, code_duration: timedelta) -> None:
        self.db = db
        self.target_email = target_email
        self.code = ""
        self.code_len = code_len
        self.code_duration = code_duration
        self.chars = list(string.ascii_lowercase) + list(range(1, 10))
        self.discord_uid = discord_uid

    @classmethod
    def delete(cls, id: int, db: sqlite3.Connection):
        cursor = db.cursor()
        cursor.execute("DELETE FROM auth_sessions WHERE id=(?);", (id,))
        db.commit()

    def generate_code(self):
        return "".join([str(random.choice(self.chars)) for i in range(self.code_len)])


    def prepare(self):
        cursor = self.db.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS auth_sessions (id INTEGER PRIMARY KEY, discord_uid INTEGER, email TEXT, code TEXT, expires TEXT);"
        )
        self.db.commit()

        res = cursor.execute("SELECT id, discord_uid, code, expires FROM auth_sessions;")
        active_sessions = res.fetchall()

        used_codes = []
        user_sessions = 0
        for sess in active_sessions:
            expire_dt = datetime.fromisoformat(sess[3])
            if datetime.now() > expire_dt:
                self.delete(sess[0], self.db)
            else:
                used_codes.append(sess[2])
                if sess[1] == self.discord_uid:
                    user_sessions += 1

        if user_sessions > config.MAX_AUTH_SESSIONS:
            raise MaxSessionsExceededError()

        self.code = self.generate_code()
        while self.code in used_codes:
            self.code = self.generate_code()

        return self.code


    def save(self):
        expires = datetime.now() + self.code_duration
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO auth_sessions (email, discord_uid, code, expires) VALUES (?, ?, ?, ?);",
            (self.target_email, self.discord_uid, self.code, expires.isoformat())
        )
        self.db.commit()

    @classmethod
    def validate(cls, code: str, db: sqlite3.Connection):
        if code is None or len(code) == 0:
            return {"success": False, "reason": "No code provided"}
        
        cursor = db.cursor()
        res = cursor.execute("SELECT id, expires FROM auth_sessions WHERE code=(?);", (code,))
        sess = res.fetchone()

        if sess is None:
            return {"success": False, "reason": "Incorrect code"}
        
        expires = datetime.fromisoformat(sess[1])
        if datetime.now() > expires:
            cls.delete(sess[0], db)
            return {"success": False, "reason": "Session expired"}
        
        cls.delete(sess[0], db)
        return {"success": True}

        

        

    