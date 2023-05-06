import requests
import json
import logging
from typing import Optional
from voicereader.protocols.destination import Destinator, TranslatedTransaction

class QiitaError(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception
        super().__init__(f"An error occurred in the other library: {original_exception}")

class PocketError(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception
        super().__init__(
            f"An error occurred in the other library: {original_exception}")

class QiitaPocketDestinator(Destinator):
    def __init__(
            self,
            qiita_access_token: str,
            pocket_consumer_key: str,
            pocket_access_token: str
    ):
        self.qiita_access_token = qiita_access_token
        self.pocket_consumer_key = pocket_consumer_key
        self.pocket_access_token = pocket_access_token

    # return url
    def create_private_article(self, transaction: TranslatedTransaction) -> Optional[str]:
        url = "https://qiita.com/api/v2/items"

        tags = [{"name": transaction.get_tag()}]
        private = True
        payload = {
            "title": transaction.get_title(),
            "body": transaction.get_article_text_jp(),
            "tags": tags,
            "private": private,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.qiita_access_token}",
        }

        try:
            response = requests.post(
                url, data=json.dumps(payload), headers=headers)
        except Exception as e:
            raise QiitaError(e)

        if response.status_code == 201:
            article_data = json.loads(response.text)
            url = article_data['url']
            logging.info(f"Success to post an article to Qiita as private. url: {url}")
            return url
        else:
            raise QiitaError(
                f"Failed to post an article with status code: {response.status_code}, response: {response.text}"
            )

    def send_to_reader(self, url: str) -> None:
        payload = {
            "consumer_key": self.pocket_consumer_key,
            "access_token": self.pocket_access_token,
            "url": url,
            "tags": ["voicereader"]
        }

        try:
            response = requests.post("https://getpocket.com/v3/add", data=payload)
        except Exception as e:
            raise PocketError(e)

        if response.status_code == 200:
            logging.info(f"Add a URL to Pocket, url: {url}")
        else:
            raise PocketError(
                f"Failed to add a URL with status code: {response.status_code}, response: {response.text}")

