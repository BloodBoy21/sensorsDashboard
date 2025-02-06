import random
import os
from paho.mqtt import client as mqtt_client
import dotenv
from .dashboard import my_dashboard
import json

# Load environment variables from .env file
dotenv.load_dotenv()

# MQTT configuration
broker = os.getenv("MQTT_BROKER")
port = int(os.getenv("MQTT_PORT", 1883))  # Default port is 1883 if not specified
topic = os.getenv(
    "MQTT_TOPIC", "sensors"
)  # Default topic is "sensors" if not specified
client_id = f"publish-{random.randint(0, 1000)}"
username = os.getenv("MQTT_USER")
password = os.getenv("MQTT_PASSWORD")


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            return
        print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client()
    if username and password:
        client.username_pw_set(username, password)
    client.on_connect = on_connect

    print(
        f"mqtt://{broker}:{port} with client_id={client_id}, username={username}, password={password}"
    )
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        data = msg.payload.decode()
        data = json.loads(data)
        for sensor in data:
            my_dashboard.update_sensor(sensor["name"], sensor["value"])

    client.subscribe(topic)
    client.on_message = on_message
    print(f"Subscribed to topic: {topic}")


def init_mqtt():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
