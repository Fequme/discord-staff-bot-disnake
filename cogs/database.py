import disnake
from disnake.ext import commands, tasks
import sqlite3
import time
from config import *

class Database(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.create_table()
        self.time.start()
        self.otpysk.start()
        self.give.start()

    def create_table(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                warn INTEGER DEFAULT 0,
                points INTEGER DEFAULT 0,
                time INTEGER DEFAULT 0,
                otpysk INTEGER DEFAULT 0,
                role TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS warn (
                user_id INTEGER,
                number INTEGER,
                real TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS nabor (
                user_id INTEGER,
                number INTEGER
            )
            """
        )
        conn.commit()

    @tasks.loop(minutes=1)  
    async def time(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("UPDATE users SET time = time + 1")
        conn.commit()

    @tasks.loop(hours=24)  
    async def otpysk(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET otpysk = CASE WHEN otpysk > 0 THEN otpysk - 1 ELSE otpysk END")
        conn.commit()

    @tasks.loop(hours=24)
    async def give(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM users WHERE otpysk = 0")
        users_with_otpysk_0 = cursor.fetchall()

        for user_id in users_with_otpysk_0:
            cursor.execute("SELECT otpysk FROM users WHERE user_id = ?", (user_id[0],))
            otpysk = cursor.fetchone()[0]
            
            if otpysk == 0:
                cursor.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (AUTO, user_id[0]))

        conn.commit()
        conn.close()

    @tasks.loop(seconds=10)
    async def warns(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, warn FROM users")
        user_warns = cursor.fetchall()

        for user_id, warn in user_warns:
            if warn <= PRED:
                user = self.client.get_user(user_id)
                roles_to_remove = [
                    STAFF_ROLE, EVENTS_MOD, MODER, CLANS_STAFF,
                    CONTROL, MAFIA_MOD, TRIBUN_MOD, CLOSE_MOD,
                    CREATIVE, SUPPORT,
                    OTVE_STAFF, OTVE_EVENTS, OTVE_MODER, OTVE_CLANS,
                    OTVE_CONTROL, OTVE_MAFIA, OTVE_TRIBUN, OTVE_CLOSE,
                    OTVE_CREATIVE, OTVE_SUPPORT,
                    ADMIN, CURATOR, MASTER
                ]
                for role in roles_to_remove:
                    await user.remove_roles(role)

        cursor.execute("DELETE user_id FROM users")
        conn.close()

def setup(client):
    client.add_cog(Database(client))
    print("Стафф: 'датабаза' включён")
