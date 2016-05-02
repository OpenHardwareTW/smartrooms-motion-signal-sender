import paho.mqtt.client as mqtt
import time


MQTT_HOST = 'test.mosquitto.org'
MQTT_TOPIC = 'thoughtwor'
IDLE_MINUTES = 20

def start_timer():
    pass

def reset_timer():
    pass

def on_connect(client, userdata, flags, result):
    print 'connected to mosquitto mqtt server with result: {}'.format(result)
    client.subscribe(MQTT_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    try:
        print(message.topic+" "+str(message.payload))
    except Exception:
        print 'message {} could not be decoded'.format(message)

if __name__ == '__main__':
    print ''
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host=MQTT_HOST, port=1883, keepalive=60)
    client.loop_forever()