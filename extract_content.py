import requests
from bs4 import BeautifulSoup

def extract_article_from_hackernews(url):
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

if __name__ == "__main__":
    hackernews_url = input("HackerNewsの記事URLを入力してください: ")
    title, article_text = extract_article_from_hackernews(hackernews_url)
    if article_text:
        print(f"\nタイトル: {title}\n\n本文:\n{article_text}")
    else:
        print("記事本文が見つかりませんでした。")