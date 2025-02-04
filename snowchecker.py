import requests
from bs4 import BeautifulSoup
import os

STMDISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
BURNABYDISCORD_WEBHOOK_URL = os.getenv("BURNABYDISCORD_WEBHOOK_URL")

webhook_list = [STMDISCORD_WEBHOOK_URL, BURNABYDISCORD_WEBHOOK_URL]

STMC_URL = "https://stthomasmorecollegiate.ca/news/"
BURNABY_URL = "https://burnabyschools.ca/"
stmpage = requests.get(STMC_URL)
burnabypage = requests.get(BURNABY_URL)

stmsoup = BeautifulSoup(stmpage.content, "html.parser")
burnabysoup = BeautifulSoup(burnabypage.content, "html.parser")

scrape_rules = { #nested dictionary allows for scraper function to be reused for many different websites
    "stmc": {
        "container": ("div", "nectar-post-grid-item"),
        "heading": ("h2", "post-heading"),
        "body": ("span", "meta-excerpt")
    },
    "burnaby": {
        "container": ("ul", "hfeed"),
        "heading": ("h3", "entry-title"),
        "body": ("div", "entry-summary")
    }
}

def discordBot(title, bodyText, alert_type, bot_type = 0):
    bot_type = 0 if bot_type == stmsoup else 1 #checks if whichSoup is STMSoup, that way it can differntiate between which integration to use

    messages = [
        f"❄ **Confirmed Snow Day Alert!** ❄\n\n**{title.text.strip()}**\n{bodyText.text.strip()}\n\n @everyone",
        f"❄ **Possible Snow Day Alert!** ❄\n\n**{title.text.strip()}**\n{bodyText.text.strip()}\n\n @everyone",
        "No news article mentioning 'snow' in the title or body"
    ]

    payload = {"content": messages[alert_type]}
    requests.post(webhook_list[bot_type], json=payload) #posts the webhook to the discord server via different integrations depending on which webpage it scraped 'Burnaby' or 'STM'
    print(f"Sent webhook to {['STM', 'Burnaby'][bot_type]}!")


def scraper(whichSoup):
    rules = scrape_rules["stmc"] if whichSoup == stmsoup else scrape_rules["burnaby"] #decides whether to take dictionary values from stmc or burnaby

    news_item = whichSoup.find(*rules["container"]) # * unpacks the tuple in the container part of the nested dictionaries
    heading = news_item.find(*rules["heading"])
    body = news_item.find(*rules["body"])
            
    title = heading.text.strip().lower()
    bodyText = body.text.strip().lower()

    if "snow day" in title or "cancel" in bodyText or "cancelled" in bodyText or "no school" in bodyText or "school closure" in title:
        discordBot(heading, body, 0, whichSoup)
    elif "snow" in title or "snow" in bodyText:
        discordBot(heading, body, 1, whichSoup)
    else:
        discordBot(heading, body, 2, whichSoup)


scraper(stmsoup)
scraper(burnabysoup)