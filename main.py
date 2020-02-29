#!/usr/bin/env pybricks-micropython

from dependencies import *
from line_follower import LineFollower

if __name__ == "__main__":
    lf = LineFollower()

    while Button.DOWN not in brick.buttons():
        sleep(lf.step())

    print("Finished")
