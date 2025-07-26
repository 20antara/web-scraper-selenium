import requests
import os
import logging

logger = logging.getLogger(__name__)

def download_image(image_url: str, save_path: str) -> bool:
    """
    Downloads image from img tag and saves locally
    """
    try:
        r = requests.get(image_url, stream=True, timeout=10)
        if r.status_code == 200:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            logger.info(f"Image downloaded: {save_path}")
            return True
        else:
            logger.warning(f"Image URL {image_url} could not be fetched, status: {r.status_code}")
            return False
    except Exception as e:
        logger.error(f"Failed to download image {image_url}")
        raise