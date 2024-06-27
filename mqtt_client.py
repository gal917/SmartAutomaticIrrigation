import paho.mqtt.client as mqtt
import json

class MqttClient:
    def __init__(self, broker, port, client_name, username, password):
        self.broker = broker
        self.port = port
        self.client_name = client_name
        self.username = username
        self.password = password
        self.client = mqtt.Client(self.client_name)
        self.client.username_pw_set(username, password)

        # Define callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Message received: {msg.topic} {msg.payload}")

    def subscribe(self, topic):
        self.client.subscribe(topic)
        print(f"Subscribed to {topic}")

    def publish(self, topic, payload):
        self.client.publish(topic, payload)
        print(f"Published {payload} to {topic}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

def load_mqtt_settings(filename):
    with open(filename, 'r') as file:
        return json.load(file)
