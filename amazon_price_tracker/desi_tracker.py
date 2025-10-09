from bs4 import BeautifulSoup
import requests
from pprint import pprint



payload = { 'api_key': '9d01445e6684c179eee9d4d753060ca6', 'url': 'https://www.amazon.in/Apple-MacBook-13-inch-10-core-Unified/dp/B0DZDC247V/ref=sr_1_8?sr=8-8' }
r = requests.get('https://api.scraperapi.com/', params=payload)
print(r.text)


# soup = BeautifulSoup(data, "lxml")
# pprint(soup)