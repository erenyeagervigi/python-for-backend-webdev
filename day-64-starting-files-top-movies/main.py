import os
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from dotenv import load_dotenv

load_dotenv('secrets.env')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.secret_key = 'eren'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)
# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250),unique=True,nullable=False)
    year:Mapped[int] = mapped_column(Integer,nullable=False)
    description:Mapped[str]=mapped_column(String,nullable=False)
    rating:Mapped[float]=mapped_column(Float,nullable=True)
    ranking:Mapped[int] = mapped_column(Integer, nullable=True)
    review:Mapped[str]=mapped_column(String, nullable=True)
    img_url:Mapped[str]=mapped_column(String,nullable=False)

with app.app_context():
    db.create_all()

class Editform(FlaskForm):
    rating = StringField('Your rating out of 10', validators=[DataRequired()])
    review = StringField('Your review',validators=[DataRequired()])
    done = SubmitField(label='done')

class Addform(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    done = SubmitField(label='Add moive')

@app.route("/")
def home():
    movies_data = db.session.execute(db.select(Movie).order_by(Movie.rating.desc())).scalars().all()
    for i, movie in enumerate(movies_data, start=1):
        movie.ranking = i
    db.session.commit()
    return render_template("index.html", data = movies_data)

@app.route('/delete')
def delete():
    movie_id = request.args.get('id')
    delete_movie = db.get_or_404(Movie,movie_id)
    db.session.delete(delete_movie)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/edit", methods = ['POST','GET'])
def edit():
    form = Editform()
    movie_id = request.args.get('id')
    edit_movie = db.get_or_404(Movie,movie_id)
    if request.method == "POST":
        rating = request.form.get('rating')
        review = request.form.get('review')
        edit_movie.rating = float(rating)
        edit_movie.review = review
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html',movie = edit_movie, form = form)

api_key = os.getenv('api_key')
api_token = os.getenv('api_token')

url = "https://api.themoviedb.org/3/search/movie"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_token}"
}


@app.route("/add", methods = ['GET', 'POST'])
def add():
    form = Addform()

    if request.method == 'POST':
        title = request.form['title']
        parameters = {
            "query": title,
        }
        response = requests.get(url, params=parameters, headers=headers).json()
        movie_data =response['results']
        return render_template('select.html', data = movie_data)
    return render_template('add.html', form = form)

@app.route('/update', methods = ['GET','POST'])
def update():
    id = request.args.get('id')
    url_update = f"https://api.themoviedb.org/3/movie/{id}"
    parameters = {
        'movie_id':{id}
    }
    response = requests.get(url_update, params=parameters, headers=headers).json()
    img_url = f"https://image.tmdb.org/t/p/w500/{response['poster_path']}"
    title = response['title']
    year = response['release_date'].split("-")[0]
    description = response['overview']
    rating = response['vote_average']

    new_data = Movie(title= title,rating=rating,img_url=img_url,year=year,description=description)
    db.session.add(new_data)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
