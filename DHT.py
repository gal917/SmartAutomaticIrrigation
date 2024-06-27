import json
import time
import random
import string
from mqtt_client import MqttClient, load_mqtt_settings

def generate_random_string(length=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def publish_sensor_data(mqtt_client):
    serial_number = generate_random_string()
    plant_name = generate_random_string()
    temp_topic = "iot/temperature"
    humidity_topic = "iot/humidity"
    info_topic = "iot/plant_info"
    
    # Adjusted ranges for temperature and humidity
    temperature = random.uniform(5.0, 40.0)
    humidity = random.uniform(10.0, 80.0)
    
    info_payload = json.dumps({
        "serial_number": serial_number,
        "plant_name": plant_name,
        "temperature": temperature,
        "humidity": humidity
    })
    
    mqtt_client.publish(temp_topic, temperature)
    mqtt_client.publish(humidity_topic, humidity)
    mqtt_client.publish(info_topic, info_payload)

if __name__ == "__main__":
    settings = load_mqtt_settings('mqtt_settings.json')
    mqtt_client = MqttClient(
        broker=settings["broker"], 
        port=int(settings["port"]), 
        client_name="dht_client", 
        username=settings["username"], 
        password=settings["password"]
    )

    mqtt_client.connect()
    try:
        while True:
            # Simulating publishing sensor data with additional attributes
            publish_sensor_data(mqtt_client)
            time.sleep(5)
    except KeyboardInterrupt:
        mqtt_client.disconnect()
