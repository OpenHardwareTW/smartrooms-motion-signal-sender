import paho.mqtt.client as mqtt
import time
from threading import Timer

# Publish message example: mosquitto_pub -h test.mosquitto.org -t 'thoughtwor' -m 'Test123'

MQTT_HOST = 'test.mosquitto.org'
MQTT_TOPIC = 'thoughtwor'

class AppTimer:
    status = 1
    minutes = 0
    seconds = 15

    @staticmethod
    def reset():
        AppTimer.minutes = 0
        AppTimer.seconds = 15
        AppTimer.status = 1

    @staticmethod
    def stop():
        AppTimer.status = 0

    @staticmethod
    def tick():
        if AppTimer.status == 0:
            Timer(1, AppTimer.tick, ()).start()
            return

        if AppTimer.seconds == 0:
            AppTimer.seconds = 59
            AppTimer.minutes -= 1

            if AppTimer.minutes < 0:
                do_something()
        else:
            AppTimer.seconds -= 1

        print("{}:{}".format(AppTimer.minutes, AppTimer.seconds))
        Timer(1, AppTimer.tick, ()).start()

    @staticmethod
    def start():
        AppTimer.status = 1
        AppTimer.reset()
        Timer(1, AppTimer.tick, ()).start()

def do_something():
    print('TURNING TV OFF... BAM')
    AppTimer.stop()

def on_connect(client, userdata, flags, result):
    print('connected to mosquitto mqtt server with result: {}'.format(result))
    client.subscribe(MQTT_TOPIC)
    AppTimer.start()

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    try:
        print(message.topic+" "+str(message.payload))
        AppTimer.reset()
    except Exception:
        print('message {} could not be decoded'.format(message))


if __name__ == '__main__':
    print('SERVER STARTED')
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host=MQTT_HOST, port=1883, keepalive=60)
    client.loop_forever()