from goose3 import Goose
import re
from fastapi import HTTPException

g = Goose({"enable_image_fetching": True})


def clean_input_text(text: str) -> str:
    return re.sub(r"\n", "", text)


def get_article_data(url: str) -> object:
    data = g.extract(url=url)
    if not data:
        raise HTTPException(
            status_code=400,
            detail="Cound not retrieve details for articles, try again later",
        )

    title = data.title
    text = data.cleaned_text
    authors = data.authors
    image = data.top_image.src

    data = {
        "title": title,
        "text": clean_input_text(text),
        "authors": authors,
        "image": image,
    }
    return data


def get_details_for_all_articles(urls: list[str]):
    data = []
    for url in urls:
        article_data = get_article_data(url)
        if not article_data:
            raise HTTPException(
                status_code=400,
                detail="Cound not retrieve article details, try again later",
            )
        article_data["link"] = url
        data.append(article_data)
    return data
