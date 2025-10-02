from flask import Flask, render_template, request
import requests
# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)

done = []

@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact",methods=['GET','post'])
def contact():
    if request.method == 'GET':
        return render_template("contact.html", done = done)
    else:
        return form_entry()


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/form-entry", methods= ['post'])
def form_entry():
    print(request.form['name'])
    print(request.form['email'])
    print(request.form['phone'])
    print(request.form['message'])
    done.append("yes")
    return render_template("contact.html", done = done)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
