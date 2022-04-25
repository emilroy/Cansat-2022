"""
@file mqtt_util.py
@author cansat/Emil

Implementation for processing data to MQTT broker for live-remote viewing of data
"""
# to test if working, go to http://cansat.info/plot.html
import paho.mqtt.client as mqtt
client = mqtt.Client()
def setup() :
    client = mqtt.Client()
    client.connect("mqtt://1052:Niyxsiku549@cansat.info");


def draw():
    pass

def keyPressed():
    client.publish("teams/1052", "world");

def clientConnected() :
    print("client connected");
# client.subscribe("/hello");

def messageReceived(topic, payload):
    print("new message: " + topic + " - " + str(payload));

def connectionLost() :
    print("connection lost");
