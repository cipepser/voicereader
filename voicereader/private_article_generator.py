import requests
import json
from typing import Optional

def create_private_article_in_qiita(access_token: str, title: str, content: str) -> Optional[str]:
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
        article_data = json.loads(response.text)
        url = article_data['url']
        print("Success to post an article to Qiita as private. url: {}".format(url))
        return url
    else:
        print(f"Failed to post an article with status code: {response.status_code}")
        print(response.text)
        return None
