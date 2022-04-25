"""
@file   states.py
@author Emil Roy

This file contains the States Section widget. It contains various statuses relating to the container and the payloads.
"""
from  PyQt5.QtWidgets import QLabel, QPlainTextEdit, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt
import constants
import commands


#create payload states/statuses
payload1Label = QLabel("Payload")
payload1Label.setStyleSheet("color: blue;"
                         "border-style: solid;"
                         "background-color: #87CEFA;"
                         "border-width: 2px;"
                         "border-color: #1E90FF;"
                         "border-radius: 3px")
pay1ValidPackets = 0
pay1InvalidPackets = 0
pay1ValidPacketLabel = QLabel("Valid Packets: " + str(pay1ValidPackets))#TODO how do we add packets?
pay1InvalidPacketLabel = QLabel("Invalid Packets: " + str(pay1InvalidPackets))

pay1PointingError = QLabel("Pointing Error: ")

payload1State = QLabel("Tethered Payload State: Launchpad and\nNot Deployed")
payload1State.setStyleSheet("color: red")

#create container states/statuses
containerLabel = QLabel("Container")
containerLabel.setStyleSheet("color: blue;"
                         "border-style: solid;"
                         "background-color: #87CEFA;"
                         "border-width: 2px;"
                         "border-color: #1E90FF;"
                         "border-radius: 3px")
conValidPackets = 0
conInvalidPackets = 0
conValidPacketLabel = QLabel("Valid Packets: " + str(conValidPackets))#TODO how do we add packets?
conInvalidPacketLabel = QLabel("Invalid Packets: " + str(conInvalidPackets))

containerState = QLabel("State: Launchpad")
containerState.setStyleSheet("color: red")

# Container GPS info
gpsTime = "no info received"
gpsLat = 0.0
gpsLon = 0.0
gpsAlt = 0.0
gpsSats = 0

gpsTimeLabel = QLabel("GPS Time (UTC): " + gpsTime)
gpsCoordLabel = QLabel("GPS Coords: " + str(gpsLat) + ", " + str(gpsLon))
gpsAltLabel = QLabel("GPS Altitude (m): " + str(gpsAlt))
gpsSatsLabel = QLabel(str(gpsSats) + " GPS satellites tracking Container")

# returns layout for payload info
def buildPay1Layout():
    #adding all the widgets to the layout
    layout = QVBoxLayout()
    # payload 1
    layout.addWidget(payload1Label)
    layout.addWidget(pay1ValidPacketLabel)
    layout.addWidget(pay1InvalidPacketLabel)
    layout.addWidget(pay1PointingError)
    layout.addWidget(payload1State)
    return layout

# return container info as layout
def buildContainerLayout():
    layout = QVBoxLayout()
    layout.addWidget(containerLabel)
    layout.addWidget(conValidPacketLabel)
    layout.addWidget(conInvalidPacketLabel)
    layout.addWidget(containerState)
    layout.addWidget(gpsTimeLabel)
    layout.addWidget(gpsCoordLabel)
    layout.addWidget(gpsAltLabel)
    layout.addWidget(gpsSatsLabel)
    return layout

#to update the pointing error of payload
def updatePointingError(error):
    pay1PointingError.setText("Pointing Error: " + str(error))

#function to update first payload states
def updatePayload1State(state):
    if(state == "R"):
        payload1State.setText("Tethered Payload State: Deployed and\nDescending")
        payload1State.setStyleSheet("color: green")

#function to update container states
def updateContainerState(state):
    if(state == "ASCENT"):
        containerState.setText("State: Ascending")
        containerState.setStyleSheet("color: green")
        payload1State.setText("Tethered Payload State: Ascending and\nNOT Deployed")
        payload1State.setStyleSheet("color: orange")

    elif(state == "DESCENT"):
        containerState.setText("State: Descending")
        containerState.setStyleSheet("color: orange")
    elif(state == "LANDED"):
        containerState.setText("State: Landed")
        containerState.setStyleSheet("color: purple")

def update_packet_count(packetCount, sp1PacketCount):
    # update variables
    global pay1ValidPackets, conValidPackets
    if packetCount + sp1PacketCount == -2:
        pay1ValidPackets += 1
    else:
        pay1ValidPackets = sp1PacketCount
        conValidPackets = packetCount - sp1PacketCount

    # update labels
    pay1ValidPacketLabel.setText("Valid Packets: " + str(pay1ValidPackets))
    conValidPacketLabel.setText("Valid Packets: " + str(conValidPackets))

def update_gps(time, lat, lon, alt, sats):
    global gpsTime, gpsLat, gpsLon, gpsAlt, gpsSats
    gpsTime = time
    gpsLat = lat
    gpsLon = lon
    gpsAlt = alt[:6]
    gpsSats = sats

    gpsTimeLabel.setText("GPS Time (UTC): " + gpsTime)
    gpsCoordLabel.setText("GPS Coords: " + str(gpsLat) + ", " + str(gpsLon))
    print(type(gpsAlt))
    gpsAltLabel.setText("GPS Altitude (m): " + str(gpsAlt))
    gpsSatsLabel.setText(str(gpsSats) + " GPS satellites tracking Container")


def update_state(packet):
    packet_args = packet.split(",")
    if packet_args[3] == "C":
        # update states
        updatePayload1State(packet_args[5])
        updateContainerState(packet_args[14])

        # update gps information
        update_gps(packet_args[9], packet_args[10], packet_args[11], packet_args[12], packet_args[13])

        # next, update packet counts regardless of type of packet
        update_packet_count(int(packet_args[2]), int(packet_args[15]))
    elif packet_args[3] == "T":
        update_packet_count(-1, -1)
