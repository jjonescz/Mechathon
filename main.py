#!/usr/bin/env pybricks-micropython

from dependencies import *
from line_follower import LineFollower
from brick_detector import BrickDetector
from planner import Planner
from depo_navigator import DepoNavigator

if __name__ == "__main__":
    print("Initializing")

    lf = LineFollower()
    bd = BrickDetector()
    p = Planner("BD")
    dn = DepoNavigator()
    last_mile = False
    skip_one_turn = False

    lf.left = p.left
    # for i in range(1, 100):
    #     lf.step()

    print("Started")

    while True:

        # Manual control.
        if Button.LEFT in brick.buttons():
            motor = Motor(Port.A, Direction.CLOCKWISE)
            motor.run_angle(360, 90)
        if Button.RIGHT in brick.buttons():
            motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
            motor.run_angle(360, 90)

        # Follow line edge.
        lf.step()

        # Depo arrival.
        if p.state[1] == "D" and len(p.ignorations) == 0:
            print("Depo arrival")
            dn.start()
            dn.go(-2)

        # Detect bricks.
        to_right = False
        brick_picked_up = False
        if p.state[1] in ["D", "L", "R"]:
            if bd.brickAhead():
                brick_picked_up = True

                # Plan destination.
                print("Plan duration", time() - p.start_time)
                p.plan(p.state[1] + bd.result)

                if not dn.visited:
                    # Turn around.
                    lf.turn(1 if p.left else - 1, 250)

                    # Set side.
                    lf.left = p.left

        # Last mile detection.
        elif p.state[1] in ["O", "Y", "B"] and len(p.ignorations) == 1 and not skip_one_turn:
            skip_one_turn = True

        # Depo departure.
        if dn.visited:
            if brick_picked_up:
                print("Depo departure")
                dn.exit()

                # Go on.
                p.plan("D" + bd.result)
                lf.left = p.left
            else:
                break

        # Ignore turns.
        no_more_ignorations = len(p.ignorations) == 0
        if lf.handleTurn(p.ignoreNext()):
            print("Popped...")
            p.popTurn()

            if (no_more_ignorations or p.state[1] == "B") and skip_one_turn:
                print("Last mile for real")
                skip_one_turn = False
                last_mile = True
                lf.completeTurn()

        elif skip_one_turn and lf.isTurn() is not None:
            print("Last mile for real")
            skip_one_turn = False
            last_mile = True
            lf.completeTurn(4)

        # Handle dropoff.
        if last_mile and lf.gradient_drop():
            print("Putting brick down")
            if bd.number == 1:
                bd.putDownBrick1()
                lf.turn(-1, 350)
            else:
                bd.putDownBrick2()
                lf.turn(1, 250)

            # Turn around and go on.
            print("Plan duration", time() - p.start_time)
            p.plan(p.state[1] + bd.nextTruck())
            lf.left = p.left
            lf.completeTurn()
            last_mile = False
            skip_one_turn = False

    print("Finished")
