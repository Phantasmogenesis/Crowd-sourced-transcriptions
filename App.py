from flask import Flask, render_template, url_for, session, request, redirect
import flask_login

from home import home
from transcribe import transcribe
from review import review
from librarian import librarian


app = Flask(__name__)

app.secret_key = '65a37542223cc0de46794d1d4970e060a06853824367f9a28539cc35b3261013'


login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# username : password
users = {'teamA': {'psw': 'secret'}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(uname):
    if uname not in users:
        return

    user = User()
    user.id = uname
    return user


@login_manager.request_loader
def request_loader(request):
    uname = request.form.get('uname')
    if uname not in users:
        return

    user = User()
    user.id = uname
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    uname = request.form['uname']
    if request.form['psw'] == users[uname]['psw']:
        user = User()
        user.id = uname
        flask_login.login_user(user)
        return redirect(url_for('librarian.librarian_page'))

    return 'Bad login, please refresh to try again.'


app.register_blueprint(librarian)

app.register_blueprint(home)

app.register_blueprint(transcribe)

app.register_blueprint(review)

@app.route('/tutorial', methods=['GET', 'POST'])
def tutorial():
    if request.method == 'GET':
        return render_template('tutorial.html')