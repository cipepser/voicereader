import requests
import json
from typing import Optional

class QiitaError(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception
        super().__init__(f"An error occurred in the other library: {original_exception}")

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

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
    except Exception as e:
        raise QiitaError(e)

    if response.status_code == 201:
        article_data = json.loads(response.text)
        url = article_data['url']
        print("Success to post an article to Qiita as private. url: {}".format(url))
        return url
    else:
        raise QiitaError(f"Failed to post an article with status code: {response.status_code}, response: {response.text}")
