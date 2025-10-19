import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.expanduser('~/.config/arinja/.env'))
POSTGRES_URI = os.getenv('POSTGRES_URI')

schema = '''
CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    title TEXT,
    source TEXT,
    published_at TIMESTAMP,
    content TEXT,
    language TEXT,
    category TEXT,
    url TEXT,
    UNIQUE(title, source, published_at)
);
CREATE TABLE IF NOT EXISTS bookmarks (
    id SERIAL PRIMARY KEY,
    article_id INTEGER REFERENCES articles(id),
    tags TEXT[],
    note TEXT,
    starred BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS highlights (
    id SERIAL PRIMARY KEY,
    article_id INTEGER REFERENCES articles(id),
    snippet TEXT,
    color TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- We'll add embeddings table later after pgvector is installed
-- CREATE TABLE IF NOT EXISTS embeddings (
--     id SERIAL PRIMARY KEY,
--     article_id INTEGER REFERENCES articles(id),
--     embedding VECTOR(1536),
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );
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
