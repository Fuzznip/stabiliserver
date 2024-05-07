import psycopg
from psycopg_pool import ConnectionPool

from dotenv import load_dotenv
load_dotenv()
import os

import wom

dbpool = ConnectionPool(conninfo = os.getenv("DATABASE_URL"))


