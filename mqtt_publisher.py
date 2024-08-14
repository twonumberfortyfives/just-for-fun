import json
import random
import time
import paho.mqtt.client as mqtt


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

mqttc.username_pw_set("publisher", "251104makS")
mqttc.connect("emqx1", 1883, 60)
mqttc.loop_start()


def publish_weather_data():

    weather_data = {
        "temperature": random.randint(0, 50),
        "humidity": random.randint(0, 50),
        "wind_speed": random.randint(0, 50)
    }

    start = time.time()

    for i in range(5):
        msg_info = mqttc.publish("weather", json.dumps(weather_data), qos=1)
        msg_info.wait_for_publish()

    end = time.time()
    print(end - start)


publish_weather_data()

mqttc.disconnect()
mqttc.loop_stop()
