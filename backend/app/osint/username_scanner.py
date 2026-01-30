import requests
from typing import Dict, List

HEADERS = {
    "User-Agent": "Mozilla/5.0 (OSINT Research Tool)"
}

TIMEOUT = 10


def scan_username(username: str) -> List[Dict]:
    results = []

    results.append(check_github(username))
    results.append(check_twitter(username))
    results.append(check_instagram(username))

    return results


# ---------------- GITHUB ----------------
def check_github(username: str) -> Dict:
    url = f"https://github.com/{username}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)

        if r.status_code == 404:
            return {
                "platform": "github",
                "status": "not_found",
                "exists": False,
                "url": None,
            }

        if r.status_code == 200 and f'"login":"{username}"' in r.text:
            return {
                "platform": "github",
                "status": "confirmed",
                "exists": True,
                "url": url,
            }

        return {
            "platform": "github",
            "status": "error",
            "exists": False,
            "url": None,
        }

    except requests.RequestException:
        return {
            "platform": "github",
            "status": "error",
            "exists": False,
            "url": None,
        }


# ---------------- TWITTER / X ----------------
def check_twitter(username: str) -> Dict:
    url = f"https://twitter.com/{username}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        text = r.text.lower()

        if "this account doesn’t exist" in text or "account suspended" in text:
            return {
                "platform": "twitter",
                "status": "not_found",
                "exists": False,
                "url": None,
            }

        if f"@{username.lower()}" in text:
            return {
                "platform": "twitter",
                "status": "confirmed",
                "exists": True,
                "url": url,
            }

        return {
            "platform": "twitter",
            "status": "blocked",
            "exists": False,
            "url": None,
        }

    except requests.RequestException:
        return {
            "platform": "twitter",
            "status": "error",
            "exists": False,
            "url": None,
        }


# ---------------- INSTAGRAM ----------------
def check_instagram(username: str) -> Dict:
    url = f"https://www.instagram.com/{username}/"

    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)

        if r.status_code == 404:
            return {
                "platform": "instagram",
                "status": "not_found",
                "exists": False,
                "url": None,
            }

        if f'"username":"{username}"' in r.text:
            return {
                "platform": "instagram",
                "status": "confirmed",
                "exists": True,
                "url": url,
            }

        return {
            "platform": "instagram",
            "status": "blocked",
            "exists": False,
            "url": None,
        }

    except requests.RequestException:
        return {
            "platform": "instagram",
            "status": "error",
            "exists": False,
            "url": None,
        }
