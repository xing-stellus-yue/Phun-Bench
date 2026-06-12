import asyncio
import aiosqlite
import hashlib
import json
from pathlib import Path

DB_FILE = Path(__file__).resolve().parents[2] / "generation_cache.sqlite3"
# _LOCK = asyncio.Lock()  # Ensures thread-safety in multi-threaded apps

async def _get_connection():
    conn = await aiosqlite.connect(DB_FILE, timeout=30)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    return conn

def get_cache_key(model_name, task_name, user_prompt):
    key = f"{model_name}:{task_name}:{user_prompt}"
    return hashlib.md5(key.encode('utf-8')).hexdigest()

async def load_cache_entry(cache_key):
    # async with _LOCK:
    conn = await _get_connection()
    try:
        async with conn.cursor() as cur:
            await cur.execute("SELECT value FROM cache WHERE key = ?", (cache_key,))
            row = await cur.fetchone()
        if row:
            return json.loads(row[0])
        return None
    finally:
        await conn.close()

async def save_cache_entry(cache_key, value):
    # async with _LOCK:
    conn = await _get_connection()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT OR REPLACE INTO cache (key, value) VALUES (?, ?)",
                (cache_key, json.dumps(value, ensure_ascii=False))
            )
            await conn.commit()
    finally:
        await conn.close()
