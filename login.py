from flask import Blueprint, render_template, request, redirect
import flask_login

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




login = Blueprint("login", __name__)

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