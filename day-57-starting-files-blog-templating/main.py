from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    anime_blog = requests.get("https://api.npoint.io/f73359371b050e25467c").json()
    return render_template("index.html",blogs = anime_blog)


@app.route("/read/<int:id>")
def get_post(id):
    print(id)
    anime_blog = requests.get("https://api.npoint.io/f73359371b050e25467c").json()
    return render_template("post.html", blogs = anime_blog, num = id)


if __name__ == "__main__":
    app.run(debug=True)
