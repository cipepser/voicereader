import requests
from bs4 import BeautifulSoup
import os
from typing import Tuple

from voicereader.translator import translate_text_to_japanese, OpenAIError
from voicereader.private_article_generator import create_private_article_in_qiita
from voicereader.pocket import add_to_pocket
from voicereader.rss import get_article_urls

def extract_abstract_from_arxiv(url) -> Tuple[str, str]:
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Unable to fetch URL ({response.status_code})")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("title").text
    abstract = soup.find("blockquote", {"class": "abstract"}).text.strip()
    
    return title, abstract

if __name__ == "__main__":
    url = "https://arxiv.org/abs/xxxxx"
    title, abstract = extract_abstract_from_arxiv(url)

    article_text = abstract.replace("Abstract:  ", "").replace("\n", " ")

    japanese_text = translate_text_to_japanese(article_text, os.getenv("API_KEY_OPENAI"))
    qiita_url = create_private_article_in_qiita(os.getenv("ACCESS_TOKEN_QIITA"), title, japanese_text)
    add_to_pocket(os.getenv("CONSUMER_KEY_POCKET"), os.getenv("ACCESS_TOKEN_POCKET"), qiita_url)