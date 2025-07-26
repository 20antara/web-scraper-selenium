import os
import requests
import logging

logger = logging.getLogger(__name__)


def translate_text(texts: list, source: str = "es", target: str = "en") -> list:
    """
    Translate text using the Rapid Translate Multi Traduction API.
    """
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
    if not RAPIDAPI_KEY:
        logger.error("Missing RAPIDAPI_KEY. Please set it as an environment variable.")
        return ""
        
    url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
    payload = {
        "from": source,
        "to": target,
        "q": texts,
        "e": ""
    }
    headers = {
        "content-type": "application/json",
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        res_json = response.json()
        
        if isinstance(res_json, list):
            return res_json
        else:
            raise RuntimeError(f"Unexpected API response format: {res_json}")
        
    except Exception as e:
        logger.error(f"Translation failed for '{texts}'")
        raise
