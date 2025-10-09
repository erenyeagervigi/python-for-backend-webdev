import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv("important.env")
CLIENT_ID = os.getenv("client_id")
CLIENT_SECRECT = os.getenv("client_secret")

#--------------------------------------------web scraping--------------------------------------------------
user_input = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = user_input.split("-")[0]
URL = "https://www.billboard.com/charts/hot-100/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0"}

response = requests.get(f"{URL}{user_input}", headers = headers)
data = response.text
soup = BeautifulSoup(data, "html.parser")

music_title = [i.getText().strip() for i in soup.select("li ul li h3")]
if not music_title:
        print("sorry it doesn't exist")
        exit()

#-------------------------------------------------------searching songs in spotify---------------------------------------------------------------
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRECT,scope="playlist-modify-private",redirect_uri="https://www.billboard.com/charts/hot-100/", show_dialog=True,
        cache_path="token.txt"))
user_id = sp.current_user()["id"]

song_uri = []

for song in music_title:
        result = sp.search(q=f"track:{song} year:{year}",type='track')
        try:
                uri = result["tracks"]["items"][0]["uri"]
                song_uri.append(uri)
        except IndexError:
                print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user = user_id, name=f"Top 100 billboard from {user_input}", public=False)
playlist_id = playlist["id"]
sp.playlist_add_items(playlist_id,song_uri)