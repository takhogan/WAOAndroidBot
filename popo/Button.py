import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import util.MapNavigator as MN
class Button:
    def __init__(self, detector, accessor):
        self.detector = detector
        self.accessor = accessor
    def detect(self):
        if(self.detector == None):
            return False
        return self.detector()
    def access(self):
        return self.accessor()
    def waitforbuttonload(self, timeout = 20, ontimeout = None):
        while (not self.detect()):
            if (timeout > 0):
                MN.robot_sleep(250)
                timeout -= 0.25
                if (timeout % 4 == 0):
                    print('waiting for button load... ' + str(timeout))
            else:
                print('button timed out!')
                if(ontimeout != None):
                    ontimeout()
    def click(self):
        return self.accessor()
    def __str__(self):
        return '(detector: ' + str(self.detector) +', accessor: ' + str(self.accessor) +')'