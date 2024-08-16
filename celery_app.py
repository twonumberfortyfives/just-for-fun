import time
from celery import Celery
from celery.signals import task_prerun, task_postrun

app = Celery('weather_processor', broker='redis://redis:6379', backend='redis://redis:6379')

task_durations = []
start_time = None
number_of_task = 0


@task_prerun.connect
def task_start_handler(sender=None, task_id=None, task=None, **kwargs):
    global start_time
    if start_time is None:
        start_time = time.time()
    task.start_time = time.time()


@task_postrun.connect
def task_end_handler(sender=None, task_id=None, task=None, **kwargs):
    global number_of_task
    duration = time.time() - task.start_time
    task_durations.append(duration)
    number_of_task += 1
    print(f"Task {task.name} completed in {duration:.2f} seconds")


@app.task
def process_weather_data(temperature, humidity, wind_speed):
    print(f"Received Measurements - Temperature: {temperature}, Humidity: {humidity}, Wind Speed: {wind_speed}")


@app.task
def average_result():
    global start_time
    if start_time is None:
        print("No tasks have been started yet.")
        return

    total_time = time.time() - start_time
    if total_time > 0:
        throughput = number_of_task / total_time
        print(f"Executed {number_of_task} tasks. Throughput: {throughput:.2f} tasks per second.")
    else:
        print("Time tracking issue. No throughput available.")
