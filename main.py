# uvicorn main:app --reload

from fastapi import FastAPI, HTTPException, Request
from datetime import date
from pydantic import BaseModel
from summarizer import TextSummarizer
from scrapers import TheGuardian, CNN, BBC
import article_data
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

allowed_origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    raise HTTPException(status_code=400, detail="Not found")


@app.get("/articles/{website_name}")
async def get_articles(website_name: str):
    if website_name == "the_guardian":
        links = TheGuardian(date.today()).get_articles()
        return article_data.get_details_for_all_articles(links)

    if website_name == "cnn":
        links = CNN().get_articles()
        return article_data.get_details_for_all_articles(links)

    if website_name == "bbc":
        links = BBC().get_articles()
        return article_data.get_details_for_all_articles(links)

    raise HTTPException(status_code=400, detail="Invalid website name")


class RequestData(BaseModel):
    text: str


@app.post("/summarize")
async def summarize_text(data: RequestData):
    if len(data.text) < 20:
        raise HTTPException(
            status_code=400,
            detail="Provide text at least 20 characters long",
        )
    text_summarizer = TextSummarizer()
    summary = text_summarizer.summarize(text=data.text)
    # print(summary)
    return summary
