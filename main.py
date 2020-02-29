#!/usr/bin/env pybricks-micropython

from dependencies import *
from line_follower import LineFollower
from brick_detector import BrickDetector

if __name__ == "__main__":
    print("Initializing")

    lf = LineFollower()
    #bd = BrickDetector()

    print("Started")

    while Button.DOWN not in brick.buttons():
        lf.step()
        # bd.brickAhead()

    print("Finished")
