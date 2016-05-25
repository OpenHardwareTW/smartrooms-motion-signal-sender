import threading
import paho.mqtt.client as mqtt
import json
import time
from subprocess import Popen, PIPE, check_output

MQTT_HOST = 'jarvis.casa.com'
MQTT_TOPIC = 'iotTW'
TURN_OFF_TIME = 5
turn_off_timer = None

def send_cec_command(command):
    echo_process = Popen(('echo', command), stdout=PIPE)
    cec_output = check_output(('cec-client','-s','RPI'), stdin=echo_process.stdout)
    echo_process.wait()

def off():
    print 'tv off'
    send_cec_command('standby 0')

def time_elapsed():
    print 'turning off tv'
    off()

def on_message():
    try:
        message = json.loads(str(message.payload))
        if message.get('presence') == '1':
            if turn_off_timer is not None:
                turn_off_timer.cancel()
        if message.get('presence') == '0':
            if turn_off_timer is not None:
                turn_off_timer.cancel()
            turn_off_timer.start()
    except:
        print 'message {} could not be decoded'.format(message)

def on_connect():
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
