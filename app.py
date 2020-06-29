from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'localhost'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)

Articles = Articles()

@app.route("/")
def index():
        return render_template("home.html")

# @app.route("/articles")
# def articles():
#         return render_template("articles.html", articles = Articles)

# @app.route("/article/<string:id>/")
# def article(id):
#         return render_template("article.html", id = id)

if __name__ == '__main__':
    app.run(debug=True)