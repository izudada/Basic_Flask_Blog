from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)

# Registration FOrm Class
class RegisterForm(Form):
        name = StringField('Name', [validators.length(min=5, max=50)])
        username = StringField('Username', [validators.length(min=4, max=25)])
        email = StringField('Email', [validators.length(min=6, max=50)])
        password = PasswordField('Passowrd', [
                validators.DataRequired(),
                validators.EqualTo('confirm', message= 'Passwords do not match')
        ])
        confirm = PasswordField('Confirm Password')

# Index/Home Page
@app.route("/", methods = ['GET', 'POST'])
def index():
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
                name = form.name.data
                email = form.email.data
                username = form.username.data
                password = sha256_crypt.encrypt(str(form.password.data))

                # Create Cursor
                cur = mysql.connection.cursor()

                # Execute Query
                cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

                # Commit To DB
                mysql.connection.commit()

                # Close Connection
                cur.close()

                flash('You are now registered, Try logging in', 'success')

                return redirect(url_for('login'))

        return render_template("index.html", form = form)


# Login
@app.route("/login", methods = ['GET', 'POST'])
def login():
        
        if request.method == 'POST':

                # Get Form Fields
                email = request.form['email']
                password_candidate = request.form['password']

                # Create Cursor
                cur = mysql.connection.cursor()

                # Get user by email
                result = cur.execute("SELECT * FROM users WHERE email = %s", [email])

                if result > 0:
                        #Get stored hash
                        data = cur.fetchone()
                        password = data['password']

                        # Compare passwords
                        if sha256_crypt.verify(password_candidate, password):
                                # Passed
                                session['logged_in'] = True
                                session['email'] = email

                                flash('You are now logged in', 'success')
                                return redirect(url_for('dashboard'))
                        else:
                                error = 'Invalid login'
                                return render_template("login.html", error = error)
                        # Close Connection
                        cur.close()
                else:
                        error = 'Username not Found'
                        return render_template("login.html", error = error)

        return render_template("login.html")


# Logout
@app.route("/logout")
def logout():
        session.clear()
        flash('You have succesfully logged out', 'success')
        return redirect(url_for('login'))

# Dashboard
@app.route("/dashboard")
def dashboard():
        return render_template("dashboard.html")

if __name__ == '__main__':
        app.secret_key = 'secret123'
        app.run(debug=True)