import os

from dotenv import find_dotenv, load_dotenv
from langchain.agents import tool
from newsapi import NewsApiClient

load_dotenv(find_dotenv())

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

newsapi = NewsApiClient(api_key=NEWSAPI_KEY)


@tool
def scrape_top_news(category):
    try:
        response = newsapi.get_top_headlines(category=category)
        response = response["articles"][0:5]
        return response
    except Exception as e:
        print(e)


# curl GET https://newsapi.org/v2/top-headlines?category=technology&apiKey=132456789876543wert
# print(scrape_top_news("technology"))
