import os

import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv

load_dotenv("important.env")

my_email = "vignesh13006@gmail.com"
password = os.getenv("password")
headers = {
    "Accept-Language":"en-US,en;q=0.8",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept-Encoding" : "gzip, deflate, br, zstd",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
}

response = requests.get("https://appbrewery.github.io/instant_pot", headers=headers)
data = response.text

soup = BeautifulSoup(data, "html.parser")
price = soup.find(name="span", class_ = "aok-offscreen").getText().split("$")[1]
print(price)

product_name = " ".join(soup.find(name="span", id= "productTitle").getText().split())
print(product_name)

message = f"SUBJECT: AMAZON PRICE ALERT \n\n {product_name} is now at ${price}"

buy_price = 100

if float(price) < buy_price:
    with smtplib.SMTP(host= "smtp.gmail.com", port= 587) as connection:
        connection.starttls()
        connection.login(user= my_email, password=password)
        connection.sendmail(to_addrs="for.signuporlogin@gmail.com", from_addr=my_email, msg = message.encode("utf-8") )

