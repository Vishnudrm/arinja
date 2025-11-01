import os
import sys
import psycopg2
from dotenv import load_dotenv

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_env = os.path.join(project_root, 'config', 'config.env')

if not os.path.exists(config_env):
    print(f"Error: config.env not found at {config_env}")
    print("Please copy config.example.env to config.env and update the values.")
    sys.exit(1)

load_dotenv(dotenv_path=config_env)
POSTGRES_URI = os.getenv('POSTGRES_URI')

schema = '''
CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    source TEXT,
    published_at TIMESTAMP,
    content TEXT,
    category TEXT,
    url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(title, source, published_at)
);
CREATE INDEX IF NOT EXISTS articles_category_idx ON articles(category);
CREATE INDEX IF NOT EXISTS articles_published_at_idx ON articles(published_at);
'''

def main():
    if not POSTGRES_URI:
        print("POSTGRES_URI not set in .env")
        return
    conn = psycopg2.connect(POSTGRES_URI)
    cur = conn.cursor()
    cur.execute(schema)
    conn.commit()
    cur.close()
    conn.close()
    print("Database initialized.")

if __name__ == "__main__":
    main()
