import requests
import json
import os

def create_hatena_draft(access_token, title, content):
    url = "https://qiita.com/api/v2/items"

    tags = [{"name": "HackerNews"}]
    private = True
    payload = {
        "title": title,
        "body": content,
        "tags": tags,
        "private": private,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.status_code == 201:
        print("Success to post an article to Qiita as private.")
        article_data = json.loads(response.text)
        print(article_data)
        return article_data['url']
    else:
        print(f"Failed to post an article with status code: {response.status_code}")
        print(response.text)
        return None

TITLE = "日本語のタイトル"
CONTENT = """
日本語のコンテンツ
"""

if __name__ == "__main__":
    access_token = os.getenv("ACCESS_TOKEN_QIITA")
    url = create_hatena_draft(access_token, TITLE, CONTENT)
    print()
    print(url)

