import ssl
import certifi
import os
import json
import subprocess as sp
from dotenv import load_dotenv
from langchain.tools import tool
from urllib.request import Request, urlopen

load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
LANG_SEARCH_API_KEY = os.getenv("LANG_SEARCH_API_KEY")


# @tool
def internet_search(query:str, result_count:int = 5)->str:
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


def web_search_tool(query: str):
    """Get details from web by web search"""
    result = internet_search(query=query)

    data = []

    for res in result['data']['webPages']['value']:
        data.append(f"Title:{res['name']}.\nURL:{res['url']}\nContent:{res['text']}\n\n-----\n\n")

    return data