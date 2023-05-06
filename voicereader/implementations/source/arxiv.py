import os
import requests
import re
import logging
from bs4 import BeautifulSoup
from typing import List, Optional, Tuple

from voicereader.protocols.source import ContentExtractor, UntranslatedTransaction

BASE_URL_ARXIV = "https://arxiv.org"
FILTER_KEY_WORDS = ["differentially", "privacy", "private", "differential"]
CATEGORIES = ["cs.CR"]

class ArxivExtractor(ContentExtractor):
    def extract(self) -> List[UntranslatedTransaction]:
        txs = []
        for category in CATEGORIES:
            link_to_all = extract_link_to_all_papers(category)

            page = requests.get(f"{BASE_URL_ARXIV}/{link_to_all}")
            soup = BeautifulSoup(page.content, "html.parser")
            n = number_items_in_yeesterday(soup)

            titles_and_links = get_arxiv_recent_titles_and_links(soup, n)
            for (title, url) in titles_and_links:
                if contains_key_words(title):
                    abstract = extract_abstract_from_arxiv(url)
                    article_text = abstract.replace("Abstract:  ", "").replace("\n", " ")

                    tx = UntranslatedTransaction(
                        title=title,
                        article_text_en=article_text,
                        tag="arxiv"
                    )
                    txs.append(tx)

        return txs

def extract_link_to_all_papers(category: str) -> Optional[str]:
    page = requests.get(f"{BASE_URL_ARXIV}/list/{category}/recent")

    soup = BeautifulSoup(page.content, "html.parser")
    links = [a.get("href") for a in soup.find_all("a", href=True)]

    target_link = None
    for link in links:
        if re.search(rf"/list/{category}/pastweek\?show=\d+", link):
            target_link = link
            break

    return target_link

def contains_key_words(title: str) -> bool:
    return any([key_word in title.lower() for key_word in FILTER_KEY_WORDS])

def number_items_in_yeesterday(soup: BeautifulSoup) -> Optional[int]:
    links = [a.get("href") for a in soup.find_all("a", href=True)]

    for link in links:
        res = re.search(r"#item(\d+)", link)
        if res:
            return int(res.group(1))

    return None

def get_arxiv_recent_titles_and_links(soup: BeautifulSoup, n: int) -> List[str]:
    titles_and_links = []
    for i, (link_item, title_item) in enumerate(zip(soup.find_all("dt"), soup.find_all("div", {"class": "meta"}))):
        if i >= n:
            break
        link_section = link_item.find("a", {"title": "Abstract"})
        link = f"{BASE_URL_ARXIV}{link_section['href']}" if link_section else None

        title_section = title_item.find("div", {"class": "list-title"})
        title = title_section.text.strip().removeprefix("Title: ") if title_section else None

        if title and link:
            titles_and_links.append((title, link))

    return titles_and_links

def extract_abstract_from_arxiv(url: str) -> str:
    response = requests.get(url)

    if response.status_code != 200:
        logging.warning(f"Error: Unable to fetch URL ({response.status_code})")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    abstract = soup.find("blockquote", {"class": "abstract"}).text.strip()

    return abstract
