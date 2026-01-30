import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (OSINT Research Tool)"
}

PLATFORMS = {
    "github": {
        "url": "https://github.com/{username}",
        "exists_if": ["data-octo-click"],      # profile-specific marker
        "not_found_if": ["Not Found"],
    },
    "twitter": {
        "url": "https://twitter.com/{username}",
        "exists_if": ["profile"],               # profile container
        "not_found_if": ["This account doesn’t exist"],
    },
    "instagram": {
        "url": "https://www.instagram.com/{username}/",
        "exists_if": ["profilePage"],
        "not_found_if": ["Sorry, this page isn't available"],
    },
}

def scan_username(username: str):
    results = []

    for platform, cfg in PLATFORMS.items():
        url = cfg["url"].format(username=username)

        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)

            # 🚫 Blocked / rate-limited
            if resp.status_code in (401, 403, 429):
                results.append({
                    "platform": platform,
                    "exists": False,
                    "status": "blocked",
                    "url": url,
                })
                continue

            # ❌ Hard not found
            if resp.status_code == 404:
                results.append({
                    "platform": platform,
                    "exists": False,
                    "status": "not_found",
                    "url": url,
                })
                continue

            html = resp.text

            # ❌ Soft not found (200 but error page)
            if any(x in html for x in cfg["not_found_if"]):
                results.append({
                    "platform": platform,
                    "exists": False,
                    "status": "not_found",
                    "url": url,
                })
                continue

            # ✅ Confirmed existence
            if any(x in html for x in cfg["exists_if"]):
                results.append({
                    "platform": platform,
                    "exists": True,
                    "status": "confirmed",
                    "url": url,
                })
                continue

            # 🤷 Unknown page structure
            results.append({
                "platform": platform,
                "exists": False,
                "status": "error",
                "url": url,
            })

        except Exception:
            results.append({
                "platform": platform,
                "exists": False,
                "status": "error",
                "url": url,
            })

    return results
