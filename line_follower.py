from dependencies import *
from simple_pid import PID


class LineFollower:

    def __init__(self):
        # Sensors
        self.cs = cs

        # Motors
        self.lm = lm
        self.rm = rm

        # Parameters
        self.speed = 90  # deg/sec, [-1000, 1000]

        # initial measurement
        self.target_value = 25  # self.cs.reflection()

        # PID tuning
        self.Kp = 8  # proportional gain
        self.Ki = 0.005  # integral gain
        self.Kd = 0.1  # derivative gain
        self.pid = PID(self.Kp, self.Ki, self.Kd,
                       setpoint=self.target_value)
        self.pid.output_limits = (-1000, 1000)

        # Turn detection
        self.last_us = [0] * 10

        # Gradient detection
        self.last_vals = []

        self.left = True

        print("Target:", self.target_value)

    def step(self):
        value = self.cs.reflection()
        if len(self.last_vals) == 10:
            self.last_vals = self.last_vals[1:]
        self.last_vals.append(value)

        u = self.pid(value)
        if not self.left:
            u = -u

        self.last_us = self.last_us[1:]
        self.last_us.append(u)

        # print("u:", u)

        # run motors
        self.lm.run(self.speed - u)
        self.rm.run(self.speed + u)

    def turn(self, dir, a=120):
        """
        Turns robot 360 degrees. Clockwise for dir=1, counterclockwise for dir=-1.
        """
        print("Turning", dir, "a=", a)
        self.lm.run_angle(360, dir * a, Stop.COAST, False)
        self.rm.run_angle(360, -dir * a)

    def isTurn(self):
        sum_us = sum(self.last_us)
        treshold = 700
        if sum_us > treshold:
            return "left"
        elif sum_us < -treshold:
            return "right"
        return None

    def handleTurn(self, ignore):
        turn = self.isTurn()
        step_delay = 5
        if turn == "left" and self.left:
            turn_dir = 1
            turn_after = step_delay
        elif turn == "right" and not self.left:
            turn_dir = -1
            turn_after = step_delay
        else:
            return False

        print("Turn detected:", turn)

        # Don't ignore, just detect the turn.
        if not ignore:
            print("Helping turn")
            a = 100
            self.lm.run_angle(360, -turn_dir * a, Stop.COAST, False)
            self.rm.run_angle(360, turn_dir * a)
            self.completeTurn()
            return True

        print("Ignoring...", end=" ")

        while turn_after > 0:
            self.step()
            turn_after -= 1
            if turn_after == 0:
                self.turn(turn_dir, 120)

        # Complete the turn.
        self.completeTurn()

        print("done")

        return True

    def completeTurn(self, wait=4):
        time_to_complete = time() + wait
        while time() < time_to_complete:
            self.step()
        print("completed")

    def gradient(self):
        if len(self.last_vals) < 10 or self.last_vals[-1] == 0:
            return 1
        return mean(self.last_vals[:-1]) / self.last_vals[-1]

    def gradient_drop(self):
        g = self.gradient()
        return g < 0.9 or g > 1.5
