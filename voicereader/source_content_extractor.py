import requests
from bs4 import BeautifulSoup
from typing import Tuple

def extract_article_from_hackernews(url: str) -> Tuple[str, str]:
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error {response.status_code}: Unable to fetch URL content")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("title").text
    article_text = ""

    for tag in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
        article_text += tag.text + "\n\n"

    return title, article_text.strip()
