from fastapi import HTTPException
import requests, os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")


class TextSummarizer:
    def __init__(self):
        pass

    def summarize(self, *, text: str) -> {str: list}:
        API_URL = (
            "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
        )
        try:
            headers = {"Authorization": f"Bearer {API_TOKEN}"}
            response = requests.post(API_URL, headers=headers, json=text)

            if response.status_code == 200:
                data = response.json()
                return {"data": data}
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="HuggingFace API returned an error",
                )

        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500, detail="HuggingFace API request failed"
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")
