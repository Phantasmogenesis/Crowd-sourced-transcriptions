# google drive api imports
# from __future__ import print_function
# import os.path
# from googleapiclient.discovery import build
# from google.oauth2 import service_account
# flask imports
from flask import Flask, render_template, url_for, session, request, redirect
import flask_login
# blueprint imports
# from flask.ext.login import LoginManager


from home import home
# from transcribe import transcribe
from review import review




app = Flask(__name__)

# x = "1"

app.secret_key = '65a37542223cc0de46794d1d4970e060a06853824367f9a28539cc35b3261013'






login_manager = flask_login.LoginManager()

login_manager.init_app(app)


users = {'adombros': {'password': 'secret'}}



class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = request.form['email']
    if request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('admin'))

    return 'Bad login'


@app.route('/admin')
@flask_login.login_required
def admin():
    return 'Logged in as: ' + flask_login.current_user.id









app.register_blueprint(home)

@app.route("/transcribe")
def transcribe_page():
    return "<h1>transcribe!</h1>"



app.register_blueprint(review)

# @app.route("/review")
# def review_page():
#     return "<h1>review!</h1>"




# TODO: review folder no larger than 30 files, take files from overflow and move to pending as needed