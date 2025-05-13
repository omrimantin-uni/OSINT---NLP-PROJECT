import json
import re


INPUT_FILE = "temp_posts.json"
OUTPUT_FILE = "clean_posts.json"


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)         # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()# remove extra spaces
    return text

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    posts = json.load(f)

cleaned_posts = []
cnt = 0
for post in posts:
    text = clean_text(post["text"])
    title = clean_text(post["title"])

    if text.strip():  # keep only posts with non-empty text
        cnt += 1
        cleaned_posts.append({
            "title": title,
            "text": text
        })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned_posts, f, ensure_ascii=False, indent=4)

print(f"[INFO] {cnt} Cleaned and saved posts.")
