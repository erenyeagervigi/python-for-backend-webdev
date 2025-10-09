import datetime

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditior = CKEditor(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


class PostForm(FlaskForm):
    title = StringField("Blog post title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    body = CKEditorField("body", validators=[DataRequired()])
    img_url = StringField("URL of the Image", validators=[DataRequired(), URL()])
    submit = SubmitField('submit')

with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    posts = []
    data = db.session.execute(db.select(BlogPost)).scalars().all()
    for i in data:
        posts.append(i)
    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/show_post/<post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.get_or_404(BlogPost,post_id)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/new_post', methods = ['GET', 'POST'])
def add_new_post():
    new_post = PostForm()
    if request.method == "POST":
        new = BlogPost(
            title = request.form.get('title'),
            subtitle = request.form.get('subtitle'),
            author = request.form.get('author'),
            date = date.today().strftime('%B %d, %Y'),
            body = request.form.get('body'),
            img_url = request.form.get('img_url'),
        )
        db.session.add(new)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template('make-post.html', post = new_post)

# TODO: edit_post() to change an existing blog post
@app.route("/edit_post/<post_id>", methods= ['POST', 'GET'])
def edit_post(post_id):
    data = db.get_or_404(BlogPost,post_id)
    new_post = PostForm(
        title = data.title,
        subtitle = data.subtitle,
        author = data.author,
        date=date.today().strftime('%B %d, %Y'),
        body = data.body,
        img_url = data.img_url
    )
    if new_post.validate_on_submit():
            data.title = request.form.get('title')
            data.subtitle = request.form.get('subtitle')
            data.author = request.form.get('author')
            data.date = date.today().strftime('%B %d, %Y')
            data.body = request.form.get('body')
            data.img_url = request.form.get('img_url')
            db.session.commit()
            return redirect(url_for('show_post', post_id = post_id))
    return render_template('make-post.html',post = new_post, value = 'edit')
# TODO: delete_post() to remove a blog post from the database
@app.route('/delete/<post_id>', methods = ['GET', 'POST'])
def delete(post_id):
    data = db.get_or_404(BlogPost,post_id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('get_all_posts'))
# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
