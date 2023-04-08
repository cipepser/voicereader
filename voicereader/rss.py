import feedparser
from datetime import datetime, timedelta
import pytz
from typing import List

def fetch_rss_feed(feed_url: str) -> feedparser.FeedParserDict:
    feed = feedparser.parse(feed_url)
    return feed

def extract_urls(feed: feedparser.FeedParserDict, before_hour: int) -> List[str]:
    urls = []
    now = datetime.now(pytz.utc)
    time_limit = now - timedelta(hours=before_hour)

    for entry in feed.entries:
        entry_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
        url = entry.link
        if entry_date > time_limit:
            urls.append(url)

    return urls

def get_article_urls() -> List[str]:
    rss_feed_url = "https://feeds.feedburner.com/TheHackersNews"
    feed = fetch_rss_feed(rss_feed_url)
    
    return extract_urls(feed, 24)
