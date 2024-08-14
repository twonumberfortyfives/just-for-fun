import json
from time import sleep

from celery_app import process_weather_data

import paho.mqtt.client as mqtt


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    if reason_code_list[0].is_failure:
        print(f"Broker rejected your subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")


def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        print("Unsubscribe succeeded (if SUBACK is received in MQTTv3 it succeeds)")
    else:
        print(f"Broker replied with failure: {reason_code_list[0]}")
    client.disconnect()


def on_message(client, userdata, message):
    try:
        json_str = message.payload.decode('utf-8')
        weather_data = json.loads(json_str)
        # Send the data to the Celery worker
        process_weather_data.delay(
            temperature=weather_data['temperature'],
            humidity=weather_data['humidity'],
            wind_speed=weather_data['wind_speed']
        )
    except json.JSONDecodeError:
        print("Received message is not in JSON format")
    except KeyError as e:
        print(f"Missing key in received data: {e}")


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        client.subscribe("weather")  # Subscribe to the 'weather' topic


# MQTT client setup
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Set username and password for the broker
mqttc.username_pw_set(username="subscriber", password="251104makS")
sleep(10)  # Wait before attempting to connect

# Connect to the MQTT broker
mqttc.connect("emqx1", 1883, 60)

# Subscribe to the 'weather' topic again just to be sure
mqttc.subscribe("weather")

# Start the network loop and block forever
mqttc.loop_forever()
