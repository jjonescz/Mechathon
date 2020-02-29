from dependencies import *


class Planner:
    """
    L: left truck
    R: right truck
    O, Y, B: colors
    S: start
    D: depo
    """

    def __init__(self):
        self.plan("SL")

    def plan(self, target):
        self.state = target
        if self.state == "SL":
            self.left = True
            self.ignorations = [False, False]
        elif self.state == "SR":
            self.left = False
            self.ignorations = [False, False]
        elif self.state == "LB":
            self.left = True
            self.ignorations = [False, True, True]
        elif self.state == "LY":
            self.left = True
            self.ignorations = [False, True, False]
        elif self.state == "LO":
            self.left = True
            self.ignorations = [False, False]
        elif self.state == "RB":
            self.left = False
            self.ignorations = [True]
        elif self.state == "RY":
            self.left = True
            self.ignorations = [True, True, False]
        elif self.state == "RO":
            self.left = True
            self.ignorations = [True, False]
        elif self.state == "BR":
            self.left = True
            self.ignorations = [True]
        elif self.state == "YR":
            self.left = False
            self.ignorations = [False, True, True]
        elif self.state == "OR":
            self.left = False
            self.ignorations = [False, True]
        elif self.state == "BL":
            self.left = False
            self.ignorations = [True, True, False]
        elif self.state == "YL":
            self.left = False
            self.ignorations = [False, True, False]
        elif self.state == "OL":
            self.left = False
            self.ignorations = [False, False]
        elif self.state == "DB":
            self.left = False
            self.ignorations = [False]
        elif self.state == "DY":
            self.left = True
            self.ignorations = [True, True, False]
        elif self.state == "DO":
            self.left = True
            self.ignorations = [True, False]
        elif self.state == "BD":
            self.left = True
            self.ignorations = [False]
        elif self.state == "YD":
            self.left = True
            self.ignorations = [True, False]
        elif self.state == "OD":
            self.left = True
            self.ignorations = [True, False]
