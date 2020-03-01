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

        self.number = 1

        # bricks to collect [B,B,R,R,Y,Y]
        self.collected = [False] * 6

    def claws(self, target):
        self.motor.run_angle(720, target - self.motor.angle())

    def go(self, target):
        self.lm.run_angle(180, target - self.lm.angle(), Stop.COAST, False)
        self.rm.run_angle(180, target - self.rm.angle())

    def turn(self, target):
        self.lm.run_angle(90, target - self.lm.angle(), Stop.COAST, False)
        self.rm.run_angle(90, -target - self.rm.angle())

    def brickAhead(self, force=False):
        """
        Returns True if any brick was detected.
        """
        # closer than 15 cm means brick ahead
        if force or self.us.distance() < 50:
            print("Brick detected")
            self.lm.reset_angle(0)
            self.rm.reset_angle(0)
            self.claws(1980)
            self.go(self.dist_to_brick - 20)
            if self.shouldPickUpBrick():
                self.loadBrick()
                return True
            else:
                self.ignoreBrick()
                return False

        return False

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
            self.result = "O"
        else:
            offset = 4  # yellow
            self.result = "Y"

        print("Found color:", r, g, b, self.result)

        if self.collected[offset] == False:
            self.collected[offset] = True
            self.number = 1
            return True
        elif self.collected[offset + 1] == False:
            self.collected[offset + 1] = True
            self.number = 2
            return True
        self.number = 2
        return False

    def putDownBrick1(self):
        # Blue target is detected too late. Compensate.
        x = 0
        if self.result == "B":
            self.lm.reset_angle(0)
            self.rm.reset_angle(0)
            self.go(-40)
            x = 10

        # Turn left
        self.lm.reset_angle(0)
        self.rm.reset_angle(0)
        self.turn(-35 + x)

        # Drop.
        self.claws(1980)

        # Turn right.
        self.turn(0)

        # Go back.
        self.lm.reset_angle(0)
        self.rm.reset_angle(0)
        self.go(-120)

        # Reset claws.
        self.claws(0)

    def putDownBrick2(self):
        # Stop.
        self.lm.reset_angle(0)
        self.rm.reset_angle(0)
        self.turn(0)

        # Drop.
        self.claws(500)

        # Go back.
        self.lm.reset_angle(0)
        self.rm.reset_angle(0)
        self.go(-120)

        # Reset claws.
        self.claws(0)

    def nextTruck(self):
        c = sum(self.collected)
        if c < 2:
            return "L"
        if c < 4:
            return "R"
        if c < 6:
            return "D"
        return "E"

    def finish(self):
        self.lm.reset_angle(0)
        self.rm.reset_angle(0)
        self.go(0)
        for i in range(27):
            self.claws(500)
            self.claws(0)
            if Button.CENTER in brick.buttons():
                break
