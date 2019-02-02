class Box:
    def __init__(self, north, east, south, west):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
    def getnorth(self):
        return self.north
    def geteast(self):
        return self.east
    def getsouth(self):
        return self.south
    def getwest(self):
        return self.west
