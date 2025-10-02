from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///manhwa.db"
app.secret_key = 'eren'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Manhwa(db.Model):
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    title:Mapped[str] = mapped_column(String,nullable=False, unique=True)
    year:Mapped[int] = mapped_column(Integer,nullable=False)
    description:Mapped[str] = mapped_column(String,nullable=False)
    rating:Mapped[float] = mapped_column(Float,nullable=True)
    review:Mapped[str] = mapped_column(String,nullable=True)
    ranking: Mapped[int] = mapped_column(Integer,nullable=True)
    img_url: Mapped[str] = mapped_column(String,nullable=False)

class Myform(FlaskForm):
    rating = StringField('your rating', validators=[DataRequired()])
    review = StringField('review', validators=[DataRequired()])
    sumbit = SubmitField('done')

class Addform(FlaskForm):
    title = StringField('Manhwa Title', validators=[DataRequired()])
    done = SubmitField(label='Add')

with app.app_context():
    db.create_all()

    # new = Manhwa(
    #     title = 'My Bias Gets on the Last Train',
    #     description = 'Every night, Yeo-Un takes the last train home—same route, same time, same routine. But one thing keeps catching his eye: a girl with a guitar and a presence that lingers in his mind. When a shared love for the indie band Long Afternoon sparks a conversation, their late-night encounters begin to turn into something more. But Hae-In isn’t just another fan—she’s the voice behind the band, a secret she can’t afford to reveal. As music draws them closer, the truth may threaten to pull them apart. When the final note plays, will their story end in harmony… or heartbreak?',
    #     year = '2024',
    #     img_url = 'https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx187944-bb9vk8N7NcDC.jpg',
    #     rating = 8.5
    # )
    # db.session.add(new)
    # db.session.commit()

def add_manhwa(name):
    url = "https://graphql.anilist.co"

    query = """
    query ($search: String) {
      Media(search: $search, type: MANGA) {
        id
        title {
          english
        }
        description(asHtml: false)
        startDate {
          year
        }
        coverImage {
          extraLarge
          large
          medium
        }
      }
    }
    """

    variables = {"search": name}

    try:
        response = requests.post(url, json={"query": query, "variables": variables})
        response.raise_for_status()  # check for HTTP errors
        json_data = response.json()

        # If Media is None → not found
        media = json_data.get("data", {}).get("Media")
        if not media:
            return None

        return {
            'title': media['title'] or {"english": name},
            'description': (media['description'] or "No description available.").split("<br>")[0],
            'year': media['startDate']['year'] if media['startDate'] else "Unknown",
            'img_url': media['coverImage']['extraLarge'] if media['coverImage'] else ""
        }

    except Exception as e:
        print("AniList error:", e)
        return None



@app.route("/")
def home():
    manhwa = db.session.execute(db.select(Manhwa).order_by(Manhwa.rating.desc())).scalars().all()
    for i, movie in enumerate(manhwa, start=1):
        movie.ranking = i
    db.session.commit()
    return render_template("index.html", data = manhwa)

@app.route('/add', methods=['POST', 'GET'])
def add():
    form = Addform()
    if request.method == 'POST':
        name = request.form.get('title')
        manhwa = add_manhwa(name)

        if not manhwa:
            return "❌ Manhwa not found. Try again.", 404

        title = manhwa['title'].get('english') or name
        description = manhwa['description']
        year = manhwa['year']
        img_url = manhwa['img_url']

        new_manwa = Manhwa(
            title=title,
            description=description,
            year=year,
            img_url=img_url,
            rating=7,
            review='review it'
        )
        db.session.add(new_manwa)
        db.session.commit()
        return redirect(url_for('edit'))
    return render_template('add.html', form=form)


@app.route('/update', methods= ['GET','POST'])
def update():
    form = Myform()
    id = request.args.get('id')
    edit_manhwa = db.get_or_404(Manhwa,id)
    if request.method == "POST":
        rating = request.form.get('rating')
        review = request.form.get('review')
        edit_manhwa.rating = float(rating)
        edit_manhwa.review = review
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form = form)

@app.route('/delete',methods = ['GET','post'])
def delete():
    id = request.args.get('id')
    delete_manhwa = db.get_or_404(Manhwa,id)
    db.session.delete(delete_manhwa)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
