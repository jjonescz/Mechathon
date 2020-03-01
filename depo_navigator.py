from dependencies import *


class DepoNavigator:

    def __init__(self):
        self.lm = lm
        self.rm = rm
        self.side = -1
        self.offset = 2
        self.c = 0
        self.k = 70

    def start(self):
        self.lm.run_angle(180, -50, Stop.COAST, False)
        self.rm.run_angle(180, -25)
        self.offset = 2

    def search(self):
        self.go(self.offset * self.side)
        self.offset = 1
        self.side *= - 1
        self.c = -self.k

    def go(self, i):
        """
        i = -2, -1, 1, 2
        """

        print("Depo: go to", i)

        # Turn.
        s = 1 if i > 0 else -1
        self.lm.run_angle(180, s * 170, Stop.COAST, False)
        self.rm.run_angle(180, s * -170)

        # Go forward.
        v = abs(s)
        self.lm.run_angle(180, 200 * v + self.c, Stop.COAST, False)
        self.rm.run_angle(180, 200 * v + self.c)

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

        self.side = 1
        self.c = self.k
