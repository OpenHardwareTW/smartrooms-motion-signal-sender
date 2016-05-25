import paho.mqtt.client as mqtt
import json
import time
from subprocess import Popen, PIPE, check_output

MQTT_HOST = 'jarvis.casa.com'
MQTT_TOPIC = 'iotTW'

def send_cec_command(command):
    echo_process = Popen(('echo', command), stdout=PIPE)
    cec_output = check_output(('cec-client','-s','RPI'), stdin=echo_process.stdout)
    echo_process.wait()

def on_connect(client, userdata, flags, result):
    print 'connected to iot mqtt server with result: {}'.format(result)
    client.subscribe(MQTT_TOPIC)

def turn_on_tv():
    print 'tv on'
    send_cec_command('on 0')

def turn_off_tv():
    print 'tv off'
    send_cec_command('standby 0')

def on_message(client, userdata, message):
    try:
        message = json.loads(str(message.payload))
        if message.get('tv_status') == 'on':
            turn_on_tv()
        if message.get('tv_status') == 'off':
            turn_off_tv()
    except:
        print 'message {} could not be decoded'.format(message)

if __name__ == '__main__':
    print 'TV MANAGER STARTED'
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, 1883, 60)
    client.loop_forever()
