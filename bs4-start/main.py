# #used for reading the data from the html file
# with open("website.html") as file:
#     data = file.read()

# #the BeautifulSoup class takes the data which has been read with html.parser
# soup = BeautifulSoup(data, "html.parser")

# #used to print the first data of the specific tag u desire
# print(soup.title)
# print(soup.a)
#
# #used to print the only text from the specific tag u provided
# print(soup.title.text)
# print(soup.a.text)

# #find_all(name= "") is used to find all the specific tag u need present in the html
# all_ancor_tags = soup.find_all(name="a")

# #to get the text of all the specific tag u would use a for loop and to extract the text from each loop u would use getText()
# for i in all_ancor_tags:
#     print(i.getText())

# #to get the links from an ancor tag u will loop through it and extract the links using .get()
# for i in all_ancor_tags:
#     print(i.get("href"))

# #finding specific tags with attributes .find_all(name= "tag name", id="respective id")
# print(soup.find_all(name = "h1", id= "name"))

# #finding specific tags with attributes .find_all(name= "tag name", class_="class_name")
# print(soup.find_all(name = "h1", class_= "class_name"))

#select_one is used to find one specific tag you're looking for
#select selects all the tags
# print(soup.select_one(selector= "p a").getText())

from bs4 import BeautifulSoup
import requests

response = requests.get("https://appbrewery.github.io/news.ycombinator.com/")
data = response.text

soup = BeautifulSoup(data, "html.parser")
article = soup.find_all(name ="a", class_ ="storylink")
article_text = [i.getText() for i in article]
article_link = [i.get("href") for i in article]
article_upvote = [int(i.getText().split()[0]) for i in soup.find_all(name = "span",class_ = "score")]

article_max = article_upvote.index(max(article_upvote))

print(article_text[article_max])
print(article_link[article_max])
print(article_upvote[article_max])