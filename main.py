import os
from .env import load_dotenv
import requests
import feedparser
import time

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SUBREDDIT = os.getenv("SUBREDDIT")


# Track posted links
seen_posts = set()

def fetch_latest_post():
    url = f"https://www.reddit.com/r/{SUBREDDIT}/.rss"
    headers = {'User-Agent': 'Mozilla/5.0 (RealTimeBot)'}
    feed = feedparser.parse(requests.get(url, headers=headers).content)

    for entry in feed.entries:
        if entry.link not in seen_posts:
            seen_posts.add(entry.link)
            send_to_telegram(entry.title, entry.link)

def send_to_telegram(title, link):
    text = f"📢 {title}\n{link}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'disable_web_page_preview': False
    }
    response = requests.post(url, data=payload)
    if response.ok:
        print(f"✅ Sent: {title}")
    else:
        print(f"❌ Failed to send: {response.text}")

if __name__ == "__main__":
    print(f"🚀 Watching r/{SUBREDDIT}...")
    while True:
        fetch_latest_post()
        time.sleep(15)  # real-time check every 15 seconds
