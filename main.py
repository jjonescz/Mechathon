#!/usr/bin/env pybricks-micropython

from dependencies import *
from line_follower import LineFollower
from brick_detector import BrickDetector
from planner import Planner

if __name__ == "__main__":
    print("Initializing")

    lf = LineFollower()
    bd = BrickDetector()
    p = Planner("SL")

    print("Started")

    while True:
        lf.left = p.left

        # Manual control.
        if Button.LEFT in brick.buttons():
            motor = Motor(Port.A, Direction.CLOCKWISE)
            motor.run_angle(360, 90)
        if Button.RIGHT in brick.buttons():
            motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
            motor.run_angle(360, 90)

        # Follow line edge.
        lf.step()

        # Ignore turns.
        if lf.handleTurn(p.ignoreNext()):
            p.popTurn()

        # Detect bricks.
        b = bd.brickAhead()
        if b is None:
            continue

        # Plan destination.
        p.plan(p.state[1] + b)

        # Turn around.
        lf.turn(1 if lf.left else -1)

    print("Finished")
