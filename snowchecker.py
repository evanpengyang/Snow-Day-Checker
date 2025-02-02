import requests
from bs4 import BeautifulSoup

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1335733996763484221/rwtwBd5lOsH4ucED0FBkjmgqtcTjnmw_bUUJIxw0RzXShoMHYSzmBopfW_G48_lnjfYQ"

URL = "https://stthomasmorecollegiate.ca/news/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

news_items = soup.find_all("div", class_="nectar-post-grid-item")

def discordBot(title, bodyText, confirmed):
    if confirmed == False:
        message = f"❄ **Possible Snow Day Alert!** ❄\n\n**{title.text.strip()}**\n{bodyText.text.strip()}\n\n @everyone"
    else:
        message = f"❄ **Confirmed Snow Day Alert!** ❄\n\n**{title.text.strip()}**\n{bodyText.text.strip()}\n\n @everyone"  
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)
    print("Sent webhook!")


for item in news_items:
    heading = item.find("h2", class_="post-heading")
    body = item.find("span", class_="meta-excerpt")
        
    title = heading.text.strip().lower()
    bodyText = body.text.strip().lower()

    if "snow day" in title or "cancel" in bodyText or "cancelled" in bodyText or "no school" in bodyText:
        discordBot(heading, body, True)
    elif "snow" in title or "snow" in bodyText:
        discordBot(heading, body, False)
    else:
        print("No article mentioning 'snow' in the title or body")