# referenced from the #pyqt channel on Freenode, by epifanio
# Remixed By: Emil R.
#Description: Compass widget to help represent what direction the payload camera is facing

from PyQt5.QtCore import pyqtProperty, pyqtSignal, QPoint, QSize, pyqtSlot, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpinBox, QLabel


class compassWidget(QWidget):

    angleChanged = pyqtSignal(float)
    
    def __init__(self, parent = None):
    
        QWidget.__init__(self, parent)
        
        self._angle = 0.0
        self._margins = 10
        self._pointText = {0: "N", 45: "NE", 90: "E", 135: "SE", 180: "S",
                           225: "SW", 270: "W", 315: "NW"}
    
    def paintEvent(self, event):
    
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.fillRect(event.rect(), self.palette().brush(QPalette.Window))
        self.drawMarkings(painter)
        self.drawNeedle(painter)
        
        painter.end()
    
    def drawMarkings(self, painter):
    
        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        scale = min((self.width() - self._margins)/120.0,
                    (self.height() - self._margins)/120.0)
        painter.scale(scale, scale)
        
        font = QFont(self.font())
        font.setPixelSize(10)
        metrics = QFontMetricsF(font)
        
        painter.setFont(font)
        painter.setPen(self.palette().color(QPalette.Shadow))
        
        i = 0
        while i < 360:
        
            if i % 45 == 0:
                painter.drawLine(0, -40, 0, -50)
                painter.drawText(-metrics.width(self._pointText[i])/2.0, -52,
                                 self._pointText[i])
            else:
                painter.drawLine(0, -45, 0, -50)
            
            painter.rotate(15)
            i += 15
        
        painter.restore()
    
    def drawNeedle(self, painter):
    
        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        painter.rotate(self._angle)
        scale = min((self.width() - self._margins)/120.0,
                    (self.height() - self._margins)/120.0)
        painter.scale(scale, scale)
        
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(self.palette().brush(QPalette.Shadow))
        
        painter.drawPolygon(
            QPolygon([QPoint(-10, 0), QPoint(0, -45), QPoint(10, 0),
                      QPoint(0, 45), QPoint(-10, 0)])
            )
        
        painter.setBrush(self.palette().brush(QPalette.Highlight))
        
        painter.drawPolygon(
            QPolygon([QPoint(-5, -25), QPoint(0, -45), QPoint(5, -25),
                      QPoint(0, -30), QPoint(-5, -25)])
            )
        
        painter.restore()
    
    def sizeHint(self):
    
        return QSize(150, 150)
    
    def angle(self):
        return self._angle

    @pyqtSlot(int)
    def setAngle(self, angle):

        if angle != self._angle:
            self._angle = angle
            self.angleChanged.emit(angle)
            self.update()
    angle = pyqtProperty(int, angle, setAngle)

title = QLabel("Payload Camera Direction")
title.setAlignment(Qt.AlignCenter)
title.setStyleSheet("font-size: 13pt")
compass = compassWidget()
spinBox = QSpinBox()
spinBox.setRange(0, 359)
spinBox.valueChanged.connect(compass.setAngle)

def build():
    layout = QVBoxLayout()
    layout.addWidget(title)
    layout.addWidget(compass, 2)
    layout.addWidget(spinBox)
    return layout





