import requests
import os

def add_to_pocket(consumer_key, access_token, url):
    payload = {
        "consumer_key": consumer_key,
        "access_token": access_token,
        "url": url
    }

    response = requests.post("https://getpocket.com/v3/add", data=payload)

    if response.status_code == 200:
        print("Add a URL to Pocket.")
    else:
        print("Failed to add a URL with status code:", response.status_code)
        print("response:", response.text)

if __name__ == "__main__":
    consumer_key = os.getenv("CONSUMER_KEY")
    access_token = os.getenv("ACCESS_TOKEN_POCKET")
    url = "https://example.com"

    add_to_pocket(consumer_key, access_token, url)
