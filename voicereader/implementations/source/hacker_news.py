import requests
import feedparser
import pytz
from bs4 import BeautifulSoup
from typing import Tuple, List
from datetime import datetime, timedelta
from voicereader.protocols.source import ContentExtractor, UntranslatedTransaction

class RssError(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception
        super().__init__(
            f"An error occurred in the other library: {original_exception}")

class ContentExtractorError(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception
        super().__init__(
            f"An error occurred in the other library: {original_exception}")

class HackerNewsExtractor(ContentExtractor):
    def extract(self) -> List[UntranslatedTransaction]:
        txs = []

        for url in get_article_urls():
            title, article = extract_article_from_hackernews(url)
            tx = UntranslatedTransaction(
                title=title,
                article_text_en=article,
                tag="HackerNews"
            )
            txs.append(tx)

        return txs

def extract_urls(feed: feedparser.FeedParserDict, before_hour: int) -> List[str]:
    urls = []
    now = datetime.now(pytz.utc)
    time_limit = now - timedelta(hours=before_hour)

    for entry in feed.entries:
        entry_date = datetime.strptime(
            entry.published, "%a, %d %b %Y %H:%M:%S %z")
        url = entry.link
        if entry_date > time_limit:
            urls.append(url)

    return urls

def get_article_urls() -> List[str]:
    try:
        feed = feedparser.parse("https://feeds.feedburner.com/TheHackersNews")
    except Exception as e:
        raise RssError(e)

    return extract_urls(feed, 24)

def extract_article_from_hackernews(url: str) -> Tuple[str, str]:
    try:
        response = requests.get(url)
    except Exception as e:
        raise ContentExtractorError(e)

    if response.status_code != 200:
        raise ContentExtractorError(f"Error {response.status_code}: Unable to fetch URL({url}) content")

    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("title").text
    article_text = ""

    for tag in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
        article_text += tag.text + "\n\n"

    return title, article_text.strip()
