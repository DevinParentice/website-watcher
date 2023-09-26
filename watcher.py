import json
import os
import requests
import time
import threading

from dotenv import load_dotenv
from utils import init_logger, send_email_alert, fetch_html, load_config

load_dotenv()

SENDING_EMAIL_USERNAME = os.environ.get("SENDER_EMAIL")
SENDING_EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
RECIPIENT_EMAIL_ADDRESS = os.environ.get("RECIPIENT_EMAIL")

if not os.path.exists("./logs"):
    os.makedirs("logs")


def webpage_has_changed(website, log):
    """Checks if the webpage has changed."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
    }

    if not os.path.exists("content.json"):
        open("content.json", "w+").close()

    website_name = website["name"]

    while True:
        log.info(f"{f'[{website_name}]':<15} | Beginning check")
        response = requests.get(website["url"], headers=headers)

        with open("content.json") as f:
            saved_content = json.load(f)

        new_content = fetch_html(response.text, website)

        if website_name not in saved_content:
            saved_content[website_name] = {}
        if new_content == saved_content[website_name]:
            log.info(f"{f'[{website_name}]':<15} | Check finished, no changes")
        else:
            stale_content = saved_content[website_name]
            saved_content[website_name] = new_content
            with open("content.json", "w", encoding="utf-8") as f:
                json.dump(saved_content, f, ensure_ascii=False)
            log.info(f"{f'[{website_name}]':<15} | Check finished, changes detected")
            if stale_content == {}:
                log.info(f"{f'[{website_name}]':<15} | First time website was scanned, skipping email")
            elif stale_content.keys() != new_content.keys():
                log.info(f"{f'[{website_name}]':<15} | First time item was scanned, skipping email")
            else:
                send_email_alert(
                    website,
                    stale_content,
                    new_content,
                    log,
                    SENDING_EMAIL_USERNAME,
                    SENDING_EMAIL_PASSWORD,
                    RECIPIENT_EMAIL_ADDRESS,
                )
        time.sleep(website["delay"] * 60)


def main():
    log = init_logger()
    log.info("Running Website Monitor")

    watcher_config = load_config()

    for website in watcher_config["websites"]:
        threading.Thread(target=webpage_has_changed, args=(website, log)).start()


if __name__ == "__main__":
    main()
