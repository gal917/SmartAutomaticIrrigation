import json
from mqtt_client import MqttClient, load_mqtt_settings

def on_message(client, userdata, msg):
    if msg.topic == "iot/relay":
        payload = msg.payload.decode()
        if payload == "ON":
            print("Relay turned ON - Water pump activated")
        elif payload == "OFF":
            print("Relay turned OFF - Water pump deactivated")

if __name__ == "__main__":
    settings = load_mqtt_settings('mqtt_settings.json')
    mqtt_client = MqttClient(
        broker=settings["broker"], 
        port=int(settings["port"]), 
        client_name="relay_client", 
        username=settings["username"], 
        password=settings["password"]
    )

    mqtt_client.client.on_message = on_message
    mqtt_client.connect()
    mqtt_client.subscribe("iot/relay")

    # שמירה על ריצת הסקריפט כדי להאזין להודעות
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mqtt_client.disconnect()
