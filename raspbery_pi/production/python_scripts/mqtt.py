import paho.mqtt.client as mqtt


class MQTT():
    def __init__(self, server, port, room_name):
        self.server = server
        self.port = port
        self.topic = room_name
        self.client = mqtt.Client(room_name)
        self.client.connect(self.server, self.port)

    def publish(self, message):
        self.client.publish(self.room_name, message)
        self.client.loop(2)
