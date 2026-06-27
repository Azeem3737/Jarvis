import os
import requests
import logging
from dotenv import load_dotenv
from livekit.agents import function_tool  # ✅ Correct decorator
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@function_tool
async def google_search(query: str) -> str:
    logger.info(f"Query حاصل ہونا۔: {query}")

    api_key = os.getenv("AQ.Ab8RN6JLv9rlhyzPjmUIHT72DpugzLJmFR08ifaiHM1xIpNIzg")
    search_engine_id = os.getenv("478ffb58725654a08")

    if not api_key or not search_engine_id:
        logger.error("API key یا Search Engine ID missing ہے")
        return "Environment variables میں API key یا Search Engine ID missing ہے۔"

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": query,
        "num": 3
    }

    logger.info("Google Custom Search API کو request ...")
    response = requests.get(url, params=params)

    if response.status_code != 200:
        logger.error(f"Google API میں error آیا: {response.status_code} - {response.text}")
        return f"Google Search API میں error آیا: {response.status_code} - {response.text}"

    data = response.json()
    results = data.get("items", [])

    if not results:
        logger.info("کوئی results نہیں ملے۔")
        return "کوئی results نہیں ملے۔"

    formatted = ""
    logger.info("Search results:")
    for i, item in enumerate(results, start=1):
        title = item.get("title", "No title")
        link = item.get("link", "No link")
        snippet = item.get("snippet", "")
        formatted += f"{i}. {title}\n{link}\n{snippet}\n\n"
        logger.info(f"{i}. {title}\n{link}\n{snippet}\n")

    return formatted.strip()

@function_tool
async def get_current_datetime() -> str:
    return datetime.now().isoformat()

