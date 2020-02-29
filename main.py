#!/usr/bin/env pybricks-micropython

from dependencies import *
from line_follower import LineFollower
from brick_detector import BrickDetector

if __name__ == "__main__":
    print("Initializing")

    # d = None
    # while True:
    #     if Button.LEFT in brick.buttons():
    #         d = Direction.CLOCKWISE
    #     if Button.RIGHT in brick.buttons():
    #         d = Direction.COUNTERCLOCKWISE
    #     if Button.CENTER in brick.buttons():
    #         d = None
    #     if d is not None:
    #         motor = Motor(Port.A, d)
    #         motor.run_angle(360, 180)

    lf = LineFollower()
    #bd = BrickDetector()

    print("Started")

    left = True

    while Button.DOWN not in brick.buttons():
        if Button.LEFT in brick.buttons():
            if not left:
                print("-> left")
            left = True
        if Button.RIGHT in brick.buttons():
            if left:
                print("-> right")
            left = False

        lf.step(left)
        # bd.brickAhead()
        pass

    print("Finished")
