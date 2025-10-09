import flask
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Select
import random as r
app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def get_dict(self):
        # dictionary = {}
        # for i in self.__table__.columns:
        #     dictionary[i.name] = getattr(self,i.name)
        # return dictionary
        dictionary = {i.name: getattr(self,i.name) for i in self.__table__.columns}
        return dictionary



with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/random", methods = ['GET'])
# def get_random_cafe():
#     return None

# HTTP GET - Read Record
@app.route('/random')
def random():
    # get_random_cafe()
    data = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = r.choice(data)
    # return flask.jsonify(
    #     name = random_cafe.name,
    #     map_url = random_cafe.map_url,
    #     img_url = random_cafe.img_url,
    #     location = random_cafe.location,
    #     seats = random_cafe.seats,
    #     coffee_price = random_cafe.coffee_price,
    #     can_take_calls = random_cafe.can_take_calls,
    #     has_sockets = random_cafe.has_sockets,
    #     has_toilet = random_cafe.has_toilet,
    #     has_wifi = random_cafe.has_wifi,
    #
    # )
    return flask.jsonify(random_cafe.get_dict())

@app.route("/all")
def all_cafe():
    data = db.session.execute(db.select(Cafe)).scalars()
    return flask.jsonify( cafe = [i.get_dict() for i in data])

@app.route("/search")
def search():
    value = request.args.get('loc')
    cafe_data = Select(Cafe).where(Cafe.location == value)
    data = db.session.execute(cafe_data).scalars().all()
    if not data:
        return flask.jsonify(erros ={"not found": "Sorry, we dont have a cafe at that location"})
    return flask.jsonify(cafe = [i.get_dict() for i in data])

# HTTP POST - Create Record
@app.route("/add", methods = ['POST'])
def add():
    name = request.form.get('name')
    map_url = request.form.get('map_url')
    img_url = request.form.get('img_url')
    location = request.form.get('location')
    seats = request.form.get('seats')
    has_toilet = bool(request.form.get('has_toilet'))
    has_wifi = bool(request.form.get('has_wifi'))
    has_sockets = bool(request.form.get('has_sockets'))
    can_take_calls = bool(request.form.get('can_take_calls'))
    coffee_price = request.form.get('coffee_price')
    add_cafe = Cafe(
        name = name,
        map_url = map_url,
        img_url = img_url,
        location = location,
        seats = seats,
        has_toilet = has_toilet,
        has_wifi = has_wifi,
        has_sockets = has_sockets,
        can_take_calls = can_take_calls,
        coffee_price = coffee_price
    )
    db.session.add(add_cafe)
    db.session.commit()
    return flask.jsonify(response = {"success": "Successfully added this cafe"})

# HTTP PUT/PATCH - Update Record
@app.route("/update_price/<int:n>", methods = ['PATCH'])
def update_price(n):
    update_coffee_price = request.args.get('new_price')
    try:
        data = db.get_or_404(Cafe,n)
    except AttributeError:
        return flask.jsonify(error={"Not found": "Invalid id"})
    else:
        data.coffee_price = update_coffee_price
        db.session.commit()
        return flask.jsonify(success="Successfully updated the price")


# HTTP DELETE - Delete Record
@app.route('/report-closed/<int:n>', methods = ['POST'])
def report_closed(n):
    api_key = request.args.get('api_key')
    if api_key == 'Topsecretkey':
        try:
            data = db.get_or_404(Cafe,n)
        except AttributeError:
            return flask.jsonify(error={"Not found": "Invalid id"})
        else:

            db.session.delete(data)
            db.session.commit()
            return flask.jsonify(success="Successfully deleted the price")
    else:
        return flask.jsonify(invalid = 'invalid api key')

if __name__ == '__main__':
    app.run(debug=True)
