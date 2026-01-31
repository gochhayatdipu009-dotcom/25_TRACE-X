from app.osint.github_scanner import scan_github
from app.osint.instagram_scanner import scan_instagram

def scan_username(username: str):
    results = []

    gh = scan_github(username)
    results.append({
        "platform": "github",
        **gh
    })

    ig = scan_instagram(username)
    results.append({
        "platform": "instagram",
        **ig
    })

    return results
