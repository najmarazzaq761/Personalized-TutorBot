
import asyncpg # type: ignore
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

async def create_tables():
    print("🔄 Connecting to DB...")
    conn = await asyncpg.connect(DB_URL)

    print("🧱 Creating tables...")
    await conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    );
    """)

    await conn.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        topic TEXT,
        level TEXT,
        roadmap TEXT,
        tutorial TEXT,
        exercise TEXT,
        review TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    await conn.close()
    print("✅ Tables created successfully.")

if __name__ == "__main__":
    asyncio.run(create_tables())
