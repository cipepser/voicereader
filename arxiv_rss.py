import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Tuple, List, Optional
import re

BASE_URL_ARXIV = "https://arxiv.org"

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

def extract_link_to_all_papers(url: str) -> Optional[str]:
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    links = [a.get("href") for a in soup.find_all("a", href=True)]

    target_link = None
    for link in links:
        if re.search(r"/list/cs.CR/pastweek\?show=\d+", link):
            target_link = link
            break

    return target_link

def number_items_in_yeesterday(soup: BeautifulSoup) -> int:
    links = [a.get("href") for a in soup.find_all("a", href=True)]

    for link in links:
        res = re.search(r"#item(\d+)", link)
        if res:
            return int(res.group(1))

    return -1

url = f"{BASE_URL_ARXIV}/list/cs.CR/recent"
link = extract_link_to_all_papers(url)

page = requests.get(f"{BASE_URL_ARXIV}/{link}")
soup = BeautifulSoup(page.content, "html.parser")
n = number_items_in_yeesterday(soup)

titles_and_links = get_arxiv_recent_titles_and_links(soup, n)
for (title, link) in titles_and_links:
    print(title, ":", link)
