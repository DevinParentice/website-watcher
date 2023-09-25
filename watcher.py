import requests
import json
import threading
import os

from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup

import yagmail
import time
import logging

load_dotenv()

SENDING_EMAIL_USERNAME = os.environ.get("SENDER_EMAIL")
SENDING_EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
RECIPIENT_EMAIL_ADDRESS = os.environ.get("RECIPIENT_EMAIL")


def send_email_alert(website, stale_content, new_content, log):
    """Sends an email alert. The subject and body will be the same."""
    website_name = website["name"]
    log.info(f"{f'[{website_name}]':<15} | Sending an email alert")
    changed_classes = []
    for key in stale_content:
        if stale_content[key] != new_content[key]:
            changed_classes.append(key)

    email_content = f"<!doctype html><html xmlns='http://www.w3.org/1999/xhtml' xmlns:v='urn:schemas-microsoft-com:vml' xmlns:o='urn:schemas-microsoft-com:office:office'><head><title>Website watcher</title><!--[if !mso]><!--><meta http-equiv='X-UA-Compatible' content='IE=edge'><!--<![endif]--><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'><style type='text/css'>#outlook a {{ padding:0; }}body {{ margin:0;padding:0; }}img {{ border:0;height:auto;line-height:100%; outline:none;text-decoration:none; }}p {{ display:block;margin:13px 0; }}</style><style type='text/css'>@media only screen and (min-width:480px) {{.mj-column-per-100 {{ width:100% !important; max-width: 100%; }}.mj-column-per-40 {{ width:40% !important; max-width: 40%; }}.mj-column-per-60 {{ width:60% !important; max-width: 60%; }}.mj-column-per-80 {{ width:80% !important; max-width: 80%; }}}}</style><style media='screen and (min-width:480px)'>.moz-text-html .mj-column-per-100 {{ width:100% !important; max-width: 100%; }}.moz-text-html .mj-column-per-40 {{ width:40% !important; max-width: 40%; }}.moz-text-html .mj-column-per-60 {{ width:60% !important; max-width: 60%; }}.moz-text-html .mj-column-per-80 {{ width:80% !important; max-width: 80%; }}</style><style type='text/css'>@media only screen and (max-width:480px) {{table.mj-full-width-mobile {{ width: 100% !important; }}td.mj-full-width-mobile {{ width: auto !important; }}}}</style></head><body style='word-spacing:normal;background-color:#F2F2F2;'><div style='background-color:#F2F2F2;'><!--[if mso | IE]><table align='center' border='0' cellpadding='0' cellspacing='0' class='' style='width:600px;' width='600' ><tr><td style='line-height:0px;font-size:0px;mso-line-height-rule:exactly;'><![endif]--><div style='margin:0px auto;max-width:600px;'><table align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='width:100%;'><tbody><tr><td style='direction:ltr;font-size:0px;padding:10px 0 20px 0;text-align:center;'><!--[if mso | IE]><table role='presentation' border='0' cellpadding='0' cellspacing='0'><tr><td class='' style='vertical-align:top;width:600px;' ><![endif]--><div class='mj-column-per-100 mj-outlook-group-fix' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;'><table border='0' cellpadding='0' cellspacing='0' role='presentation' style='vertical-align:top;' width='100%'><tbody></tbody></table></div><!--[if mso | IE]></td></tr></table><![endif]--></td></tr></tbody></table></div><!--[if mso | IE]></td></tr></table><table align='center' border='0' cellpadding='0' cellspacing='0' class='' style='width:600px;' width='600' bgcolor='#FFFFFF' ><tr><td style='line-height:0px;font-size:0px;mso-line-height-rule:exactly;'><![endif]--><div style='background:#FFFFFF;background-color:#FFFFFF;margin:0px auto;max-width:600px;'><table align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='background:#FFFFFF;background-color:#FFFFFF;width:100%;'><tbody><tr><td style='direction:ltr;font-size:0px;padding:20px 20px 0 20px;text-align:center;'><!--[if mso | IE]><table role='presentation' border='0' cellpadding='0' cellspacing='0'><tr><td class='' style='vertical-align:top;width:224px;' ><![endif]--><div class='mj-column-per-40 mj-outlook-group-fix' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;'><table border='0' cellpadding='0' cellspacing='0' role='presentation' style='vertical-align:top;' width='100%'><tbody><tr><td align='left' style='font-size:0px;padding:10px 25px;word-break:break-word;'><div style='font-family:Montserrat, Helvetica, Arial, sans-serif;font-size:20px;font-weight:500;line-height:24px;text-align:left;color:#000000;'>// Website Watcher</div></td></tr></tbody></table></div><!--[if mso | IE]></td><td class='' style='vertical-align:top;width:336px;' ><![endif]--><div class='mj-column-per-60 mj-outlook-group-fix' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;'><table border='0' cellpadding='0' cellspacing='0' role='presentation' style='vertical-align:top;' width='100%'><tbody></tbody></table></div><!--[if mso | IE]></td></tr></table><![endif]--></td></tr></tbody></table></div><!--[if mso | IE]></td></tr></table><table align='center' border='0' cellpadding='0' cellspacing='0' class='' style='width:600px;' width='600' bgcolor='#FFFFFF' ><tr><td style='line-height:0px;font-size:0px;mso-line-height-rule:exactly;'><![endif]--><div style='background:#FFFFFF;background-color:#FFFFFF;margin:0px auto;max-width:600px;'><table align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='background:#FFFFFF;background-color:#FFFFFF;width:100%;'><tbody><tr><td style='direction:ltr;font-size:0px;padding:20px 20px 0 20px;text-align:center;'><!--[if mso | IE]><table role='presentation' border='0' cellpadding='0' cellspacing='0'><tr><td class='' style='vertical-align:top;width:560px;' ><![endif]--><div class='mj-column-per-100 mj-outlook-group-fix' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;'><table border='0' cellpadding='0' cellspacing='0' role='presentation' style='vertical-align:top;' width='100%'><tbody><tr><td align='center' style='font-size:0px;padding:30px 40px 10px 40px;word-break:break-word;'><div style='font-family:Montserrat, Helvetica, Arial, sans-serif;font-size:32px;font-weight:300;line-height:40px;text-align:center;color:#5d96f6;'>A change has been detected on {website_name}</div></td></tr></tbody></table></div><!--[if mso | IE]></td></tr></table><![endif]--></td></tr></tbody></table></div><!--[if mso | IE]></td></tr></table><table align='center' border='0' cellpadding='0' cellspacing='0' class='' style='width:600px;' width='600' bgcolor='#FFFFFF' ><tr><td style='line-height:0px;font-size:0px;mso-line-height-rule:exactly;'><![endif]--><div style='background:#FFFFFF;background-color:#FFFFFF;margin:0px auto;max-width:600px;'><table align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='background:#FFFFFF;background-color:#FFFFFF;width:100%;'><tbody><tr><td style='direction:ltr;font-size:0px;padding:10px 20px;text-align:center;'><!--[if mso | IE]><table role='presentation' border='0' cellpadding='0' cellspacing='0'><tr><td class='' style='vertical-align:top;width:560px;' ><![endif]--><div class='mj-column-per-100 mj-outlook-group-fix' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;'><table border='0' cellpadding='0' cellspacing='0' role='presentation' style='vertical-align:top;' width='100%'><tbody><tr><td align='center' style='font-size:0px;padding:10px 25px;word-break:break-word;'><p style='border-top:solid 3px #9B9B9B;font-size:1px;margin:0px auto;width:30px;'></p><!--[if mso | IE]><table align='center' border='0' cellpadding='0' cellspacing='0' style='border-top:solid 3px #9B9B9B;font-size:1px;margin:0px auto;width:30px;' role='presentation' width='30px' ><tr><td style='height:0;line-height:0;'> &nbsp;</td></tr></table><![endif]--></td></tr></tbody></table></div><!--[if mso | IE]></td></tr></table><![endif]--></td></tr></tbody></table></div><!--[if mso | IE]></td></tr></table><table align='center' border='0' cellpadding='0' cellspacing='0' class='' style='width:600px;' width='600' bgcolor='#FFFFFF' ><tr><td style='line-height:0px;font-size:0px;mso-line-height-rule:exactly;'><![endif]--><div style='background:#FFFFFF;background-color:#FFFFFF;margin:0px auto;max-width:600px;'><table align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='background:#FFFFFF;background-color:#FFFFFF;width:100%;'><tbody><tr><td style='direction:ltr;font-size:0px;padding:0 20px 20px 20px;text-align:center;'><!--[if mso | IE]><table role='presentation' border='0' cellpadding='0' cellspacing='0'><tr><td class='' style='vertical-align:top;width:448px;' ><![endif]--><div class='mj-column-per-80 mj-outlook-group-fix' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;'><table border='0' cellpadding='0' cellspacing='0' role='presentation' style='vertical-align:top;' width='100%'><tbody>"

    for changed_class in changed_classes:
        email_content += f"<tr><td align='center' style='font-size:0px;padding:0px;padding-top:10px;word-break:break-word;'><div style='font-family:Montserrat, Helvetica, Arial, sans-serif;font-size:16px;font-weight:500;line-height:24px;text-align:center;color:#000000;'>Your watched tag '{changed_class}' has been updated:</div></td></tr>"

    email_content += f"</tbody></table></div><!--[if mso | IE]></td></tr></table><![endif]--></td></tr></tbody></table></div><!--[if mso | IE]></td></tr></table><table align='center' border='0' cellpadding='0' cellspacing='0' class='' style='width:600px;' width='600' ><tr><td style='line-height:0px;font-size:0px;mso-line-height-rule:exactly;'><v:rect style='width:600px;' xmlns:v='urn:schemas-microsoft-com:vml' fill='true' stroke='false'><v:fill origin='0, -0.5' position='0, -0.5' src='https://htmlcolorcodes.com/assets/images/colors/baby-blue-color-solid-background-1920x1080.png' type='frame' size='1,1' aspect='atleast' /><v:textbox style='mso-fit-shape-to-text:true' inset='0,0,0,0'><![endif]--><div style='background:url(https://htmlcolorcodes.com/assets/images/colors/baby-blue-color-solid-background-1920x1080.png) center top / cover no-repeat;background-position:center top;background-repeat:no-repeat;background-size:cover;margin:0px auto;max-width:600px;'><div style='line-height:0;font-size:0;'><table align='center' background='https://htmlcolorcodes.com/assets/images/colors/baby-blue-color-solid-background-1920x1080.png' border='0' cellpadding='0' cellspacing='0' role='presentation' style='background:url(https://htmlcolorcodes.com/assets/images/colors/baby-blue-color-solid-background-1920x1080.png) center top / cover no-repeat;background-position:center top;background-repeat:no-repeat;background-size:cover;width:100%;'><tbody><tr><td style='direction:ltr;font-size:0px;padding:0px;text-align:center;'><!--[if mso | IE]><table role='presentation' border='0' cellpadding='0' cellspacing='0'><tr><td class='' style='vertical-align:top;width:600px;' ><![endif]--><div class='mj-column-per-100 mj-outlook-group-fix' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;'><table border='0' cellpadding='0' cellspacing='0' role='presentation' style='vertical-align:top;' width='100%'><tbody><tr><td align='center' style='font-size:0px;padding:0px;word-break:break-word;'><table border='0' cellpadding='0' cellspacing='0' role='presentation' style='border-collapse:collapse;border-spacing:0px;'><tbody><tr><td style='width:600px;'><img alt='' height='auto' src='http://nimus.de/share/tpl-card/lineshadow.png' style='border:none;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;' width='600'></td></tr></tbody></table></td></tr>"

    for changed_class in changed_classes:
        email_content += f"<tr><td align='center' style='font-size:0px;padding:50px 40px 0 40px;word-break:break-word;'><div style='font-family:Montserrat, Helvetica, Arial, sans-serif;font-size:16px;font-weight:300;line-height:24px;text-align:center;color:#000000;'>{stale_content[changed_class]} -> {new_content[changed_class]}</div></td></tr>"

    email_content += f"<tr><td align='center' vertical-align='middle' style='font-size:0px;padding:10px 25px;padding-top:20px;padding-bottom:100px;word-break:break-word;'><table border='0' cellpadding='0' cellspacing='0' role='presentation' style='border-collapse:separate;line-height:100%;'><tr><td align='center' bgcolor='#5d96f6' role='presentation' style='border:none;border-radius:2px;cursor:auto;mso-padding-alt:15px 30px;background:#5d96f6;' valign='middle'><a href='{website['url']}' style='display:inline-block;background:#5d96f6;color:#FFFFFF;font-family:Montserrat, Helvetica, Arial, sans-serif;font-size:13px;font-weight:normal;line-height:120%;margin:0;text-decoration:none;text-transform:none;padding:15px 30px;mso-padding-alt:0px;border-radius:2px;' target='_blank'>View Page</a></td></tr></table></td></tr></tbody></table></div><!--[if mso | IE]></td></tr></table><![endif]--></td></tr></tbody></table></div></div><!--[if mso | IE]></v:textbox></v:rect></td></tr></table><table align='center' border='0' cellpadding='0' cellspacing='0' class='' style='width:600px;' width='600' bgcolor='#FFFFFF' ><tr><td style='line-height:0px;font-size:0px;mso-line-height-rule:exactly;'><![endif]--><div style='background:#FFFFFF;background-color:#FFFFFF;margin:0px auto;max-width:600px;'><table align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='background:#FFFFFF;background-color:#FFFFFF;width:100%;'><tbody><tr><td style='direction:ltr;font-size:0px;padding:50px 0 0 0;text-align:center;'><!--[if mso | IE]><table role='presentation' border='0' cellpadding='0' cellspacing='0'><tr><td class='' style='vertical-align:top;width:600px;' ><![endif]--><div class='mj-column-per-100 mj-outlook-group-fix' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;'><table border='0' cellpadding='0' cellspacing='0' role='presentation' style='vertical-align:top;' width='100%'><tbody><tr><td align='center' style='font-size:0px;padding:0px;word-break:break-word;'><table border='0' cellpadding='0' cellspacing='0' role='presentation' style='border-collapse:collapse;border-spacing:0px;'><tbody><tr><td style='width:600px;'><img alt='bottom border' height='auto' src='http://nimus.de/share/tpl-card/bottom.png' style='border:none;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;' width='600'></td></tr></tbody></table></td></tr></tbody></table></div>"

    try:
        yagmail.SMTP(SENDING_EMAIL_USERNAME, SENDING_EMAIL_PASSWORD).send(
            RECIPIENT_EMAIL_ADDRESS, f"Update detected on {website_name}", email_content
        )
        log.info(f"{f'[{website_name}]':<15} | Successfully sent email")
    except Exception as e:
        log.error(f"{f'[{website_name}]':<15} | Error sending email:\n\n{e}\n\n")


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
                send_email_alert(website, stale_content, previous_content[website_name], log)
        time.sleep(website["delay"] * 60)


def main():
    now = datetime.now()
    log = logging.getLogger(__name__)
    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "INFO"),
        format="[%(asctime)s] | [%(levelname)s] | %(message)s",
        handlers=[
            logging.FileHandler(f"website_monitor_{now.year}_{now.month}_{now.day}_{now.hour}.log"),
            logging.StreamHandler(),
        ],
    )
    log.info("Running Website Monitor")

    with open("config.json") as config:
        json_data = json.load(config)

    for website in json_data["websites"]:
        threading.Thread(target=webpage_was_changed, args=(website, log)).start()


if __name__ == "__main__":
    main()
