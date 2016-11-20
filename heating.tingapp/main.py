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

@right_button.press
def on_right():
    connect()

@midleft_button.press
def on_midleft():
    connect()

@midright_button.press
def on_midright():
    connect()

@left_button.press
def on_left():
    connect()

@touch_button('Off', xy=(55,175), color='blue')
def on_touch():
    mqttc.publish('heating/radiators/target', payload='10.0', qos=1, retain=True)

@touch_button('On', xy=(155,175), color='blue')
def on_touch():
    mqttc.publish('heating/radiators/target', payload='21.0', qos=1, retain=True)

@touch_button('Boost', xy=(255,175), color='orange')
def on_touch():
    mqttc.publish('heating/radiators/target', payload='22.5', qos=1, retain=True)

@every(seconds=1.0/15)
def mqtt_loop():
    mqttc.loop()

@every(seconds=1.0/30)
def loop():
    screen.fill(
        color='black'
    )

    touch_button.renderAll()

    screen.text(
        time.strftime('%H:%M:%S'),
        xy=(315, 5),
        color='white',
        font_size=14,
        align='topright'
    )
    screen.text(
        Status,
        xy=(5, 5),
        color='white',
        font_size=12,
        align='topleft'
    )
    screen.text(
        u'Actual: {0}°C'.format(Topics['heating/radiators/actual']),
        xy=(5, 235),
        color='white',
        align='bottomleft',
        font_size=18,
    )
    screen.text(
        u'Target: {0}°C'.format(Topics['heating/radiators/target']),
        xy=(160, 235),
        color='white',
        align='bottomleft',
        font_size=18,
    )

    if Topics['heating/radiators/state'] == 'on':
        screen.image('fire.png', align='bottomright', xy=(315,235))


tingbot.run()
