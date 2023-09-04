import requests, os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")


def cleanOutputText(text):
    text = text.replace(" .", ".")
    return text


class TextSummarizer:
    def __init__(self):
        pass

    def summarize(self, *, text: str):
        API_URL = (
            "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
        )
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        response = requests.post(API_URL, headers=headers, json=text)
        if not response.ok:
            return ""
        text_summary = response.json()
        return text_summary
