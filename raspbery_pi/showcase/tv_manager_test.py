import threading
import paho.mqtt.client as mqtt
import json
import time
from subprocess import Popen, PIPE, check_output

MQTT_HOST = 'test.mosquitto.org'
MQTT_TOPIC = 'iotTW'
TURN_OFF_TIME = 0.5
turn_off_timer = None

def send_cec_command(command):
    print 'this command has been sent: {}'.format(command)

def off():
    print 'tv off'
    send_cec_command('standby 0')

def time_elapsed():
    off()

def cancel_timer():
    global turn_off_timer
    if turn_off_timer is not None:
        turn_off_timer.cancel()
    print 'timer has been canceled'

def start_timer():
    global turn_off_timer
    turn_off_timer = threading.Timer(TURN_OFF_TIME * 60, time_elapsed)
    turn_off_timer.start()
    print 'timer started'

def on_message(client, userdata, message):
    try:
        message = json.loads(str(message.payload))
        presence = message['presence']
        if presence:
            cancel_timer()
        else:
            cancel_timer()
            start_timer()
    except:
        print 'message {} could not be decoded'.format(message)

def on_connect(client, userdata, flags, result):
    print 'connected to iot mqtt server with result: {}'.format(result)
    client.subscribe(MQTT_TOPIC)

if __name__ == '__main__':
    print 'TV MANAGER STARTED'
    turn_off_timer = threading.Timer(TURN_OFF_TIME * 60, time_elapsed)
    turn_off_timer.start()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, 1883, 60)
    client.loop_forever()
