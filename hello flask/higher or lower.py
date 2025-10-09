from flask import Flask
import random

random_number = random.randint(1,8)
print(random_number)
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Guess a random number between 1 to 9</h1>"\
            "<img src = 'https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcGxlN2xwNTU2eWprd3JiczdmejJ3emZvcGx3NmRmZHZycWMzZGl1NSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7aCSPqXE5C6T8tBC/giphy.gif'>"

@app.route("/<int:num>")
def guess(num):
    if random_number == num:
        return "<h1>its equal</h1>"\
                "<img src = 'https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'>"
    if random_number < num:
        return "<h1>its low</h1>"\
                "<img src = 'https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'>"
    return "<h1>its high</h1>"\
            "<img src = 'https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'>"


if __name__ == "__main__":
    app.run(debug=True)