from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import smtplib

load_dotenv(".env")
URL = os.getenv("URL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
BUY_PRICE = 100

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
              "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en,ka;q=0.9"
}


def send_email():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg=(f"Subject: Best Amazon Price!\n\n"
                 f"For the item: {item_title}\nBest price is: ${item_price},"
                 f"\nWhat are you waiting for!!!\nNavigate to buy: {URL}").encode("utf-8")
        )


try:
    response = requests.get(url=URL, headers=HEADERS)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    item_price = int(soup.find(name="span", class_="a-price-whole").getText().rstrip("."))
    item_title = soup.find(name="span", id="productTitle").getText().strip()
except AttributeError as atr_error:
    print(f"Error: {atr_error}")
else:
    if item_price < BUY_PRICE:
        send_email()
