import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db import create_tables
import asyncio

# Run DB table creation
asyncio.run(create_tables())
