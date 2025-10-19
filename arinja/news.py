"""News fetching and processing utilities."""
import datetime
import pytz

# IST timezone
IST = pytz.timezone('Asia/Kolkata')

def get_current_ist_time():
    """Get current time in IST."""
    return datetime.datetime.now(IST)