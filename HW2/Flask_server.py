from flask import Flask, render_template
import os
import requests
import random
from HW2.config import Config

BASE_DIR = os.path.dirname(__file__)
API_KEY = Config.OWM_API_KEY
# API_KEY = '23232775d430e5fe2ac9a9c2cbdb8410'

app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static') , 
            template_folder=os.path.join(BASE_DIR, 'templates'))


BASE_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

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
@app.route('/fox/<int:count>')
def fox_page(count=1):
    if count < 1 or count > 10:
        return "Ошибка: можно запросить только от 1 до 10 лис", 400
    
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
    return get_weather_data("Minsk")

@app.route('/weather/<city>/')
def weather_city_page(city):
    return get_weather_data(city)

def get_weather_data(city_name):
    try:
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric'
        }

        response = requests.get(BASE_WEATHER_URL, params=params)
        response.raise_for_status()
        data = response.json()

        weather_data = {
            'city': data['name'],
            'temp': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'description': data['weather'][0]['description'].capitalize(),
            'humidity': data['main']['humidity'],
            'wind': round(data['wind']['speed'])
        }

        return render_template('weather.html', weather=weather_data)
        

    except Exception as e:
        print(f"Ошибка: {e}")
        return render_template('weather_error.html', city=city_name)




@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'


app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)