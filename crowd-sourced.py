# google drive api imports
# from __future__ import print_function
# import os.path
# from googleapiclient.discovery import build
# from google.oauth2 import service_account
# flask imports
from flask import Flask, render_template, url_for, session, request, redirect
# blueprint imports
# from flask.ext.login import LoginManager


from home import home
# from transcribe import transcribe
from review import review




app = Flask(__name__)

# x = "1"

# app.secret_key = '65a37542223cc0de46794d1d4970e060a06853824367f9a28539cc35b3261013'


# login_manager = LoginManager()

# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

# class User:
#     def 




# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # Here we use a class of some kind to represent and validate our
#     # client-side form data. For example, WTForms is a library that will
#     # handle this for us, and we use a custom LoginForm to validate.
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Login and validate the user.
#         # user should be an instance of your `User` class
#         login_user(user)

#         flask.flash('Logged in successfully.')

#         next = flask.request.args.get('next')
#         # is_safe_url should check if the url is safe for redirects.
#         # See http://flask.pocoo.org/snippets/62/ for an example.
#         if not is_safe_url(next):
#             return flask.abort(400)

#         return flask.redirect(next or flask.url_for('index'))
#     return flask.render_template('login.html', form=form)

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect('\home')
            # return("1")
    return render_template('login.html', error=error)
    # return(error)




app.register_blueprint(home)

@app.route("/transcribe")
def transcribe_page():
    return "<h1>transcribe!</h1>"



app.register_blueprint(review)

# @app.route("/review")
# def review_page():
#     return "<h1>review!</h1>"

