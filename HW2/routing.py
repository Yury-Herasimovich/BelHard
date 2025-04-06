from flask import Flask, render_template
import os
import requests
import random
from weather_scripts import *

BASE_DIR = os.path.dirname(__file__)

app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static') , 
            template_folder=os.path.join(BASE_DIR, 'templates'))

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/duck/")
def duck_page():
    response = requests.get('https://random-d.uk/api/random')
    data = response.json()
    return render_template('duck.html', 
                         image_url=data['url'],
                         image_num=data['url'].split('/')[-1].split('.')[0])
   
@app.route('/fox/')
@app.route('/fox/<int:count>/')
def fox_page(count=1):
    if count < 1 or count > 10:
        return "Error: can only request from 1 to 10 foxes", 400
    
    fox_ids = random.sample(range(1, 123), count)
    
    foxes = []
    for fox_id in fox_ids:
        foxes.append({
            'id': fox_id,
            'url': f'https://randomfox.ca/images/{fox_id}.jpg'
        })
    
    return render_template('fox.html', foxes=foxes)

@app.route('/weather-minsk/')
def weather_minsk_page():
    data = get_weather_data('Minsk')
    return render_template('weather.html', weather=data)

@app.route('/weather/<city>/')
def weather_city_page(city):
    data = get_weather_data(city)
    return render_template('weather.html', weather=data)


@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">404. Page does not exist</h1>'


app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)