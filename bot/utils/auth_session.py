import sqlite3

from datetime import datetime, timedelta
import string
import random

class AuthSession:
    def __init__(self, db: sqlite3.Connection, target_email: str, code_len: int, code_duration: timedelta) -> None:
        self.db = db
        self.target_email = target_email
        self.code = ""
        self.code_len = code_len
        self.code_duration = code_duration
        self.chars = list(string.ascii_lowercase) + list(range(1, 10))


    def delete(self, id: int):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM auth_sessions WHERE id=(?);", (id,))
        self.db.commit()

    def generate_code(self):
        return "".join([str(random.choice(self.chars)) for i in range(self.code_len)])


    def prepare(self):
        cursor = self.db.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS auth_sessions (id INTEGER PRIMARY KEY, email TEXT, code TEXT, expires TEXT);"
        )
        self.db.commit()

        res = cursor.execute("SELECT id, code, expires FROM auth_sessions;")
        active_sessions = res.fetchall()

        used_codes = []
        for sess in active_sessions:
            expire_dt = datetime.fromisoformat(sess[2])
            if datetime.now() > expire_dt:
                self.delete(sess[0])
            else:
                used_codes.append(sess[1])

        self.code = self.generate_code()
        while self.code in used_codes:
            self.code = self.generate_code()


    def save(self):
        expires = datetime.now() + self.code_duration
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO auth_sessions (email, code, expires) VALUES (?, ?, ?);",
            (self.target_email, self.code, expires.isoformat())
        )
        self.db.commit()

    
    def validate(self, code: str):
        if code is None or len(code) == 0:
            return {"success": False, "reason": "No code provided"}
        
        cursor = self.db.cursor()
        res = cursor.execute("SELECT id, expires FROM auth_sessions WHERE code=(?);", (code,))
        sess = res.fetchone()

        if sess is None:
            return {"success": False, "reason": "Incorrect code"}
        
        expires = datetime.fromisoformat(sess[1])
        if datetime.now() > expires:
            self.delete(sess[0])
            return {"success": False, "reason": "Session expired"}
        
        self.delete(sess[0])
        return {"success": True}

        

        

    