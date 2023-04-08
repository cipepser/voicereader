import os
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root_path))

from voicereader.source_content_extractor import extract_article_from_hackernews
from voicereader.translator import translate_text_to_japanese
from voicereader.private_article_generator import create_private_article_in_qiita
from voicereader.pocket import add_to_pocket
from voicereader.rss import get_article_urls

if __name__ == "__main__":
    urls = get_article_urls()
    print("{} articles has found".format(len(urls)))
    for source_content_url in urls:
        title, article_text = extract_article_from_hackernews(source_content_url)
        if article_text:
            print("got the article which title is ': {}'".format(title))
        else:
            print("no text in the article which title is ': {}'".format(title))

        japanese_text = translate_text_to_japanese(article_text, os.getenv("API_KEY_OPENAI"))
        qiita_url = create_private_article_in_qiita(os.getenv("ACCESS_TOKEN_QIITA"), title, japanese_text)
        add_to_pocket(os.getenv("CONSUMER_KEY_POCKET"), os.getenv("ACCESS_TOKEN_POCKET"), qiita_url)
