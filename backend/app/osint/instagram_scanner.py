import requests
import re
import json

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}

FOLLOWER_RE = re.compile(r'"edge_followed_by":\{"count":(\d+)\}')
FOLLOWING_RE = re.compile(r'"edge_follow":\{"count":(\d+)\}')
POST_RE = re.compile(r'"edge_owner_to_timeline_media":\{"count":(\d+)\}')

def scan_instagram(username: str):
    url = f"https://www.instagram.com/{username}/"

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)

        if r.status_code != 200:
            return {"status": "not_found", "signals": {}}

        html = r.text

        if "Sorry, this page isn't available" in html:
            return {"status": "not_found", "signals": {}}

        follower_match = FOLLOWER_RE.search(html)
        following_match = FOLLOWING_RE.search(html)
        post_match = POST_RE.search(html)

        # 🔒 HARD CONFIRMATION RULE
        if not follower_match:
            return {"status": "not_found", "signals": {}}

        followers = int(follower_match.group(1))
        following = int(following_match.group(1)) if following_match else 0
        posts = int(post_match.group(1)) if post_match else 0

        return {
            "status": "confirmed",
            "url": url,
            "signals": {
                "followers": followers,
                "following": following,
                "posts": posts,
                "username_length": len(username),
                "is_verified_hint": '"is_verified":true' in html
            }
        }

    except Exception:
        return {"status": "error", "signals": {}}
