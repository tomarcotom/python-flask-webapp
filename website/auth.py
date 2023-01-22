from flask import Blueprint, render_template, request, flash

def validate_login(password1, password2):
  # add validations that you want 
  return password1 == password2

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  data = request.form
  print('asadasda')
  print(data)
  return render_template("login.html")

@auth.route('/logout')
def logout():
  return render_template("logout.html")

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    email = request.form.get('email')
    firstName = request.form.get('firstName')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    if validate_login(password1, password2):
      flash('Good!', category='success')
    else:
      flash('passwords are not the same!', category='error')


  return render_template("signup.html")
