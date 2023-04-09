import requests
from bs4 import BeautifulSoup
from typing import Tuple

class ContentExtractorError(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception
        super().__init__(f"An error occurred in the other library: {original_exception}")

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
