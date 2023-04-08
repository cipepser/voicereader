import requests

def add_to_pocket(consumer_key: str, access_token: str, url: str):
    payload = {
        "consumer_key": consumer_key,
        "access_token": access_token,
        "url": url,
        "tags": ["voicereader"]
    }

    response = requests.post("https://getpocket.com/v3/add", data=payload)

    if response.status_code == 200:
        print("Add a URL to Pocket.")
    else:
        print("Failed to add a URL with status code:", response.status_code)
        print("response:", response.text)
