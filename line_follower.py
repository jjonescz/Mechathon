import dependencies


class LineFollower:
    # Constructor
    def __init__(self):
        self.shut_down = False

    # Main method
    def run(self):

        # sensors
        cs = ColorSensor(Port.S4)

        # motors
        lm = Motor(Port.A)
        rm = Motor(Port.D)

        speed = 1000  # deg/sec, [-1000, 1000]
        dt = 500       # milliseconds
        stop_action = Stop.COAST

        # PID tuning
        Kp = 1  # proportional gain
        Ki = 0  # integral gain
        Kd = 0  # derivative gain

        integral = 0
        previous_error = 0

        # initial measurement
        target_value = cs.reflection()

        # Start the main loop
        while not self.shut_down:

            # Calculate steering using PID algorithm
            error = target_value - cs.reflection()
            integral += (error * dt)
            derivative = (error - previous_error) / dt

            # u zero:     on target,  drive forward
            # u positive: too bright, turn right
            # u negative: too dark,   turn left

            u = (Kp * error) + (Ki * integral) + (Kd * derivative)

            # limit u to safe values: [-1000, 1000] deg/sec
            if speed + abs(u) > 1000:
                if u >= 0:
                    u = 1000 - speed
                else:
                    u = speed - 1000

            # run motors
            if u >= 0:
                lm.run_time(speed + u, dt, stop_action)
                rm.run_time(speed - u, dt, stop_action)
                sleep(dt / 1000)
            else:
                lm.run_time(speed - u, dt, stop_action)
                rm.run_time(speed + u, dt, stop_action)
                sleep(dt / 1000)

            previous_error = error

            # Check if buttons pressed (for pause or stop)
            if Button.DOWN in brick.buttons():  # Stop
                print("Exit program... ")
                self.shut_down = True
