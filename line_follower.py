from dependencies import *


class LineFollower:

    def __init__(self):
        # Sensors
        self.cs = ColorSensor(Port.S3)

        # Motors
        self.lm = Motor(Port.A)
        self.rm = Motor(Port.D)

        # Parameters
        self.speed = 90  # deg/sec, [-1000, 1000]
        self.dt = 100     # milliseconds
        self.stop_action = Stop.COAST
        self.k = 20

        # PID tuning
        self.Kp = 1  # proportional gain
        self.Ki = 0  # integral gain
        self.Kd = 0.5  # derivative gain

        self.integral = 0
        self.previous_error = 0

        # initial measurement
        self.target_value = self.cs.reflection()

        print("Target:", self.target_value)

    def step(self, left=True):
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

        if not left:
            u = -u

        # run motors
        self.lm.run_time(self.speed - u, self.dt, self.stop_action, False)
        self.rm.run_time(self.speed + u, self.dt, self.stop_action, False)
        sleep(self.dt / 1000)
