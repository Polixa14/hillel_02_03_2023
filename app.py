from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')


@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        error = None
        registered_emails = []
        with open('users.txt', 'rt') as usersfile:
            for line in usersfile:
                registered_emails.append(line.split(', ')[0])
        if not email:
            error = "Email is required"
        elif not password:
            error = "Password is required"
        elif password != password2:
            error = "Password doesn't match"
        elif email in registered_emails:
            return redirect(url_for('login'))
        else:
            usersfile = open('users.txt', 'at')
            usersfile.write(email + ', ' + generate_password_hash(password) + '\n')
        if error:
            flash(error)
    return render_template('register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        error = None
        user = None
        with open('users.txt', 'rt') as usersfile:
            for line in usersfile:
                if line.split(', ')[0] == email:
                    user = {'email': email,
                            'password': line.rstrip().split(', ')[1]
                            }
        if user is None:
            error = 'Incorrect email'
        elif not check_password_hash(user.get('password'), password):
            error = 'Incorrect password'
        if error is None:
            return redirect(url_for('index'))
        else:
            flash(error)
    return render_template('login.html')
