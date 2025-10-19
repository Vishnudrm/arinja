"""Database utilities and connections."""
import os
from contextlib import contextmanager
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.expanduser('~/.config/arinja/.env'))
POSTGRES_URI = os.getenv('POSTGRES_URI')

@contextmanager
def get_db_connection():
    """Get a database connection."""
    conn = None
    try:
        conn = psycopg2.connect(POSTGRES_URI)
        yield conn
    finally:
        if conn is not None:
            conn.close()