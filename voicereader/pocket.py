import requests

class PocketError(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception
        super().__init__(f"An error occurred in the other library: {original_exception}")

def add_to_pocket(consumer_key: str, access_token: str, url: str):
    payload = {
        "consumer_key": consumer_key,
        "access_token": access_token,
        "url": url,
        "tags": ["voicereader"]
    }

    try: 
        response = requests.post("https://getpocket.com/v3/add", data=payload)
    except Exception as e:
        raise PocketError(e)

    if response.status_code == 200:
        print("Add a URL to Pocket.")
    else:
        raise PocketError(f"Failed to add a URL with status code: {response.status_code}, response: {response.text}")
