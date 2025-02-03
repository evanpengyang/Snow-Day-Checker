import requests
from bs4 import BeautifulSoup

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1335733996763484221/rwtwBd5lOsH4ucED0FBkjmgqtcTjnmw_bUUJIxw0RzXShoMHYSzmBopfW_G48_lnjfYQ"

URL = "https://stthomasmorecollegiate.ca/news/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

def discordBot(title, bodyText, confirmed):
    if confirmed == 1:
        message = f"❄ **Possible Snow Day Alert!** ❄\n\n**{title.text.strip()}**\n{bodyText.text.strip()}\n\n @everyone"
    elif confirmed == 2:
        message = f"❄ **Confirmed Snow Day Alert!** ❄\n\n**{title.text.strip()}**\n{bodyText.text.strip()}\n\n @everyone" 
    elif confirmed == 3:
        message = ("No news article mentioning 'snow' in the title or body") 
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)
    print("Sent webhook!")


news_item = soup.find("div", class_="nectar-post-grid-item")

heading = news_item.find("h2", class_="post-heading")
body = news_item.find("span", class_="meta-excerpt")
        
title = heading.text.strip().lower()
bodyText = body.text.strip().lower()

if "snow day" in title or "cancel" in bodyText or "cancelled" in bodyText or "no school" in bodyText:
    discordBot(heading, body, 1)
elif "snow" in title or "snow" in bodyText:
    discordBot(heading, body, 2)
else:
    discordBot(heading, body, 3)