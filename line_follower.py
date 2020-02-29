from dependencies import *


class LineFollower:

    def __init__(self):
        # Sensors
        self.cs = ColorSensor(Port.S4)

        # Motors
        self.lm = Motor(Port.B)
        self.rm = Motor(Port.D)

        # Parameters
        self.speed = 360  # deg/sec, [-1000, 1000]
        self.dt = 110     # milliseconds
        self.stop_action = Stop.COAST
        self.k = 80

        # PID tuning
        self.Kp = 1  # proportional gain
        self.Ki = 0  # integral gain
        self.Kd = 0.5  # derivative gain

        self.integral = 0
        self.previous_error = 0

        # initial measurement
        self.target_value = 25  # self.cs.reflection()

        self.last_us = [0] * 10

        self.left = True

        print("Target:", self.target_value)

    def step(self):
        current_value = self.cs.reflection()

        # Calculate steering using PID algorithm
        error = self.k * (self.target_value - current_value)
        self.integral += (error * self.dt)
        derivative = (error - self.previous_error) / self.dt
        self.previous_error = error

        # u zero:     on target,  drive forward
        # u positive: too bright, turn right
        # u negative: too dark,   turn left

        u = (self.Kp * error) + (self.Ki * self.integral) + \
            (self.Kd * derivative)

        # print("Current:", current_value, "Target:",
        #       self.target_value, "Speed:", u, end=" ")

        # limit u to safe values: [-1000, 1000] deg/sec
        if self.speed + abs(u) > 1000:
            if u >= 0:
                u = 1000 - self.speed
            else:
                u = self.speed - 1000

        # print("Speed clipped:", u)

        if not self.left:
            u = -u

        self.last_us = self.last_us[1:]
        self.last_us.append(u)

        # print("Sum of 10:", sum(self.last_us))

        # run motors
        self.lm.run_time(self.speed - u, self.dt, self.stop_action, False)
        self.rm.run_time(self.speed + u, self.dt, self.stop_action)

    def turn(self, dir=1):
        """
        Turns robot 350 degrees. Clockwise for dir=1, counterclockwise for dir=-1.
        """
        a = 200
        self.lm.run_angle(360, dir * a, Stop.COAST, False)
        self.rm.run_angle(360, -1 * dir * a)

    def isTurn(self):
        sum_us = sum(self.last_us)
        treshold = 5000
        if sum_us > treshold:
            return "left"
        elif sum_us < -treshold:
            return "right"
        return None

    def ignoreTurn(self):
        turn = self.isTurn()
        step_delay = 30
        if turn == "left":
            turn_dir = 1
            turn_after = step_delay
        elif turn == "right":
            turn_dir = -1
            turn_after = step_delay
        else:
            return

        while turn_after > 0:
            self.step()
            turn_after -= 1
            if turn_after == 0:
                self.turn(turn_dir)

        step_after_turn = 30
        while step_after_turn > 0:
            self.step()
            step_after_turn -= 1
