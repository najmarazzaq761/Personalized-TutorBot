import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from database import db
import asyncio

# Run DB table creation
asyncio.run(db.create_tables())

