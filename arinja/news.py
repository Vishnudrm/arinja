"""News fetching and processing utilities."""
import datetime
import re
from typing import List, Dict, Optional
import pytz
import requests
from bs4 import BeautifulSoup
from gnews import GNews
from rich.progress import Progress, SpinnerColumn, TextColumn
from urllib.parse import urlparse, parse_qs

def clean_google_url(url: str) -> str:
    """Clean Google News redirect URLs to get the actual article URL."""
    if 'news.google.com' in url:
        try:
            parsed = urlparse(url)
            if parsed.path == '/rss/articles/':
                # Extract actual URL from Google News redirect
                return parse_qs(parsed.query).get('url', [url])[0]
            return url
        except:
            return url
    return url

# IST timezone
IST = pytz.timezone('Asia/Kolkata')

def get_current_ist_time() -> datetime.datetime:
    """Get current time in IST."""
    return datetime.datetime.now(IST)

class NewsSource:
    """News source class for fetching and processing articles."""
    
    def __init__(self, start_date: Optional[datetime.date] = None, end_date: Optional[datetime.date] = None):
        """Initialize news sources with date range."""
        # Default to last 7 days if no dates provided
        if not start_date and not end_date:
            end_date = datetime.datetime.now(IST).date()
            start_date = end_date - datetime.timedelta(days=7)
            
        # Ensure both dates are set if one is provided
        elif start_date and not end_date:
            end_date = datetime.datetime.now(IST).date()
        elif end_date and not start_date:
            start_date = end_date - datetime.timedelta(days=7)
            
        self.start_date = start_date
        self.end_date = end_date
            
        self.gnews = GNews(
            language='en',
            country='IN',
            start_date=start_date,
            end_date=end_date,
            max_results=100
        )
    def detect_category(self, title: str, description: str) -> str:
        """Detect article category from title and description."""
        text = f"{title} {description}".lower()
        
        # Enhanced keyword-based categorization
        categories = {
            'technology': [
                'tech', 'ai', 'robot', 'smartphone', 'computer', 'software', 'app', 'digital',
                'gadget', 'mobile', 'cyber', 'code', 'programming', 'developer', '5g', 'blockchain',
                'cryptocurrency', 'bitcoin', 'internet', 'website', 'online', 'startup'
            ],
            'business': [
                'market', 'stock', 'economy', 'trade', 'business', 'company', 'finance',
                'investment', 'revenue', 'profit', 'earnings', 'shares', 'investor', 'banking',
                'corporate', 'industry', 'sector', 'startup', 'valuation', 'funding'
            ],
            'sports': [
                'cricket', 'football', 'sport', 'match', 'game', 'player', 'tournament',
                'team', 'score', 'win', 'lose', 'championship', 'series', 'athletics',
                'olympic', 'cup', 'league', 'stadium', 'coach', 'athlete'
            ],
            'entertainment': [
                'movie', 'film', 'actor', 'celebrity', 'music', 'song', 'tv', 'show',
                'star', 'cinema', 'drama', 'series', 'concert', 'award', 'director',
                'box office', 'netflix', 'streaming', 'hollywood', 'bollywood'
            ],
            'science': [
                'science', 'research', 'study', 'discovery', 'space', 'physics',
                'biology', 'chemistry', 'scientist', 'experiment', 'laboratory',
                'innovation', 'breakthrough', 'quantum', 'nasa', 'isro', 'astronomy'
            ],
            'health': [
                'health', 'medical', 'disease', 'treatment', 'hospital', 'doctor',
                'patient', 'medicine', 'vaccine', 'virus', 'infection', 'cure',
                'surgery', 'therapy', 'clinic', 'research', 'drug', 'pharmaceutical'
            ],
            'world': [
                'world', 'global', 'international', 'foreign', 'embassy', 'diplomat',
                'president', 'minister', 'united nations', 'treaty', 'summit',
                'bilateral', 'overseas', 'abroad', 'foreign policy', 'war', 'peace'
            ],
            'india': [
                'india', 'indian', 'delhi', 'mumbai', 'bangalore', 'chennai',
                'kolkata', 'hyderabad', 'modi', 'bjp', 'congress', 'parliament',
                'lok sabha', 'supreme court', 'rbi', 'rupee', 'state'
            ]
        }
        
        for cat, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return cat
        
        return 'general'

    def fetch_headlines(self, category: Optional[str] = None) -> List[Dict]:
        """Fetch headlines from various sources."""
        articles = []
        
        try:
            # Configure GNews query based on category
            query = ""
            if category == 'india':
                self.gnews.country = 'IN'
                self.gnews.language = 'en'
                query = "india"
            elif category:
                # Add date range to query for better filtering
                date_range = ""
                if self.start_date and self.end_date:
                    start_str = self.start_date.strftime("%Y-%m-%d")
                    end_str = self.end_date.strftime("%Y-%m-%d")
                    date_range = f" after:{start_str} before:{end_str}"
                query = f"{category} news{date_range}"
            
            # Use get_news which properly supports date ranges
            news = self.gnews.get_news(query)
            
            # Process each article
            for article in news:
                # Basic metadata
                title = article.get('title', '')
                description = article.get('description', '')
                url = clean_google_url(article.get('url', ''))
                detected_category = self.detect_category(title, description)
                
                # Clean title (remove source suffix if present)
                title = re.sub(r'\s*-\s*[^-]+$', '', title)
                
                # Parse published date
                pub_date = article.get('published date')
                if isinstance(pub_date, str):
                    try:
                        # GNews returns dates in format like "1 hour ago", "2 days ago"
                        pub_date = datetime.datetime.now(IST)
                    except:
                        pub_date = datetime.datetime.now(IST)
                
                data = {
                    'title': title,
                    'source': article.get('publisher', {}).get('title'),
                    'url': url,
                    'published_at': pub_date,
                    'category': category or detected_category
                }
                
                try:
                    # Set up headers to mimic a browser
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    
                    # Fetch article content
                    response = requests.get(data['url'], headers=headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Remove unwanted elements
                    for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                        tag.decompose()
                    
                    # Try to find article content
                    article_tags = soup.find_all(['article', 'main']) or soup.find_all(class_=re.compile(r'article|content|story'))
                    
                    if article_tags:
                        # Use the first article/main content area
                        content_area = article_tags[0]
                    else:
                        # Fallback to body
                        content_area = soup.body
                    
                    # Extract paragraphs
                    paragraphs = content_area.find_all('p')
                    content = '\n\n'.join(
                        p.get_text().strip()
                        for p in paragraphs
                        if len(p.get_text().strip()) > 100  # Only substantial paragraphs
                    )
                    
                    # Add content if we found something meaningful
                    if content:
                        data['content'] = content
                    else:
                        data['content'] = "Article content could not be retrieved. Please check the source URL."
                    
                except Exception as e:
                    data['content'] = f"Error fetching article: {str(e)}"
                
                articles.append(data)
        
        except Exception as e:
            print(f"Error fetching headlines for category '{category}': {str(e)}")
        
        return articles
