import ssl
import certifi
import os
import subprocess as sp
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
LANG_SEARCH_API_KEY = os.getenv("LANG_SEARCH_API_KEY")


@tool
def internet_search_tool(query:str, result_count:int = 5)->str:
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
    # with urlopen(request, timeout=30) as response:
    #     return json.load(response)

    #If get SSLCertVerificationError
    ssl_context = ssl.create_default_context(cafile=certifi.where())