import ssl
import certifi
import os
import json
import re
import subprocess as sp
import requests
import trafilatura 
from dotenv import load_dotenv
from langchain.tools import tool
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from readability import Document
from pydantic import AnyUrl, BaseModel

load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
LANG_SEARCH_API_KEY = os.getenv("LANG_SEARCH_API_KEY")


def internet_search(query:str, result_count:int = 2)->str:
    """Get the information from the internet"""
    request = Request(
    "https://api.langsearch.com/v1/web-search",
    data=json.dumps({
        "query": f"{query}",
        "count": result_count, "contents": {"text": True}, "freshness": "noLimit"
    }).encode(),
    headers={
        "Authorization": f"Bearer {LANG_SEARCH_API_KEY}",
        "Content-Type": "application/json"
    }
    )
    
    #If get SSLCertVerificationError
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    with urlopen(request, timeout=30, context=ssl_context) as response:
        return json.load(response)


@tool
def scrape_url_tool(url: list[AnyUrl]) -> list[dict]:
    """
    Extract URLs from search results and scrape webpage content
    using BeautifulSoup.
    """

    scraped_pages = []

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    for link in url:
        try:
            response = requests.get(
                link,
                headers=headers,
                timeout=15
            )

            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove unwanted elements
            for tag in soup([
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "aside",
                "noscript"
            ]):
                tag.decompose()

            # Try to locate the main article
            article = soup.find("article")

            if not article:
                article = soup.find("main")

            if not article:
                article = soup.body or soup

            # Extract clean text
            content = article.get_text(
                separator="\n",
                strip=True
            )

            scraped_pages.append({
                "url": link,
                "content": content
            })

        except requests.RequestException as error:
            scraped_pages.append({
                "url": link,
                "content": None,
                "error": str(error)
            })

    return scraped_pages


@tool
def web_search_tool(query: str):
    """Search the details in web"""

    result = internet_search(query=query)

    data = []

    for res in result['data']['webPages']['value']:
        data.append({
            "Title":res['name'],
            "URL":res['url'],
            "Content":res['text']
            })

    return data