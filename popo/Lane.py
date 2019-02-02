class Lane:
    def __init__(self, startx, starty, paces, direction):
        self.startx = startx #stored as percentages
        self.starty = starty #stored as percentages
        self.paces = paces
        self.direction = direction
        #direction is a unit vector in xy plane (0,1), (-1,0) etc
    def lane_end(self, swipedist) -> float:
        return self.startx+self.paces*swipedist

    def sub_paces(self) -> None:
        print('paces: ' +str(self.paces))
        self.paces -= 1
    def __str__(self):
        return 'Lane:[startloc: ('+str(self.startx)+', '+str(self.starty)+')|paces: '+\
               str(self.paces)+'|direction: '+str(self.direction)+']'