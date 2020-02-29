#!/usr/bin/env pybricks-micropython

from dependencies import *
from line_follower import LineFollower
from brick_detector import BrickDetector
from planner import Planner

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
    #         motor.run_angle(360, 90)

    lf = LineFollower()
    #bd = BrickDetector()
    p = Planner("SL")

    print("Started")

    while True:
        lf.left = p.left

        # Follow line edge.
        lf.step()

        # Ignore turns.
        if lf.handleTurn(p.ignoreNext()):
            p.popTurn()

        # bd.brickAhead()

    print("Finished")
