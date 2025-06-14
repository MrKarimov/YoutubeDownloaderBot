import aiosqlite

import os

DB_PATH = os.path.join(os.path.dirname(__file__), "botdata.db")

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        await db.commit()

async def ensure_db_exists():
    if not os.path.exists(DB_PATH):
        print("❌ Ma'lumotlar bazasi topilmadi. Yaratilmoqda...")
        await init_db()
    else:
        print("✅ Ma'lumotlar bazasi mavjud.")


        
async def add_user(user_id,  username, full_name):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (user_id, username, full_name)
            VALUES (?, ?, ?)
        """, (user_id, username, full_name))
        await db.commit()


async def user_info():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id, username, full_name FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows

async def user_full_info():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows

async def get_all_user_ids():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]


        

        

