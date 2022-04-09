"""
@file   local_test.py
@author Joshua Tenorio

Contains the Local Test GUI for testing GCS in real time.
"""
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget
from testing import sensors


window = QWidget()
window.setWindowTitle("Team 1052 W.A.F.F.L.E GCS Local Test Suite")
window.resize(450,100)
layout = QVBoxLayout()
setDataButton = QPushButton("Randomize Data")
sendCPacketButton = QPushButton("Send Container Packet")
sendSp1PacketButton = QPushButton("Send TP Packet")

layout.addWidget(setDataButton)
layout.addWidget(sendCPacketButton)
layout.addWidget(sendSp1PacketButton)
window.setLayout(layout)

setDataButton.clicked.connect(sensors.randomizeData)
sendCPacketButton.clicked.connect(sensors.sendContainerPacket)
sendSp1PacketButton.clicked.connect(sensors.sendPayloadPacket1)


def run():
    window.show()