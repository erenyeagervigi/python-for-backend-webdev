import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇
response = requests.get(URL)
data = response.text

soup = BeautifulSoup(data, "html.parser")
movies_title = soup.find_all(name = "h3", class_ = "title")
for i in movies_title[::-1]:
    movie = i.getText()
    with open("movies.txt", "a", encoding="utf-8") as file:
        file.write(f"{movie} \n")
