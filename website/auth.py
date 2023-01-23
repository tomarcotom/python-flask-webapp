from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db

auth = Blueprint('auth', __name__)

def validate_login(password1, password2):
  # add validations that you want 
  return password1 == password2

def create_user(email, firstName, password):
  new_user = User(email=email, first_name=firstName, password=generate_password_hash(password, method='sha256'))
  if not db.session.query(User).filter(User.email == email).first():
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user , remember=True)
  else:
    flash('Username already exists', category='error')

  return redirect(url_for('views.home'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    existing_user = db.session.query(User) \
                    .filter(User.email == email).first()

    if existing_user and check_password_hash(existing_user.password, password):
      flash('Logged in', category='success')
      login_user(existing_user, remember=True)
      return redirect(url_for('views.home'))
    else:
      flash('Wrong credentials', category='error')

  return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required #run this function only when the user is logged in 
def logout():
  logout_user()

  return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    email = request.form.get('email')
    firstName = request.form.get('firstName')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    if email and firstName and password1 and password2 and validate_login(password1, password2):
      create_user(email, firstName, password1)
    else:
      flash('passwords are not the same!', category='error')

  return render_template("signup.html", user=current_user)
