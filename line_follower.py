from dependencies import *


class LineFollower:

    def __init__(self):
        # Sensors
        self.cs = ColorSensor(Port.S3)

        # Motors
        self.lm = Motor(Port.A)
        self.rm = Motor(Port.D)

        # Parameters
        self.speed = 360/4  # deg/sec, [-1000, 1000]
        self.dt = 500      # milliseconds
        self.stop_action = Stop.COAST

        # PID tuning
        self.Kp = 1  # proportional gain
        self.Ki = 0  # integral gain
        self.Kd = 0  # derivative gain

        self.integral = 0
        self.previous_error = 0

        # initial measurement
        self.target_value = self.cs.reflection()

    def step(self):
        """
        Returns time to sleep in seconds.
        """

        # Calculate steering using PID algorithm
        error = self.target_value - self.cs.reflection()
        self.integral += (error * self.dt)
        derivative = (error - self.previous_error) / self.dt
        self.previous_error = error

        # u zero:     on target,  drive forward
        # u positive: too bright, turn right
        # u negative: too dark,   turn left

        u = (self.Kp * error) + (self.Ki * self.integral) + \
            (self.Kd * derivative)

        # limit u to safe values: [-1000, 1000] deg/sec
        if self.speed + abs(u) > 1000:
            if u >= 0:
                u = 1000 - self.speed
            else:
                u = self.speed - 1000

        # run motors
        if u >= 0:
            self.lm.run_time(self.speed + u, self.dt, self.stop_action)
            self.rm.run_time(self.speed - u, self.dt, self.stop_action)
            return self.dt / 1000
        else:
            self.lm.run_time(self.speed - u, self.dt, self.stop_action)
            self.rm.run_time(self.speed + u, self.dt, self.stop_action)
            return self.dt / 1000
