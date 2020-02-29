from dependencies import *


class BrickDetector:

    def __init__(self):
        self.color = None
        self.motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        self.left_wheel = Motor(Port.B, Direction.COUNTERCLOCKWISE)
        self.right_wheel = Motor(Port.D, Direction.COUNTERCLOCKWISE)

        self.color = ColorSensor(Port.S4)
        self.us = UltrasonicSensor(Port.S2)

        # bricks to collect [B,B,R,R,Y,Y]
        self.collected = [False]*6

    def brickAhead(self):
        """
        Returns True if brick was loaded on robot, else False
        """
        # closer than 3 cm means brick below
        if self.us.distance() < 150:
            print("Brick detected")
            self.motor.run_angle(360, 1890)
            print("*brick loaded*")
            # TODO: Return back.
            self.motor.run_angle(360, -1890)
            if self.shouldPickUpBrick():
                self.loadBrick()
                return True
            else:
                return False

    def loadBrick(self):
        self.motor.run_angle(90, 90)

    def shouldPickUpBrick(self):
        col = self.color.color()
        offset = -1
        if col == Color.BLUE:
            offset = 0
        elif col == Color.RED:
            offset = 2
        elif col == Color.YELLOW:
            offset = 4

        if self.collected[offset] == False:
            self.collected[offset] = True
            return True
        elif self.collected[offset + 1] == False:
            self.collected[offset + 1] = True
            return True
        return False
