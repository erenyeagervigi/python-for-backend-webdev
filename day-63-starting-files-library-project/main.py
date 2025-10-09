from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import os


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books_collection.db"

db.init_app(app)

class Book(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)


@app.route('/')
def home():
    if not os.path.exists('books_collection.db'):
        db.create_all()

    book_data = db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()
    return render_template('index.html', books = book_data)


@app.route("/add", methods=['GET','POST'])
def add():
    if request.method == 'POST':
        book = Book(
            title = request.form['book_name'],
            author = request.form['book_name'],
            rating = request.form['rating']
        )
        db.session.add(book)
        db.session.commit()
    return render_template('add.html')

@app.route('/edit', methods=['GET','Post'])
def edit():
    id = request.args.get('id')
    if request.method == "POST":
        new_rating = request.form['change rating']
        update_new_rating = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
        update_new_rating.rating = int(new_rating)
        db.session.commit()
        return home()

    book_data = db.session.execute(db.select(Book).order_by(Book.id == id)).scalar()
    return render_template('edit.html', data = book_data)

@app.route('/<int:id>', methods = ['POST','GET'])
def delete(id):
        print(id)
        book_to_delete = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
        db.session.delete(book_to_delete)
        db.session.commit()
        return home()


if __name__ == "__main__":
    app.run(debug=True)

