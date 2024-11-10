import json
import random
import paho.mqtt.client as mqtt

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

try:
    mqttc.connect("emqx1", 1883, 60)
except ConnectionRefusedError:
    print("Connecting to MQTT broker...")

mqttc.loop_start()


def publish_weather_data():
    for _ in range(10):
        weather_data = {
            "temperature": random.randint(0, 50),
            "humidity": random.randint(0, 50),
            "wind_speed": random.randint(0, 50),
        }

        try:
            msg_info = mqttc.publish("weather", json.dumps(weather_data), qos=1)
        except RuntimeError:
            print("Publish failed")


publish_weather_data()

mqttc.disconnect()
mqttc.loop_stop()
