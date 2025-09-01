from flask import Flask, render_template
import random
import datetime
import requests

app = Flask(__name__)

@app.route('/')
def home():
    date = datetime.datetime.today()
    current_year = date.year
    random_number = random.randint(1,9)
    return render_template("index.html",num = random_number, year=current_year)

@app.route("/guess/<name>")
def guess(name):
    parameters = {
        "name": name
    }
    url_age = "https://api.agify.io"
    age = requests.get(url_age,params=parameters).json()["age"]

    url_gender = "https://api.genderize.io"
    gender = requests.get(url_gender,params=parameters).json()["gender"]

    return render_template("guess.html",age= age, name= name, gender= gender)

@app.route("/blog")
def get_blog():
    blog_url = "https://api.npoint.io/f73359371b050e25467c"
    blog_post = requests.get(blog_url).json()
    return render_template("blog.html", blogs = blog_post)

if __name__ == "__main__":
    app.run(debug=True)


