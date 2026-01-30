# backend/app/osint/username_scanner.py

import requests
from app.utils.logger import logger

PLATFORMS = {
    "github": "https://github.com/{username}",
    "twitter": "https://twitter.com/{username}",
    "instagram": "https://www.instagram.com/{username}",
}


def scan_username(username: str) -> list[dict]:
    """
    Scan username across supported platforms.
    Returns structured exposure data.
    """

    results = []

    headers = {
        "User-Agent": "OSINT-SaaS-Scanner/1.0"
    }

    for platform, url_template in PLATFORMS.items():
        url = url_template.format(username=username)

        try:
            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                logger.info(f"[FOUND] {platform}: {url}")
                results.append({
                    "platform": platform,
                    "url": url,
                    "exists": True,
                    "confidence": 0.6
                })
            else:
                logger.info(f"[MISS] {platform}: {url}")
                results.append({
                    "platform": platform,
                    "url": url,
                    "exists": False,
                    "confidence": 0.0
                })

        except requests.RequestException as e:
            logger.warning(f"[ERROR] {platform}: {e}")
            results.append({
                "platform": platform,
                "url": url,
                "exists": False,
                "confidence": 0.0,
                "error": str(e)
            })

    return results
