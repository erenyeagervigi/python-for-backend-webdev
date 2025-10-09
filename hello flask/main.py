from flask import Flask

app = Flask(__name__)

def make_bold(function):
    def wrapper():
        contents = function()
        return f"<b>{contents}</b>"
    return wrapper

def make_italic(function):
    def wrapper():
        contents = function()
        return f"<em>{contents}</em>"
    return wrapper

def make_background(function):
    def wrapper():
        contents = function()
        return f"<body style='background-color:black'></body>"\
                f"<h1 style='color:white'>{contents}</h1>"
    return wrapper

# def make_bold(function):
#     def wrapper():
#         return "<b>" + function() + "</b>"
#     return wrapper
#
# def make_emphasis(function):
#     def wrapper():
#         return "<em>" + function() + "</em>"
#     return wrapper
#
# def make_underlined(function):
#     def wrapper():
#         return "<u>" + function() + "</u>"
#     return wrapper


@app.route("/")
def hello_world():
    return "<h1 style='text-align:center; color:red'>Hello, eren!</h1>" \
            "<img src = 'https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3hxdnFmeHcxM2d6M2FqenBlZmF4ZWZwY2U0aTAyeWRwNHJ5bWh5ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tliXLSkzfq2C4/giphy.gif'>"\
            "<body style='background-color:black'></body>"

#router
@app.route("/bye")
@make_bold
@make_italic
@make_background
def bye():
    return "have a bad day"

#to get hold of what the user typed use <variable_name>
# to use a path u can <path:variable_name>
# to use int <int:variable name>

@app.route("/<name>")
def name(name):
    return f"hello, {name}"

if __name__ == "__main__":
    app.run(debug=True)

# to run in powershell
# (myenv) PS C:\Users\Dell\Desktop\web dev\hello flask> python main.py
# (myenv) PS C:\Users\Dell\Desktop\web dev\hello flask> flask --app main--