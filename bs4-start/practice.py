from bs4 import BeautifulSoup
import requests

response = requests.get("https://news.ycombinator.com/news")
data = response.text

soup = BeautifulSoup(data, "html.parser")
article = soup.find_all(name = "span", class_= "titleline")
article_text = [i.getText() for i in article]
article_link = [i.find("a").get("href") for i in article]
article_score = [int(i.getText().split()[0]) for i in soup.find_all(name = "span", class_ = "score")]

article_max = article_score.index(max(article_score))

print(article_text[article_max])
print(article_link[article_max])
print(article_score[article_max])