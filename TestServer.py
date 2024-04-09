from flask import Flask, render_template, url_for, request
from weather import getCurrentWeather
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def getWeather():
    city = request.args.get('city')
    weatherData = getCurrentWeather(city)
    return render_template("weather.html", city=city, weatherData=weatherData)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)