import json
import time
from mqtt_client import MqttClient, load_mqtt_settings

def on_button_press(mqtt_client):
    topic = "iot/button"
    payload = "Button Pressed"
    mqtt_client.publish(topic, payload)
    mqtt_client.publish("iot/relay", "ON")

if __name__ == "__main__":
    settings = load_mqtt_settings('mqtt_settings.json')
    mqtt_client = MqttClient(
        broker=settings["broker"], 
        port=int(settings["port"]), 
        client_name="button_client", 
        username=settings["username"], 
        password=settings["password"]
    )

    mqtt_client.connect()
    try:
        while True:
            # Simulating a button press
            on_button_press(mqtt_client)
            time.sleep(10)
    except KeyboardInterrupt:
        mqtt_client.disconnect()
