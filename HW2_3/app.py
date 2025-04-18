import os
import re
import requests
from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from pydantic import ValidationError
from pydantic_schemas import UserRegister, UserLogin
from config import Config
from weather_scripts import *
from models import User, db

BASE_DIR = os.path.dirname(__file__)

app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static') , 
            template_folder=os.path.join(BASE_DIR, 'templates'))

app.config['SECRET_KEY'] = "my secret key - ds;ldks;ldks;ldks"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.db"

db.init_app(app)

def get_user_by_login(login: str) -> User:
    return User.query.filter_by(login=login).first()

def create_user(user_data: UserRegister) -> User:
    hashed_password = generate_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        login=user_data.login,
        email=user_data.email,
        password=hashed_password,  # Захэшировал встроенными функциями werkzeug
        age=user_data.age
    )
    db.session.add(user)
    db.session.commit()
    return user

@app.route('/register/', methods=['GET', 'POST'])
def register():
    errors = []
    if request.method == 'POST':
        try:
            user_data = UserRegister(
                username=request.form['username'],
                login=request.form['login'],
                email=request.form['email'],
                password=request.form['password'],
                age=int(request.form['age'])
            )
            user = create_user(user_data)
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Register successfull!', 'success')
            return redirect(url_for('index'))
        except ValidationError as e:
            errors = [err['msg'] for err in e.errors()]
        except Exception as e:
            flash(str(e), 'error')
    
    return render_template('register.html', errors = errors, form_data = request.form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    errors = []
    if request.method == 'POST':
        try:
            login_data = UserLogin(
                login=request.form['login'],
                password=request.form['password']
            )
            user = get_user_by_login(login_data.login)
            print(f"User found: {user}")
            if user:
                print(f"Password match: {check_password_hash(user.password, login_data.password)}")
            if not user or not check_password_hash(user.password, login_data.password):
                errors.append('Wrong login or password')
            else:
                session['user_id'] = user.id
                session['username'] = user.username
                flash('Entry successfull!', 'success')
                return redirect(url_for('index'))
        except ValidationError as e:
            errors = [err['msg'] for err in e.errors()]
        except Exception as e:
            flash(str(e), 'error')
    
    return render_template('login.html', errors=errors, form_data=request.form)

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/duck/")
def duck_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    response = requests.get('https://random-d.uk/api/random')
    data = response.json()
    return render_template('duck.html', 
                         image_url=data['url'],
                         image_num=data['url'].split('/')[-1].split('.')[0])
   
@app.route('/fox/')
@app.route('/fox/<int:count>/')
def fox_page(count=1):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if count < 1 or count > 10:
        return "Error: can only request from 1 to 10 foxes", 400
    
    foxes = []
    for i in range(count):
            res = requests.get('https://randomfox.ca/floof/').json()
            foxes.append(res['image'])

    # fox_ids = random.sample(range(1, 123), count)
    # for fox_id in fox_ids:
    #     foxes.append({
    #         'id': fox_id,
    #         'url': f'https://randomfox.ca/images/{fox_id}.jpg'
    #     })
    
    return render_template('fox.html', foxes=foxes)

@app.route('/weather-minsk/')
def weather_minsk_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    data = get_weather_data('Minsk')
    return render_template('weather.html', weather=data)

@app.route('/weather/<city>/')
def weather_city_page(city):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    data = get_weather_data(city)
    return render_template('weather.html', weather=data)


@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">404. Page does not exist</h1>'


# app.run(debug=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)