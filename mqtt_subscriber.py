import json
from celery_app import process_weather_data, average_result
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
        json_str = message.payload.decode("utf-8")
        weather_data = json.loads(json_str)
        process_weather_data.delay(
            temperature=weather_data["temperature"],
            humidity=weather_data["humidity"],
            wind_speed=weather_data["wind_speed"],
        )
        average_result.delay()
    except json.JSONDecodeError:
        print("Received message is not in JSON format")
    except KeyError as e:
        print(f"Missing key in received data: {e}")


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        client.subscribe("weather")


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

try:
    mqttc.connect("emqx1", 1883, 60)
except ConnectionRefusedError:
    print("Connecting to MQTT broker...")

mqttc.loop_forever()
