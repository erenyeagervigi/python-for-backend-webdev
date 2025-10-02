from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms import validators
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.secret_key = 'eren'
bootstrap = Bootstrap5(app)



class MyForm(FlaskForm):
    email = StringField(label='email', validators=[DataRequired(), Email("invalid email")])
    password = PasswordField(label='password', validators=[DataRequired(), validators.Length(min=8, max=20, message="it is short")])
    submit = SubmitField(label="log in")

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET","POST"])
def login():
    login_form = MyForm()
    if login_form.validate_on_submit():
        print(login_form.email.data)
        if login_form.email.data == "admin@gmail.com" and login_form.password.data == '12345678':
            return render_template('success.html')
        else:
            return render_template('denied.html')
    return render_template('login.html', form = login_form)


if __name__ == '__main__':
    app.run(debug=True)
