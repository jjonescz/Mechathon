from dependencies import *


class DepoNavigator:

    def __init__(self):
        self.lm = lm
        self.rm = rm

    def start(self):
        self.lm.run_angle(180, -50, Stop.COAST, False)
        self.rm.run_angle(180, -25)
        pass
