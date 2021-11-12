from flask import Blueprint, render_template, request, redirect,url_for,flash
from marvel_api.models import User,db, check_password_hash
from marvel_api.forms import UserSignupForm
from marvel_api.forms import UserSigninForm
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignupForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            user_name = form.user_name.data
            email = form.email.data
            password = form.password.data
            print(email,password)

            user = User(first_name, last_name, email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {first_name} {last_name} {email}', 'user-created')

            return redirect(url_for('site.home'))

    except:
        raise Exception('Invalid Form Data: Please check your form')
    return render_template('signup.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserSigninForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            

    return render_template('signin.html')