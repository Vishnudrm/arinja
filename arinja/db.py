"""Database operations for storing and retrieving news articles."""
from typing import List, Dict, Optional
import datetime
from contextlib import contextmanager
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os
import sys

# Load environment variables from config/config.env
config_env = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config/config.env')
load_dotenv(dotenv_path=config_env)
POSTGRES_URI = os.getenv('POSTGRES_URI')

if not POSTGRES_URI:
    print("Error: POSTGRES_URI environment variable not found in config/config.env")
    sys.exit(1)

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

def store_articles(articles: List[Dict]) -> List[int]:
    """Store articles in the database, handling duplicates."""
    article_ids = []
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            for article in articles:
                # Check for duplicates
                cur.execute("""
                    SELECT id FROM articles 
                    WHERE title = %s AND source = %s
                    AND published_at::date = %s::date
                """, (article['title'], article['source'], article['published_at']))
                
                result = cur.fetchone()
                if result:
                    article_ids.append(result[0])
                    continue
                
                # Insert new article
                cur.execute("""
                    INSERT INTO articles 
                    (title, source, published_at, content, category, url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    article['title'],
                    article['source'],
                    article['published_at'],
                    article['content'],
                    article['category'],
                    article['url']
                ))
                
                article_ids.append(cur.fetchone()[0])
        
        conn.commit()
    
    return article_ids

def get_articles(
    category: Optional[str] = None,
    from_date: Optional[datetime.datetime] = None,
    to_date: Optional[datetime.datetime] = None,
    limit: int = 20
) -> List[Dict]:
    """Retrieve articles from the database with optional filters."""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = """
                SELECT id, title, source, published_at, category, url
                FROM articles
                WHERE 1=1
            """
            params = []
            
            if category:
                query += " AND category = %s"
                params.append(category)
            
            if from_date:
                query += " AND published_at >= %s"
                params.append(from_date)
            
            if to_date:
                query += " AND published_at <= %s"
                params.append(to_date)
            
            query += " ORDER BY published_at DESC LIMIT %s"
            params.append(limit)
            
            cur.execute(query, params)
            return [dict(row) for row in cur.fetchall()]

def get_article_by_id(article_id: int) -> Optional[Dict]:
    """Retrieve a single article by ID."""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("""
                SELECT id, title, source, published_at, content, category, url
                FROM articles WHERE id = %s
            """, (article_id,))
            
            result = cur.fetchone()
            return dict(result) if result else None