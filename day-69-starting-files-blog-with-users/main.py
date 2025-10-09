from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
# Import your forms from the forms.py
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

gravatar = Gravatar(app,
                    size=100,                # Size of the avatar (in px)
                    rating='g',              # Allowed rating ('g', 'pg', 'r', 'x')
                    default='retro',         # Default image if no Gravatar is found
                    force_default=False,
                    use_ssl=True,            # Use HTTPS
                    base_url=None)

# TODO: Configure Flask-Login


# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

# CONFIGURE TABLES
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)

    # A user can have many blog posts and many comments
    posts = relationship('BlogPost', back_populates='author')
    comments = relationship('Comment', back_populates='author')  # ✅ fixed


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    # One author can have many blog posts
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='posts')

    post_comment = relationship('Comment', back_populates='commented')

class Comment(db.Model):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    # One comment belongs to one user (the author)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    author = relationship('User', back_populates='comments')  # ✅ renamed for clarity

    post_comment_id: Mapped[int] = mapped_column(Integer, ForeignKey('blog_posts.id'))
    commented = relationship('BlogPost', back_populates='post_comment')

with app.app_context():
    db.create_all()

def admin_only(fuc):
    @wraps(fuc)
    def wrapper(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return fuc(*args,**kwargs)
    return wrapper


# TODO: Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register', methods = ['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        name = request.form.get('name')
        email = request.form.get('email')
        password = generate_password_hash(salt_length=8, password=request.form.get('password'), method = 'pbkdf2')

        data = db.session.execute(db.select(User).where(User.email == email)).scalars().first()
        if data:
            flash('The email already exists')
            return redirect(url_for('register'))

        new_user = User(
            name = name,
            email = email,
            password = password,
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        print('successfully registered')
        return redirect(url_for('get_all_posts'))
    return render_template("register.html", form = register_form)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User,user_id)

# TODO: Retrieve a user from the database based on their email.
@app.route('/login', methods = ['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        data = db.session.execute(db.select(User).where(User.email == email)).scalars().first()

        if data is None:
            flash('This email does not exists')
            return redirect(url_for('login'))

        check_password = check_password_hash(pwhash=data.password,password= password)
        if check_password:
            login_user(data)
            return redirect(url_for('get_all_posts'))
        else:
            flash('Invalid password')
            return redirect(url_for('login'))
    return render_template("login.html", form = login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/', methods = ['GET'])
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts, logged_in = current_user.is_authenticated)


# TODO: Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods = ['POST', 'GET'])
def show_post(post_id):
    form = CommentForm()
    requested_post = db.get_or_404(BlogPost, post_id)
    commented_post = db.session.execute(db.select(Comment)).scalars()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            text = request.form.get('comment')
            requested_post = db.get_or_404(BlogPost, post_id)

            new_comment = Comment(
                text = text,
                author = current_user,
                commented = requested_post,
            )

            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('show_post', post_id = post_id))
        else:
            flash("you must be logged in to comment")
            return redirect(url_for('register'))
    return render_template("post.html", post=requested_post, form = form, logged_in = current_user.is_authenticated, comments = commented_post, gravatar = gravatar)


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, logged_in = current_user.is_authenticated)


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True, logged_in = current_user.is_authenticated)


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
