import requests

GITHUB_API = "https://api.github.com/users/{}"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "OSINT-Scanner"
}

def scan_github(username: str):
    r = requests.get(GITHUB_API.format(username), headers=HEADERS, timeout=8)

    if r.status_code == 404:
        return {
            "status": "not_found",
            "signals": {}
        }

    if r.status_code != 200:
        return {
            "status": "error",
            "signals": {}
        }

    data = r.json()

    return {
        "status": "confirmed",
        "url": data.get("html_url"),
        "signals": {
            "public_profile": True,
            "public_repos": data.get("public_repos", 0),
            "followers": data.get("followers", 0),
            "following": data.get("following", 0),
            "account_age_years": (
                2026 - int(data["created_at"][:4])
                if data.get("created_at")
                else 0
            ),
        }
    }
