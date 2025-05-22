import json
import os
import praw
from datetime import datetime

REDDIT_CLIENT_ID = "cj5WPnCz0zy3GkqjtVITfg"
REDDIT_CLIENT_SECRET = "hmFUQ8rmn13LD9An-AzzhMB4GtpwKA"
REDDIT_USER_AGENT = "Project"

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

stamp = datetime.now().timestamp()
print(stamp)
FILENAME = f"temp_posts.json"


def collect_user_posts(username, limit=10):
    posts = []
    try:
        for submission in reddit.redditor(username).submissions.new(limit=limit):
            posts.append({
                "title": submission.title,
                "text": submission.selftext,
            })
    except Exception as exception:
        print(f"[ERROR] Could not fetch posts: {exception}")
    return posts

posts = collect_user_posts("Unidan", limit=1000)

try:
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)
    print(f"[INFO] Saved {len(posts)} posts to {FILENAME}")
except Exception as exception:
    print(f"[ERROR] Could not save posts: {exception}")

try:
    with open(FILENAME, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"[INFO] Got posts.")
except Exception as exception:
    print(f"[ERROR] Could not load posts: {exception}")

print(f"[CLEANUP] Deleted temporary file: {FILENAME}")
