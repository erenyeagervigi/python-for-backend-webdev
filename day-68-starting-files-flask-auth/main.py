from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, select
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

# CREATE TABLE IN DB

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html", logged_in = current_user.is_authenticated)


@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = generate_password_hash(password=request.form.get('password'), method='pbkdf2', salt_length=8)
        name = request.form.get('name')

        data = db.session.execute( select(User).where(User.email == email)).scalars().first()
        if data:
            flash('Email already exists, Please try with a different email')
            return redirect(url_for('register'))

        new_data = User(
            email = email,
            password = password,
            name = name,
        )
        db.session.add(new_data)
        db.session.commit()

        login_user(new_data)
        print('successfully registered')
        return redirect(url_for('secrets'))
    return render_template("register.html")


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User,user_id)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        data = db.session.execute( select(User).where(User.email == email)).scalars().first()
        if data is None:
            flash('The email does not exists, Please try again ')
            return redirect(url_for('login'))
        else:
            password_check = check_password_hash(pwhash=data.password, password=password)
            if password_check:
                login_user(data)
                return redirect(url_for('secrets'))
            else:
                flash('Invalid password')
                return redirect(url_for('login'))
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    user = current_user.name
    print(user)
    return render_template("secrets.html", name= user, logged_in = current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download', methods = ['GET', 'POST'])
def download():
    return send_from_directory('static', path = 'files/cheat_sheet.pdf')


if __name__ == "__main__":
    app.run(debug=True)
