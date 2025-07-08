# pages/init_db.py

import asyncio
from database.db import create_tables

asyncio.run(create_tables())
