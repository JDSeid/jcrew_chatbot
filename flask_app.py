# from chatbot import qa
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    # return "<h1> Hi <h1>"
    return render_template('home.html')


@app.route("/otherpage")
def other():
    return "info for other page"
