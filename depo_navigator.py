from dependencies import *


class DepoNavigator:

    def __init__(self):
        self.lm = lm
        self.rm = rm
        self.visited = False

    def start(self):
        self.lm.run_angle(180, -50, Stop.COAST, False)
        self.rm.run_angle(180, -25)
        self.visited = True

    def go(self, i):
        """
        i = -2, -1, 1, 2
        """

        # Turn.
        s = 1 if i > 0 else -1
        self.lm.run_angle(180, s * 170, Stop.COAST, False)
        self.rm.run_angle(180, s * -170)

        # Go forward.
        v = abs(s)
        self.lm.run_angle(180, 200 * v, Stop.COAST, False)
        self.rm.run_angle(180, 200 * v)

        # Turn back.
        self.lm.run_angle(180, s * -170, Stop.COAST, False)
        self.rm.run_angle(180, s * 170)

        # Go towards brick.
        self.lm.run_angle(180, 10, Stop.COAST, False)
        self.rm.run_angle(180, 10)

    def exit(self):
        # Go back to line.
        self.lm.run_angle(180, -200, Stop.COAST, False)
        self.rm.run_angle(180, -200)

        # Turn left.
        self.lm.run_angle(180, -170, Stop.COAST, False)
        self.rm.run_angle(180, 170)

        self.visited = False
