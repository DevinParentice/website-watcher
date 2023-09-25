import requests
import json
import threading
import os
from dotenv import load_dotenv

from bs4 import BeautifulSoup

import yagmail
import time
import logging

load_dotenv()

SENDING_EMAIL_USERNAME = os.environ.get("SENDER_EMAIL")
SENDING_EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
RECIPIENT_EMAIL_ADDRESS = os.environ.get("RECIPIENT_EMAIL")


def send_email_alert(website_name, stale_content, new_content, log):
    """Sends an email alert. The subject and body will be the same."""
    log.info(f"Sending an email alert - SITE: {website_name}")
    changed_classes = []
    for key in stale_content:
        if stale_content[key] != new_content[key]:
            changed_classes.append(key)

    email_content = "Content that changed:\n\n"
    for changed_class in changed_classes:
        email_content += f"""
            {website_name} had a change on {changed_class}!
 
            {stale_content[changed_class]} -> {new_content[changed_class]}.\n\n	
	    """
    try:
        yagmail.SMTP(SENDING_EMAIL_USERNAME, SENDING_EMAIL_PASSWORD).send(
            RECIPIENT_EMAIL_ADDRESS, f"Update detected on {website_name}", email_content
        )
        log.info(f"{f'[{website_name}]':<15} | Successfully sent email")
    except:
        log.error(f"{f'[{website_name}]':<15} | Error sending email")


def fetch_html(string, website):
    soup = BeautifulSoup(string, features="lxml")

    # make the html look good
    soup.prettify()

    # remove script tags
    for s in soup.select("script"):
        s.extract()

    # remove meta tags
    for s in soup.select("meta"):
        s.extract()

    new_content = {}
    for element in website["elements"]:
        new_content[element["class"]] = str(
            soup.find_all(element["tag"], class_=element["class"])[0].get_text(strip=True)
        ).replace("\r", "")

    return new_content


def webpage_was_changed(website, log):
    """Returns true if the webpage was changed, otherwise false."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
    }

    # create the previous_content.txt if it doesn't exist
    if not os.path.exists("content.json"):
        open("content.json", "w+").close()
    website_name = website["name"]
    while True:
        log.info(f"{f'[{website_name}]':<15} | Beginning check")
        response = requests.get(website["url"], headers=headers)

        with open("content.json") as f:
            previous_content = json.load(f)

        new_content = fetch_html(response.text, website)

        if website_name not in previous_content:
            previous_content[website_name] = {}
        if new_content == previous_content[website_name]:
            log.info(f"{f'[{website_name}]':<15} | Check finished, no changes")
        else:
            stale_content = previous_content[website_name]
            previous_content[website_name] = new_content
            with open("content.json", "w", encoding="utf-8") as f:
                json.dump(previous_content, f, ensure_ascii=False)
            log.info(f"{f'[{website_name}]':<15} | Check finished, changes detected")
            if stale_content != {}:
                send_email_alert(website_name, stale_content, previous_content[website_name], log)
        time.sleep(website["delay"] * 60)


def main():
    log = logging.getLogger(__name__)
    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "INFO"),
        format="[%(asctime)s] | [%(levelname)s] | %(message)s",
        filemode="a",
        filename="website_monitor.log",
    )
    log.info("Running Website Monitor")

    with open("config.json") as config:
        json_data = json.load(config)

    for website in json_data["websites"]:
        threading.Thread(target=webpage_was_changed, args=(website, log)).start()


if __name__ == "__main__":
    main()
