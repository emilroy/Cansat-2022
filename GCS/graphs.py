"""
@file   graphs.py
@author Emil Roy, Joshua Tenorio

This file contains the Graphs and States widgets.
"""
from  PyQt5.QtWidgets import QLabel, QPlainTextEdit, QLineEdit, QGridLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import compassWidget
import states
import simulation as sim
import numpy as np

# used for stand in values
initial_array = [0] * 120 # create a List of 120 zero's
initial_cx = np.empty(120)
initial_sp1x = np.array(list(range(-120, 0)))
initial_sp2x = np.array(list(range(-120, 0)))

#Container Graphs==============================================================

#graph to check the CONTAINER ALTITUDE
containerAltitudeGraph = pg.GraphicsLayoutWidget()
containerAltitudeData = np.array(initial_array).astype(float)
caPlot = containerAltitudeGraph.addPlot(title = "Container Altitude Data")
containerAltitudeCurve = caPlot.plot(containerAltitudeData)
caPlot.setLabel('left', "Altitude(m)")
caPlot.setLabel('bottom', "# of Packets")

#graph to check the containers GPS LOCATION. TODO
containerLocationGraph = pg.GraphicsLayoutWidget()
ctLatData = np.array(initial_array).astype(float)
ctLongData = np.array(initial_array).astype(float)
caPlot = containerLocationGraph.addPlot(title = "Location")
containerLocationCurve = caPlot.plot(ctLatData,ctLongData)
caPlot.setLabel('left', "Longitude")
caPlot.setLabel('bottom', "latitude")
caPlot.showGrid(x = True, y = True)

#Container and Payload Graphs===========================================================

# graph the VOLTAGE DATA
voltageGraph = pg.GraphicsLayoutWidget()
containerVoltageData = np.array(initial_array).astype(float)
payloadVoltageData = np.array(initial_array).astype(float)
cvPlot = voltageGraph.addPlot(title = "Voltage Data")
containerVoltageCurve = cvPlot.plot(containerVoltageData, "Container Voltage", 'r')
payloadVoltageCurve = cvPlot.plot(payloadVoltageData, "Payload Voltage", 'b')
cvPlot.setLabel('left', "Volts(V)")
cvPlot.setLabel('bottom', "# of Packets")

#graph to check the TEMPERATURE
tempGraph = pg.GraphicsLayoutWidget()
containerTempData = np.array(initial_array).astype(float)
payloadTempData = np.array(initial_array).astype(float)
ctPlot = tempGraph.addPlot(title = "Temperature Data")
containerTempCurve = ctPlot.plot(containerTempData, "Container Temperature", 'r')
payloadTempCurve = ctPlot.plot(payloadTempData, "Payload Temperature", 'b')
ctPlot.setLabel('left', "Temperature(C°)")
ctPlot.setLabel('bottom', "# of Packets")

#PAYLOAD Graphs------------------------------------------------------------

#graph to check the PAYLOAD ALTITUDE
payload1AltitudeGraph = pg.GraphicsLayoutWidget()
p1AltitudeData = np.array(initial_array).astype(float)
p1aPlot = payload1AltitudeGraph.addPlot(title = "Payload Altitude Data")
p1AltitudeCurve = p1aPlot.plot(p1AltitudeData)
p1aPlot.setLabel('left', "Altitude(m)")
p1aPlot.setLabel('bottom', "# of Packets")

#the PAYLOAD'S ORIENTATION
payloadOrientationGraph = pg.GraphicsLayoutWidget()
payloadOrientationData = np.array(initial_array).astype(float)
caPlot = payloadOrientationGraph.addPlot(title = "Payload Orientation")
payloadOrientationCurve = caPlot.plot(payloadOrientationData)
caPlot.setLabel('left', "Orientation(°)")
caPlot.setLabel('bottom', "# of Packets")

camOrientationData = 0 

def build():
    layout = QGridLayout()
    pay1Widget: QVBoxLayout = states.buildPay1Layout()
    conWidget: QVBoxLayout = states.buildContainerLayout()
    compWidget: QVBoxLayout = compassWidget.build()
    layout.addLayout(pay1Widget, 0, 0)
    layout.addWidget(payload1AltitudeGraph, 0, 1)
    layout.addWidget(containerAltitudeGraph, 0, 2)
    layout.addLayout(compWidget, 0, 3)

    layout.setRowMinimumHeight(2, 10)#adds spacing between payloads and container
    #add bottom row
    layout.addLayout(conWidget, 3, 0)
    layout.addWidget(tempGraph, 3, 1)
    layout.addWidget(voltageGraph, 3, 2)
    layout.addWidget(containerLocationGraph, 3, 3)

    return layout

# these variables are used for updating the graphs
containerPtr = 0
p1Ptr = 0

# TODO: implement update function
# ie setData setPos functions
def update():
    # update container
    compassWidget.spinBox.setValue(camOrientationData)

    if containerPtr > 119:
        containerVoltageCurve.setData(containerVoltageData)
        containerAltitudeCurve.setData(containerAltitudeData)
        containerTempCurve.setData(containerTempData)
        payloadTempCurve.setData(payloadTempData)
        containerLocationCurve.setData(ctLatData, ctLongData)

        containerVoltageCurve.setPos(containerPtr-120, containerPtr)
        containerAltitudeCurve.setPos(containerPtr-120, containerPtr)
        containerTempCurve.setPos(containerPtr-120, containerPtr)
        payloadTempCurve.setPos(containerPtr-120, containerPtr)
        containerLocationCurve.setPos(containerPtr-120, containerPtr) #have feeling gotta setpos by data not ctPtr

    else:
        containerVoltageCurve.setData(containerVoltageData[:containerPtr])
        containerAltitudeCurve.setData(containerAltitudeData[:containerPtr])
        containerTempCurve.setData(containerTempData[:containerPtr])
        payloadTempCurve.setData(containerTempData[:containerPtr])
        containerLocationCurve.setData(ctLatData, ctLongData)

    #update payloads
    if p1Ptr > 119:
        p1AltitudeCurve.setData(p1AltitudeData)
        p1AltitudeCurve.setPos(p1Ptr-120, p1Ptr)
    else:
        p1AltitudeCurve.setData(p1AltitudeData[:p1Ptr])

# given a packet, update arrays
def update_data(packet):
    global containerAltitudeData, containerVoltageData, containerTempData, ctLatData, ctLongData
    global p1AltitudeData, payloadTempData, camOrientationData, payloadVoltageData
    global containerPtr, p1Ptr

    # send packet to states widget
    states.update_state(packet)

    # parse packet for stuff to update
    packet_args = packet.split(",")

    if packet_args[3] == "C":
        if containerPtr > 119:
            containerPtr += 1
            containerAltitudeData[:-1] = containerAltitudeData[1:]
            containerAltitudeData[-1] = float(packet_args[6])

            containerTempData[:-1] = containerTempData[1:]
            containerTempData[-1] = float(packet_args[7])

            containerVoltageData[:-1] = containerVoltageData[1:]
            containerVoltageData[-1] = float(packet_args[8])

            ctLatData[:-1] = ctLatData[1:]
            ctLatData[-1] = float(packet_args[10])
            ctLongData[:-1] = ctLongData[1:]
            ctLongData[-1] = float(packet_args[11])
        else:
            containerAltitudeData[containerPtr] = float(packet_args[6])
            containerTempData[containerPtr] = float(packet_args[7])
            containerVoltageData[containerPtr] = float(packet_args[8])
            ctLatData[containerPtr] = float(packet_args[10])
            ctLongData[containerPtr] = float(packet_args[11])
            containerPtr += 1

    elif packet_args[3] == "T":

        if p1Ptr > 119:
            p1Ptr += 1
            p1AltitudeData[:-1] = p1AltitudeData[1:]
            p1AltitudeData[-1] = float(packet_args[4])

            payloadTempData[:-1] = payloadTempData[1:]
            payloadTempData[-1] = float(packet_args[5])

            payloadVoltageData[:-1] = payloadVoltageData[1:]
            payloadVoltageData[-1] = float(packet_args[6])
        else:
            p1AltitudeData[p1Ptr] = float(packet_args[4])
            payloadTempData[p1Ptr] = float(packet_args[5])
            payloadVoltageData[containerPtr] = float(packet_args[6])
            p1Ptr += 1

        #compassWidget.spinBox.setAngle() way to update compass angle
    else:
        print("GRAPH ERR: invalid packet")
