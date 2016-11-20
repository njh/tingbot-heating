#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tingbot
from tingbot import *
from touch_button import *
import paho.mqtt.client as mqtt
import time
import re

mqttc = mqtt.Client()
Status = 'Disconnected'
Topics = {
    'heating/radiators/actual':  '?',
    'heating/radiators/target':  '?',
    'heating/radiators/state':   '?',
    'heating/underfloor/actual': '?',
    'heating/underfloor/target': '?',
    'heating/underfloor/state':  '?',
}

def on_connect(client, userdata, flags, rc):
    global Status
    if rc == 0:
        Status = 'Connected'
        for topic in Topics:
            client.subscribe(topic)
    else:
        Status = 'MQTT Error'

def on_disconnect(client, userdata, rc):
    global Status
    Status = 'Disconnected'

def on_message(client, userdata, msg):
    global Topics
    if re.match('^[\d\.-]+$', msg.payload):
        Topics[msg.topic] = '%1.1f' % float(msg.payload)
    else:
        Topics[msg.topic] = msg.payload

mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message


def connect():
    global Status
    Status = 'Connecting'
    mqttc.connect('mqtt.aelius.co.uk', keepalive=10)

@once()
def setup():
    screen.fill(color='black')
    connect()

@left_button.press
def on_left():
    connect()

@touch_button('Off', xy=(55,75), color='blue')
def on_touch():
    mqttc.publish('heating/radiators/target', payload='10.0', qos=1, retain=True)

@touch_button('On', xy=(160,75), color='blue')
def on_touch():
    mqttc.publish('heating/radiators/target', payload='21.0', qos=1, retain=True)

@touch_button('Boost', xy=(265,75), color='red')
def on_touch():
    mqttc.publish('heating/radiators/target', payload='22.5', qos=1, retain=True)

@touch_button('Off', xy=(55,190), color='blue')
def on_touch():
    mqttc.publish('heating/underfloor/target', payload='10.0', qos=1, retain=True)

@touch_button('On', xy=(160,190), color='blue')
def on_touch():
    mqttc.publish('heating/underfloor/target', payload='21.0', qos=1, retain=True)

@touch_button('Boost', xy=(265,190), color='red')
def on_touch():
    mqttc.publish('heating/underfloor/target', payload='22.5', qos=1, retain=True)

@every(seconds=1.0/15)
def mqtt_loop():
    mqttc.loop()

@every(seconds=1.0/30)
def loop():
    screen.fill(
        color=(80,80,80)
    )

    ## Status at top bar
    screen.rectangle(
        xy=(0,0), size=(320,25), color='black',  align='topleft'
    )
    screen.text(
        time.strftime('%H:%M:%S'),
        xy=(315, 5),  color='white',  font_size=14,  align='topright'
    )
    screen.text(
        Status,
        xy=(5, 5),    color='white',  font_size=12,  align='topleft'
    )


    ## Radiators Heating Zone
    screen.text(
        'Radiators',
        xy=(5, 55),    color='white',  font_size=18,  align='bottomleft'
    )

    screen.text(
        u'Target: {0}°C'.format(Topics['heating/radiators/target']),
        xy=(5, 120),   color='white',  font_size=18,  align='bottomleft',
    )
    screen.text(
        u'Actual: {0}°C'.format(Topics['heating/radiators/actual']),
        xy=(160, 120), color='white',  font_size=18,  align='bottomleft',
    )

    if Topics['heating/radiators/state'] == 'on':
        screen.image('fire.png', align='bottomright', xy=(315, 120))


    ## Underfloor Heating Zone
    screen.text(
        'Underfloor',
        xy=(5, 170),   color='white',  font_size=18,  align='bottomleft'
    )

    screen.text(
        u'Target: {0}°C'.format(Topics['heating/underfloor/target']),
        xy=(5, 235),   color='white',  font_size=18,  align='bottomleft',
    )
    screen.text(
        u'Actual: {0}°C'.format(Topics['heating/underfloor/actual']),
        xy=(160, 235), color='white',  font_size=18,  align='bottomleft',
    )

    if Topics['heating/underfloor/state'] == 'on':
        screen.image('fire.png', align='bottomright', xy=(315, 235))

    touch_button.renderAll()

tingbot.run()
