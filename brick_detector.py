from dependencies import *


class BrickDetector:

    def __init__(self):
        self.color = None
        self.motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
        self.color = ColorSensor(Port.S3)
        self.touch = TouchSensor(Port.S4)
        #self.ir = InfraredSensor(Port.S2)

    def brickAhead(self):
        if self.touch.pressed():
            self.motor.run_angle(10, 90)

    def brickCollected(self):
        self.motor.reset_angle(0)
