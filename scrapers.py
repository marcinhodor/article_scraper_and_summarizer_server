from bs4 import BeautifulSoup
import requests
from fastapi import HTTPException


class TheGuardian:
    def __init__(self, today):
        self.today = today

    def get_articles(self) -> list[str]:
        try:
            article_links = []
            year = self.today.strftime("%Y")
            month = self.today.strftime("%b").lower()
            day = self.today.strftime("%d")
            url = f"https://www.theguardian.com/world/{year}/{month}/{day}/all"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            articles = soup.find_all("div", class_="fc-item__container")
            for article in articles:
                link = article.find("a", class_="fc-item__link").get("href")
                if link.find("live") == -1 and link.find("video") == -1:
                    article_links.append(link)
            if article_links == []:
                raise HTTPException(
                    status_code=400,
                    detail="Could not fetch The Guardian news, try again later",
                )
            return article_links
        except:
            raise HTTPException(
                status_code=400,
                detail="Could not fetch The Guardian news, try again later",
            )


class BBC:
    def __init__(self):
        pass

    def get_articles(self) -> list[str]:
        try:
            url = "https://www.bbc.com/news"
            article_links = []
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            news_container = soup.find("div", id="news-top-stories-container")
            articles = news_container.find_all("a", class_="gs-c-promo-heading")
            for article in articles:
                link = article.get("href")
                article_links.append("https://www.bbc.com" + link)
            if article_links == []:
                raise HTTPException(
                    status_code=400, detail="Could not fetch BBC news, try again later"
                )
            return set(article_links)
        except:
            raise HTTPException(
                status_code=400, detail="Could not fetch BBC news, try again later"
            )


class CNN:
    def __init__(self):
        pass

    def get_articles(self) -> list[str]:
        try:
            url = "https://edition.cnn.com/world"
            article_links = []
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            zone = soup.find("div", class_="zone")
            articles = zone.find_all("a", class_="container__link")
            for article in articles:
                link = article.get("href")
                article_links.append("https://edition.cnn.com" + link)
            if article_links == []:
                raise HTTPException(
                    status_code=400, detail="Could not fetch CNN news, try again later"
                )
            return set(article_links)
        except:
            raise HTTPException(
                status_code=400, detail="Could not fetch CNN news, try again later"
            )
