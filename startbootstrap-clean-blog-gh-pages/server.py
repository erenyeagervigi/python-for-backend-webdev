from flask import Flask, render_template
import requests
from post import Post

response = requests.get("https://api.npoint.io/f73359371b050e25467c").json()
post_obj = []
for data in response:
    post = Post(title=data['title'],body=data['body'],subtitle=data['subtitle'],id=data['id'])
    post_obj.append(post)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", post = post_obj)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/post/<int:id>')
def post(id):
    requested_post = None
    for i in post_obj:
        if i.id == id:
            requested_post = i

    return render_template('post.html', post = requested_post)

if __name__ == "__main__":

    app.run(host='0.0.0.0',debug=True)
