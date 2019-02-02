import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import math
import popo.Lane as ln
import config.SystemVars
class MapManager:
    SV = config.SystemVars.SystemVars()
    def __init__(self, tilelevel, mirror):
        #mirror = 0 no mirroring (only the safe half)
        #mirror = 1 full mirroring (both halves of map)
        #mirror = 2 custom mirroring (DOA/SNS/MFA + former PHX land)
        self.shortradius = 100
        self.longradius = 200

    @staticmethod
    def flip_vector(x, y):
        return -x, -y

    @staticmethod
    def screen_system_convert(x, y):
        return x, -y

    @staticmethod
    def angle_to_unit_vector(angle):
        rad = math.radians(angle)
        vx = math.cos(rad)
        vy = math.sin(rad)
        return vx,-vy

    def default_direction(self):
        return self.angle_to_unit_vector(SV.getmapangle())

    def get_lane_paces(self, unitlength):
        return unitlength/SV.getswipedistance()
    def get_lane_count(self, unitrange):
        return unitrange/SV.getswipeheight()

    def diamond_box(self):
        print('creating diamond box')
        lanelist = []

        direction = self.default_direction()
        sixbox = SV.getlvl6box()
        fivebox = SV.getlvl5box()

        eastcorner = fivebox.geteast()
        fiveendx = eastcorner[0]
        fivestarty = eastcorner[1]
        print(str(eastcorner))

        westcorner = fivebox.getwest()
        fivestartx = westcorner[0]
        fiveendy = westcorner[1]
        print(str(westcorner))


        fiveboxlen = fiveendx - fivestartx
        fiveboxpaces = self.get_lane_paces(fiveboxlen)

        swipeheight = SV.getswipeheight()

        sixboxeast = sixbox.geteast()
        sixendx = sixboxeast[0]
        sixstarty = sixboxeast[1]

        sixboxwest = sixbox.getwest()
        sixstartx = sixboxwest[0]
        sixendy = sixboxwest[1]

        print('five')
        print('start: ' + str(fivestarty) +' end: ' + str(fiveendy))
        print('six')
        print('start: ' + str(sixstarty) + ' end: ' + str(sixendy))
        for i in range(fivestarty, fiveendy, swipeheight):
            #note that this goes from south to north
            yval = i
            if(yval > sixstarty) and (yval < sixendy):
                halfrange = self.get_lane_paces(sixstartx-fivestartx)
                lanelist.append(ln.Lane(fivestartx, yval, halfrange, direction))
                lanelist.append(ln.Lane(sixendy, yval, halfrange, direction))
            else:
                lanelist.append(ln.Lane(fivestartx, yval, fiveboxpaces, direction))
        print(lanelist)
        for lane in lanelist:
            print(str(lane))
        return lanelist

    #erases areas that cross identity line
    def diamond_scan(self):
        print('starting diamond scan')
        swipedist = SV.getswipedistance()
        lanelist = self.diamond_box()
        print(lanelist)
        for lane in lanelist:
            endx = lane.lane_end(swipedist)-swipedist
            print('endx: '+str(endx))
            starty = lane.starty
            if(lane.startx-swipedist)>starty:
                lanelist.remove(lane)
                continue
            while(endx>starty):
                lane.sub_paces()
                endx = lane.lane_end(swipedist)-swipedist
            print(str(lane))
        return lanelist




    def generate_lanes(self, mode):
        lanelist = []
        if(mode == 3):
            lanelist = self.diamond_scan()
        #mode == 1 -> spiral from top
        #mode == 2 -> order by longest lanes
        #some math here (create some Lane objects)
        #make sure to alternate start & finish so we weave back and forth (actually it doesn't matter)
        return lanelist
