import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import popo.Box as box

class SystemVars:
    #configured for vysor by default
    def __init__(self):
        self.isMac = False

        self.screenwidth = 800
        self.screenheight = 1280
        self.screenx = 880
        self.screeny = 142
        self.xscrolldist = 0
        self.yscrolldist = 0
        self.mapangle_zoomedin = 35
        self.mapangle_zoomedout = 37.5
        self.lvl5_north = (700, 700)
        self.lvl5_east = (700, 500)
        self.lvl5_south = (500, 500)
        self.lvl5_west = (500, 700)
        self.lvl6_north = (626, 626)
        self.lvl6_east = (626, 574)
        self.lvl6_south = (574, 574)
        self.lvl6_west = (574, 626)
        self.center = (600, 600)
        self.north_edge = (1199, 1199)
        self.east_edge = (1199, 0)
        self.south_edge = (0, 0)
        self.west_edge = (0, 1199)

        self.swipedistance = 8  # move about 8 units with each swipe
        self.swipeheight = 10  # cover about 10 vertical units


    def getxscroll(self):
        return self.xscrolldist
    def getyscroll(self):
        return self.yscrolldist

    def getxwidth(self):
        return self.screenwidth
    def getscreenwidth(self):
        return self.getxwidth()
    def setxwidth(self, newwidth):
        self.screenwidth = newwidth

    def getyheight(self):
        return self.screenheight
    def getscreenheight(self):
        return self.getyheight()
    def setyheight(self, newheight):
        self.screenheight = newheight

    def getscreenx(self):
        return self.screenx
    def setscreenx(self, newscreenx):
        self.screenx = newscreenx

    def getscreeny(self):
        return self.screeny
    def setscreeny(self, newscreeny):
        self.screeny = newscreeny

    def getmapangle(self):
        return self.mapangle_zoomedin
    def getswipedistance(self):
        return self.swipedistance
    def getswipeheight(self):
        return self.swipeheight
    def getlvl5box(self):
        return box.Box(self.lvl5_north, self.lvl5_east, self.lvl5_south, self.lvl5_west)
    def getlvl6box(self):
        return box.Box(self.lvl6_north, self.lvl6_east, self.lvl6_south, self.lvl6_west)
    def getIsMac(self):
        return self.isMac
