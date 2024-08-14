from celery.app import Celery

app = Celery('weather_processor', broker='redis://redis:6379', backend='redis://redis:6379')


@app.task
def process_weather_data(temperature, humidity, wind_speed):
    # Print the received measurements (this is the "processing")
    print(f"Received Measurements - Temperature: {temperature}, Humidity: {humidity}, Wind Speed: {wind_speed}")
