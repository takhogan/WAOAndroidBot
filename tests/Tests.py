import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import util.MapNavigator as MN
import util.MapManager as MM
import config.SystemVars
import popo.Color as C

SV = config.SystemVars.SystemVars()

def test_map_navigator():
    print('Map Navigator Test')
    MN.open_airdroid()
    MN.init_screen()
    MN.open_map()
def test_map_manager():
    print('Map Manager Test:')
    mm = MM.MapManager(5, True, SV)
    mm.generate_lanes(3)

def test_wait_functions():
    # print(test_one(True, False))
    # print(test_one(False, False))
    # print(test_one(True, True))
    # print(test_mult(True, False))
    # print(test_mult(False, False))
    # print(test_mult(True, True))
    while (not MN.color_comp(1.5823863636363635, -0.10828025477707007, C.Color(90, 92, 94))) or \
            (not MN.color_comp(-0.42329545454545453, 0.09394904458598727, C.Color(255, 255, 255))) or \
            (not MN.color_comp(0.5965909090909091, 0.2786624203821656, C.Color(43, 43, 43))):
        MN.robot_sleep(250)


if __name__ == '__main__':
    test_wait_functions()