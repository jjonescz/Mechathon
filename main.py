#!/usr/bin/env pybricks-micropython

from dependencies import *
from line_follower import LineFollower
from brick_detector import BrickDetector
from planner import Planner

if __name__ == "__main__":
    print("Initializing")

    lf = LineFollower()
    bd = BrickDetector()
    p = Planner("LO")
    last_mile = False
    skip_one_turn = False

    # lf.left = p.left
    # for i in range(1, 100):
    #     lf.step()

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

        # Detect bricks.
        to_right = False
        if p.state[1] in ["D", "L", "R"]:
            if bd.brickAhead():
                # Plan destination.
                p.plan(p.state[1] + bd.result)

                # Turn around.
                lf.turn(1 if p.left else - 1, p.left)
        # Last mile detection.
        elif p.state[1] in ["O", "Y", "B"] and len(p.ignorations) == 1 and not last_mile:
            to_right = bd.number == 2
            skip_one_turn = p.state[1] != "B"
            last_mile = not skip_one_turn
            if last_mile:
                print("Last mile")

        # Ignore turns.
        if lf.handleTurn(p.ignoreNext(), to_right):
            print("Popped...")
            p.popTurn()
        elif skip_one_turn and lf.isTurn() is not None:
            print("Last mile for real")
            skip_one_turn = False
            last_mile = True

        # Handle dropoff.
        if last_mile and lf.gradient_drop():
            print("Putting brick down")
            if bd.number == 1:
                bd.putDownBrick1()
            else:
                bd.putDownBrick2()
            break

    print("Finished")
