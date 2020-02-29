from dependencies import *


class BrickDetector:

    def __init__(self):
        self.color = None
        self.motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        self.motor.reset_angle(0)
        self.lm = lm
        self.rm = rm

        self.color = cs
        self.us = UltrasonicSensor(Port.S2)

        self.dist_to_brick = 60

        # bricks to collect [B,B,R,R,Y,Y]
        self.collected = [False] * 6

    def claws(self, target):
        self.motor.run_angle(720, target - self.motor.angle())

    def go(self, target):
        self.lm.run_angle(180, target - self.lm.angle(), Stop.COAST, False)
        self.rm.run_angle(180, target - self.rm.angle())

    def brickAhead(self):
        """
        Returns True if brick was loaded on robot, else False
        """
        self.lm.reset_angle(0)
        self.rm.reset_angle(0)
        # closer than 15 cm means brick ahead
        if self.us.distance() < 45:
            print("Brick detected")
            self.claws(1980)
            self.go(self.dist_to_brick - 20)
            if self.shouldPickUpBrick():
                self.loadBrick()
                print("Loaded")
                return True
            else:
                self.ignoreBrick()
                print("Ignored")
                return True

    def loadBrick(self):
        self.go(0)
        self.claws(500)
        self.go(self.dist_to_brick)
        self.claws(0)
        self.go(0)

    def ignoreBrick(self):
        self.go(0)
        self.claws(0)

    def shouldPickUpBrick(self):
        (r, g, b) = self.color.rgb()
        sleep(1)
        (r, g, b) = self.color.rgb()

        print("Found color:", r, g, b)
        offset = 0
        # if col == Color.BLUE:
        #     offset = 0
        # elif col == Color.RED:
        #     offset = 2
        # elif col == Color.YELLOW:
        #     offset = 4

        if self.collected[offset] == False:
            self.collected[offset] = True
            return True
        elif self.collected[offset + 1] == False:
            self.collected[offset + 1] = True
            return True
        return False
