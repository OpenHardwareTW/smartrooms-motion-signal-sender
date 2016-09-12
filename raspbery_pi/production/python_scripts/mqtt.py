import paho.mqtt.client as mqtt


class MQTT():
    def __init__(self, server, port, room_name):
        self.server = server
        self.port = port
        self.client = mqtt.Client(room_name)
        self.client.connect(self.server, self.port)

    def publish(self, message, topic):
        self.client.publish(topic, message)
        self.client.loop(2)
