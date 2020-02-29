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

    turn_dir = 0
    turn_after = 0
    left = True

    while Button.DOWN not in brick.buttons():
        if Button.LEFT in brick.buttons():
            if not left:
                print("-> left")
            left = True
            # lf.turn(-1)
        if Button.RIGHT in brick.buttons():
            if left:
                print("-> right")
            left = False
            # lf.turn(1)

        # Follow line edge
        lf.step(left)

        # Ignore turns
        turn = lf.isTurn()
        step_delay = 30
        if turn == "left":
            turn_dir = 1
            turn_after = step_delay
        elif turn == "right":
            turn_dir = -1
            turn_after = step_delay

        if turn_after > 0:
            turn_after = turn_after - 1
            if turn_after == 0:
                lf.turn(turn_dir)

        # bd.brickAhead()
        pass

    print("Finished")
