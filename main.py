#!/usr/bin/env pybricks-micropython

from dependencies import *
from line_follower import LineFollower
from brick_detector import BrickDetector

if __name__ == "__main__":
    print("Initializing")

    # while True:
    #     if Button.LEFT in brick.buttons():
    #         d = Direction.CLOCKWISE
    #     if Button.RIGHT in brick.buttons():
    #         d = Direction.COUNTERCLOCKWISE
    #     motor = Motor(Port.A, Direction.CLOCKWISE)
    #     motor.run_angle(360, 180)

    lf = LineFollower()
    #bd = BrickDetector()

    print("Started")

    while Button.DOWN not in brick.buttons():
        lf.step()
        # bd.brickAhead()

    print("Finished")
