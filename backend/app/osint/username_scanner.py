import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (OSINT-Research)",
    "Accept": "text/html",
}

TIMEOUT = 8


def scan_username(username: str):
    results = []

    platforms = {
        "github": f"https://github.com/{username}",
        "instagram": f"https://www.instagram.com/{username}/",
    }

    for platform, url in platforms.items():
        try:
            resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            text = resp.text.lower()

            # -------- GITHUB --------
            if platform == "github":
                if resp.status_code == 200 and "not found" not in text:
                    status = "confirmed"
                elif resp.status_code == 404:
                    status = "not_found"
                else:
                    status = "error"

            # -------- INSTAGRAM --------
            elif platform == "instagram":
                if "sorry, this page isn't available" in text:
                    status = "not_found"
                elif f'"username":"{username.lower()}"' in text:
                    status = "confirmed"
                elif "profilepage_" in text:
                    status = "confirmed"
                else:
                    status = "blocked"

            results.append({
                "platform": platform,
                "status": status,
                "url": url if status == "confirmed" else None,
            })

        except requests.RequestException:
            results.append({
                "platform": platform,
                "status": "error",
                "url": None,
            })

    return results
