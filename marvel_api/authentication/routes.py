from flask import Blueprint, render_template, request, redirect,url_for,flash
from marvel_api.models import User,db, check_password_hash
from marvel_api.forms import UserSignupForm, UserSigninForm
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignupForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            user_name = form.user_name.data
            password = form.password.data


            user = User(first_name, last_name, email, user_name, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {user_name}', 'user-created')

            return redirect(url_for('site.home'))

    except:
        raise Exception('Invalid Form Data: Please check your form')
    return render_template('signup.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserSigninForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            user_name = form.user_name.data
            password = form.password.data
            print(user_name,password)

            logged_user = User.query.filter(User.user_name == user_name).first() # Not super confident about this line.
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in: Via username/password', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Your username/password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid form data: please check your form')
    return render_template('signin.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))