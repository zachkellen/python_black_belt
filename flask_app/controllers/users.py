from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/submit', methods = ['post'])
def create_user():
    if User.validate_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }
        user_id = User.register_user(data)
        flash("Registration complete. Please login.")
        return redirect('/')
    else:
        flash("Registration Failed.")
        return redirect('/')

@app.route('/user/login', methods=['post'])
def login():
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)
    print(user_in_db)
    if not user_in_db:
        flash("Invalid Email", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db[0].password, request.form['password']):
        flash("Invalid Password.", 'login')
        return redirect('/')
    session['user_id'] = user_in_db[0].id
    session['first_name'] = user_in_db[0].first_name
    session['last_name'] = user_in_db[0].last_name
    return redirect('/paintings')

@app.route('/user/logout')
def logout():
    session.clear()
    flash("You've been logged out!", 'login')
    return redirect('/')