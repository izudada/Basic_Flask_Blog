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

class RegisterForm(Form):
        name = StringField('Name', [validators.length(min=5, max=50)])
        username = StringField('Username', [validators.length(min=4, max=25)])
        email = StringField('Email', [validators.length(min=6, max=50)])
        password = PasswordField('Passowrd', [
                validators.DataRequired(),
                validators.EqualTo('confirm', message= 'Passwords do not match')
        ])
        confirm = PasswordField('Confirm Password')

@app.route("/", methods = ['GET', 'POST'])
def index():
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
                return render_template("index.html")

        return render_template("index.html", form = form)

if __name__ == '__main__':
    app.run(debug=True)