import json
import os
from mqtt_client import MqttClient, load_mqtt_settings

data_file = 'sensor_data.json'

def save_data_to_file(data):
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            try:
                file_data = json.load(file)
                if not isinstance(file_data, list):
                    file_data = []
            except json.JSONDecodeError:
                file_data = []
    else:
        file_data = []

    file_data.append(data)

    with open(data_file, 'w') as file:
        json.dump(file_data, file, indent=4)

def check_conditions(temperature, humidity):
    print(f"Checking conditions for Temperature: {temperature}, Humidity: {humidity}")
    if temperature < 15 or humidity < 30:
        status = "Too Low"
    elif temperature > 30 or humidity > 70:
        status = "Too High"
    else:
        status = "Middle"
    print(f"Status determined: {status}")
    return status

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    if msg.topic == "iot/plant_info":
        plant_info = json.loads(payload)
        print(f"Plant Info - Serial Number: {plant_info['serial_number']}, Plant Name: {plant_info['plant_name']}, Temperature: {plant_info['temperature']}, Humidity: {plant_info['humidity']}")

        status = check_conditions(plant_info['temperature'], plant_info['humidity'])
        plant_info['status'] = status
        print(f"Status: {status}")

        save_data_to_file(plant_info)
    else:
        print(f"Message received: {msg.topic} {payload}")

if __name__ == "__main__":
    settings = load_mqtt_settings('mqtt_settings.json')
    mqtt_client = MqttClient(
        broker=settings["broker"], 
        port=int(settings["port"]), 
        client_name="main_gui_client", 
        username=settings["username"], 
        password=settings["password"]
    )

    mqtt_client.client.on_message = on_message
    mqtt_client.connect()
    mqtt_client.subscribe("iot/plant_info")

    # Keep the script running to listen for messages
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mqtt_client.disconnect()
