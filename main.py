#!/usr/bin/env pybricks-micropython

from dependencies import *
from line_follower import LineFollower
from brick_detector import BrickDetector

if __name__ == "__main__":
    lf = LineFollower()
    bd = BrickDetector()

    print("Started")

    while Button.DOWN not in brick.buttons():
        sleep(lf.step())
        bd.brickAhead()

    print("Finished")
