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
        Returns color of loaded brick or None.
        """
        # closer than 15 cm means brick ahead
        if self.us.distance() < 45:
            print("Brick detected")
            self.lm.reset_angle(0)
            self.rm.reset_angle(0)
            self.claws(1980)
            self.go(self.dist_to_brick - 20)
            if self.shouldPickUpBrick():
                self.loadBrick()
                return self.result
            else:
                self.ignoreBrick()
                return "D"

        return None

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

        if r == 0 or b/r > 3:
            offset = 0  # blue
            self.result = "B"
        elif g == 0 or r/g > 3:
            offset = 2  # red
            self.result = "R"
        else:
            offset = 4  # yellow
            self.result = "Y"

        print("Found color:", r, g, b, self.result)

        if self.collected[offset] == False:
            self.collected[offset] = True
            return True
        elif self.collected[offset + 1] == False:
            self.collected[offset + 1] = True
            return True
        return False
