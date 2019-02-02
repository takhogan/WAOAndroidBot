def wait_mailbutton():
    timeout = 20
    while (not color_comp(0.59875, 0.94296875, C.Color(217, 211, 197))) or \
    (not color_comp(0.5825, 0.953125, C.Color(209, 201, 176))) or \
    (not color_comp(0.58625, 0.97578125, C.Color(189, 174, 148))) or \
    (not color_comp(0.65, 0.9703125, C.Color(191, 175, 150))) or \
    (not color_comp(0.61875, 0.95625, C.Color(132, 62, 62))):
        if(timeout>0):
            robot_sleep(250)
            timeout-=0.25


def click_mailbutton():
    click_screen_area(0.57875, 0.95078125, 0.6525, 0.978125)


def wait_alliancestatusmail():
    timeout = 20
    while (not color_comp(0.09125, 0.50703125, C.Color(16, 112, 189))) or \
    (not color_comp(0.1575, 0.50859375, C.Color(192, 90, 16))) or \
    (not color_comp(0.18, 0.515625, C.Color(175, 152, 120))) or \
    (not color_comp(0.165, 0.53046875, C.Color(253, 245, 220))) or \
    (not color_comp(0.14625, 0.5515625, C.Color(192, 164, 118))) or \
    (not color_comp(0.0875, 0.4859375, C.Color(178, 155, 123))) or \
    (not color_comp(0.585, 0.48984375, C.Color(217, 191, 147))):
        if(timeout>0):
            robot_sleep(250)
            timeout-=0.25


def click_alliancestatusmail():
    click_screen_area(0.045, 0.47734375, 0.945, 0.58125)


def wait_unreadmail():
    timeout = 20
    while (not color_comp(0.1175, 0.13828125, C.Color(124, 60, 60))) or \
    (not color_comp(0.10625, 0.12734375, C.Color(217, 212, 199))) or \
    (not color_comp(0.07875, 0.13828125, C.Color(194, 185, 152))) or \
    (not color_comp(0.0925, 0.159375, C.Color(191, 178, 150))) or \
    (not color_comp(0.155, 0.14921875, C.Color(198, 185, 160))) or \
    (not color_comp(0.1125, 0.1109375, C.Color(180, 162, 134))) or \
    (not color_comp(0.625, 0.11015625, C.Color(219, 198, 161))):
        if(timeout>0):
            robot_sleep(250)
            timeout-=0.25


def click_unreadmail():
    click_screen_area(0.05, 0.103125, 0.9325, 0.19609375)


def wait_mailload():
    timeout = 20
    while (not color_comp(0.215, 0.03359375, C.Color(1, 1, 1))) or \
    (not color_comp(0.34125, 0.028125, C.Color(102, 26, 22))) or \
    (not color_comp(0.65875, 0.02734375, C.Color(105, 27, 22))) or \
    (not color_comp(0.8025, 0.0296875, C.Color(8, 8, 8))) or \
    (not color_comp(0.725, 0.1125, C.Color(210, 185, 142))) or \
    (not color_comp(0.2025, 0.525, C.Color(210, 185, 142))) or \
    (not color_comp(0.81125, 0.8453125, C.Color(210, 186, 142))):
        if(timeout>0):
            robot_sleep(250)
            timeout-=0.25


def click_getmailreward():
    click_screen_area(0.37875, 0.91640625, 0.61875, 0.953125)


def wait_mailrewarddisplay():
    timeout = 20
    while (not color_comp(0.17375, 0.29453125, C.Color(199, 172, 123))) or \
    (not color_comp(0.82875, 0.2921875, C.Color(196, 170, 121))) or \
    (not color_comp(0.645, 0.30859375, C.Color(142, 7, 6))) or \
    (not color_comp(0.32875, 0.275, C.Color(78, 1, 0))) or \
    (not color_comp(0.74875, 0.48046875, C.Color(166, 133, 84))):
        if(timeout>0):
            robot_sleep(250)
            timeout-=0.25


def click_escapemailreward():
    click_screen_area(0.09125, 0.5859375, 0.915, 0.91953125)


def wait_maildeletebutton():
    timeout = 20
    while (not color_comp(0.925, 0.0171875, C.Color(232, 198, 130))) or \
    (not color_comp(0.9175, 0.05, C.Color(146, 113, 55))) or \
    (not color_comp(0.9675, 0.03671875, C.Color(24, 27, 28))):
        if(timeout>0):
            robot_sleep(250)
            timeout-=0.25

def click_maildelete():
    click_screen_area(0.90625, 0.0203125, 0.93625, 0.046875)

def quick_mailclearscript():
    wait_mailbutton()
    click_mailbutton()
    wait_alliancestatusmail()
    click_alliancestatusmail()
    while True:
        wait_unreadmail()
        click_unreadmail()
        wait_mailload()
        click_getmailreward()
        wait_mailrewarddisplay()
        click_escapemailreward()
        wait_maildeletebutton()
        click_maildelete()



def click_tile_gather(cx, cy):
    click_screen_area(0.18 + cx, -0.062200956937799035 + cy, 0.24571428571428572 + cx, -0.02870813397129185 + cy)

def click_tile_check(cx,cy):
    click_screen_area(-0.2485714285714286 + cx, -0.06379585326953746 + cy, -0.17714285714285716 + cx,
                      -0.027113237639553422 + cy)

def click_close_ad():
    click_screen_loc(0.04871794871794872, 0.02745664739884393)
    robot_sleep(1000)

def click_safe_area_north():
    click_screen_area(0.6846590909090909, 0.054140127388535034, 0.7528409090909091, 0.0875796178343949)

def click_safe_area_south():
    click_screen_area(0.5575, 0.82734375, 0.87875, 0.87109375)

def click_map_button():
    double_click_screen_area(0.05965909090909091, 0.9299363057324841, 0.16193181818181818, 0.9808917197452229)
    wait_for_mapload()

def click_city_button():
    double_click_screen_area(0.05965909090909091, 0.9299363057324841, 0.16193181818181818, 0.9808917197452229)
    wait_for_baseload()

def click_map_search():
    click_screen_area(0.90625, 0.7722929936305732, 0.9744318181818182, 0.7961783439490446)
    wait_for_map_search()


def click_monster_search():
    click_screen_area(0.8409090909090909, 0.7961783439490446, 0.9431818181818182, 0.8519108280254777)
    wait_for_monster_search()

def click_search_go():
    click_screen_area(0.7329545454545454, 0.9410828025477707, 0.9375, 0.9729299363057324)
    wait_for_buffering(False, 20)

def click_monster():
    print('INCOMPLETE')
    imname = 'images/monster_search.png'
    im = grab_phone_area(0.26136363636363635, 0.31528662420382164, 0.6505681818181818, 0.5398089171974523)
    im.save(imname, 'PNG')
    IM.match_template(imname, ['images/templates/level_marker.png'])
    exit(0)
    #missed monster
    if (not color_comp(0.03409090909090909, 0.3646496815286624, C.Color(20, 11, 14))) or \
            (not color_comp(0.03977272727272727, 0.6640127388535032, C.Color(10, 10, 10))) or \
            (not color_comp(0.39204545454545453, 0.6719745222929936, C.Color(112, 18, 10))):
        click_map_button()
        wait_for_baseload()
        click_map_button()
        wait_for_mapload()
        attack_monster()

    wait_for_monsterattackscreen()

def click_monster_attackbutton():
    click_screen_area(0.2471590909090909, 0.6592356687898089, 0.7556818181818182, 0.6894904458598726)
    wait_for_march_setup()


def click_army4():
    click_screen_area(0.8096590909090909, 0.1751592356687898, 0.8522727272727273, 0.19745222929936307)

def click_include_monster():
    click_screen_area(0.8977272727272727, 0.27229299363057324, 0.9545454545454546, 0.30254777070063693)

def click_send_attack():
    click_screen_area(0.7357954545454546, 0.945859872611465, 0.9431818181818182, 0.9792993630573248)
    wait_for_mapload()


def click_coord_input():
    click_screen_area(0.35795454545454547, 0.8455414012738853, 0.6704545454545454, 0.8646496815286624)
    wait_for_coord_input()


def click_ok_and_wait():
    click_screen_area(0.7670454545454546, 0.535031847133758, 0.9545454545454546, 0.5843949044585988)
    wait_for_ok_finish()


def click_xinput():
    click_screen_area(0.25, 0.48089171974522293, 0.4659090909090909, 0.5015923566878981)
    wait_for_keyboard()


def click_yinput():
    click_screen_area(0.6051136363636364, 0.48089171974522293, 0.8267045454545454, 0.5015923566878981)
    wait_for_keyboard()


def click_lordmenuicon():
    click_screen_area(0.04, 0.03349282296650718, 0.12285714285714286, 0.0733652312599681)
    wait_for_lordmenu()


def click_lordmenuback():
    click_screen_area(0.022857142857142857, 0.014354066985645933, 0.11714285714285715, 0.049441786283891544)
    robot_sleep(1000)
    #wait_for_mapload()


def click_coord_go():
    click_screen_area(0.36363636363636365, 0.5828025477707006, 0.6420454545454546, 0.6162420382165605)
    timeout = 400
    while (timeout > 0):
        im = grab_phone_area(0.014204545454545454, 0.07643312101910828, 0.05397727272727273, 0.09554140127388536)
        levelnum = img_to_text(im)
        if (levelnum == None):
            print('No levelnum')
        else:
            print('levelnum: ' + str(levelnum))
            break
        robot_sleep(250)
        timeout -= 1






#---------------wait functions--------------

def wait_for_march_setup():
    while (not color_comp(0.9034090909090909, 0.10828025477707007, C.Color(17, 13, 10))) or \
            (not color_comp(0.48863636363636365, 0.2754777070063694, C.Color(30, 23, 13))) or \
            (not color_comp(0.48863636363636365, 0.35828025477707004, C.Color(211, 184, 146))) or \
            (not color_comp(0.9147727272727273, 0.9585987261146497, C.Color(69, 92, 20))):
        robot_sleep(250)
    #template = ''
    #need to look for monster within search area
    #print('INCOMPLETE')
def wait_for_monster_search():
    wait_for_point(0.8295454545454546, 0.8184713375796179, 248, 181, 126)

def wait_for_map_search():
    while (not color_comp(0.14488636363636365, 0.9506369426751592, C.Color(210, 43, 50))) or \
            (not color_comp(0.7784090909090909, 0.9554140127388535, C.Color(66, 95, 13))) or \
            (not color_comp(0.375, 0.9267515923566879, C.Color(211, 184, 146))) or \
            (not color_comp(0.5056818181818182, 0.8009554140127388, C.Color(96, 75, 50))):
        robot_sleep(250)

def wait_for_buffering(debug, timeout):
    print('wait_for_buffering')
    robot_sleep(1000)
    clear_screen()
    im = grab_phone_area(0.8948863636363636, 0.802547770700637, 0.9943181818181818, 0.8550955414012739)
    im.save('images/bufferimg.png')
    ptlist = []
    templatelist = ['images/templates/buffer1.png', 'images/templates/buffer2.png',
                   'images/templates/buffer3.png', #4 has been deleted
                   'images/templates/buffer5.png', 'images/templates/buffer6.png',
                   'images/templates/buffer7.png', 'images/templates/buffer8.png',
                   'images/templates/buffer9.png', 'images/templates/buffer10.png',
                   'images/templates/buffer11.png', 'images/templates/buffer12.png',
                   'images/templates/buffer13.png', 'images/templates/buffer14.png',
                   'images/templates/buffer15.png', 'images/templates/buffer16.png',
                   'images/templates/buffer17.png', 'images/templates/buffer18.png']
    if(debug):
        ptlist = IM.match_template_debug('images/bufferimg.png', templatelist, '/buffering/'+str(random.randint(0,100))+'-buffer')
    else:
        ptlist = IM.match_template('images/bufferimg.png', templatelist)
    if(len(ptlist)>0):
        print('waiting for load...')
        timeout-=1
        if(timeout>0):
            if(timeout %2 == 0):
                pyautogui.moveRel(0,20)
            else:
                pyautogui.moveRel(0,-20)
            return wait_for_buffering(True, timeout)
        else:
            print('wait for buffer timed out')
            IM.match_template_debug('images/bufferimg.png', templatelist,'TIMEOUT-'+str(random.randint(0, 100)) + '-buffer')
            screen_test()
            return

    print('finished buffering!')

def wait_for_monsterattackscreen():
    while (not color_comp(0.03409090909090909, 0.3646496815286624, C.Color(20, 11, 14))) or \
            (not color_comp(0.03977272727272727, 0.6640127388535032, C.Color(10, 10, 10))) or \
            (not color_comp(0.39204545454545453, 0.6719745222929936, C.Color(112, 18, 10))):
        robot_sleep(250)

def wait_for_coord_input():
    timeout = 20
    while (not color_comp(0.24147727272727273, 0.4171974522292994, C.Color(208, 186, 143))) or \
            (not color_comp(0.26704545454545453, 0.4888535031847134, C.Color(165, 131, 87))) or \
            (not color_comp(0.21022727272727273, 0.5859872611464968, C.Color(208, 186, 143))) or \
            (not color_comp(0.45170454545454547, 0.5971337579617835, C.Color(81, 108, 18))):
        if(timeout > 0):
            robot_sleep(250)
        else:
            click_coord_input()



def wait_for_ok_finish():
    while (not color_comp(0.23295454545454544, 0.5939490445859873, C.Color(211, 184, 146))) or \
            (not color_comp(0.44886363636363635, 0.5939490445859873, C.Color(79, 105, 18))):
        robot_sleep(250)
def regular_keyboard():
    return (not color_comp(0.9176136363636364, 0.5493630573248408, C.Color(255, 255, 255))) or \
    (not color_comp(0.5255681818181818, 0.5461783439490446, C.Color(255, 255, 255))) or \
    (not color_comp(0.7642045454545454, 0.410828025477707, C.Color(211, 184, 146)))

def airdroid_keyboard():
    return (not color_comp(0.08238636363636363, 0.9713375796178344, C.Color(63, 193, 103))) or \
    (not color_comp(0.8210227272727273, 0.9554140127388535, C.Color(237, 237, 237))) or \
    (not color_comp(0.7982954545454546, 0.8821656050955414, C.Color(255, 255, 255)))
def wait_for_keyboard():
    while regular_keyboard() and airdroid_keyboard():
        robot_sleep(250)




def wait_for_suggested_quest():
    while (not color_comp(0.11647727272727272, 0.8487261146496815, C.Color(82, 5, 3))) and \
            (not color_comp(0.0625, 0.8423566878980892, C.Color(7, 87, 36))) and \
            (not color_comp(0.3181818181818182, 0.5828025477707006, C.Color(196, 182, 157))) and \
            (not color_comp(0.5909090909090909, 0.5414012738853503, C.Color(174, 172, 150))):
        robot_sleep(250)

#is visible in both map and city screens
def wait_for_top_bar():
    while (not color_comp(0.19318181818181818, 0.05573248407643312, C.Color(168, 13, 15))) or \
            (not color_comp(0.4005681818181818, 0.06050955414012739, C.Color(89, 9, 4))) or \
            (not color_comp(0.9090909090909091, 0.06847133757961783, C.Color(3, 34, 48))):
        robot_sleep(250)

def wait_for_baseload():
    print('waiting for baseload')
    wait_for_suggested_quest()
    wait_for_top_bar()
    print('baseload finished')

def wait_for_bookmarks():
    while (not color_comp(0.05965909090909091, 0.6767515923566879, C.Color(139, 54, 62))) or \
            (not color_comp(0.04261363636363636, 0.6942675159235668, C.Color(109, 43, 49))) or \
            (not color_comp(0.08522727272727272, 0.695859872611465, C.Color(132, 55, 58))):
        robot_sleep(250)
def wait_for_mapandsearch():
    while (not color_comp(0.05965909090909091, 0.7786624203821656, C.Color(89, 73, 44))) or \
            (not color_comp(0.05397727272727273, 0.7961783439490446, C.Color(216, 197, 153))) or \
            (not color_comp(0.9346590909090909, 0.7818471337579618, C.Color(182, 133, 92))) or \
            (not color_comp(0.9630681818181818, 0.7770700636942676, C.Color(210, 170, 113))):
        robot_sleep(250)

def wait_for_mapload():
    print('wait_for_mapload')
    wait_for_bookmarks()
    wait_for_top_bar()
    wait_for_mapandsearch()
    wait_for_buffering(False, 20)
    if(test_mapload()):
        robot_sleep(250)
    else:
        reload_map()

def wait_for_lordmenu():
    print('wait_for_lordmenu')
    timeout = 20
    while (not color_comp(0.5914285714285714, 0.03349282296650718, C.Color(151, 36, 33))) or \
            (not color_comp(0.9571428571428572, 0.03827751196172249, C.Color(9, 9, 9))) or \
            (not color_comp(0.8685714285714285, 0.2647527910685805, C.Color(205, 178, 140))) or \
            (not color_comp(0.6114285714285714, 0.5964912280701754, C.Color(31, 19, 19))) or \
            (not color_comp(0.4942857142857143, 0.8054226475279107, C.Color(206, 183, 144))):
        if(timeout>0):
            robot_sleep(250)
            timeout-=1
        else:
            click_lordmenuicon()

#------------------test functions--------------------
def test_monster_attackscreen():
    return (color_comp(0.03409090909090909, 0.3646496815286624, C.Color(20, 11, 14))) and \
    (color_comp(0.03977272727272727, 0.6640127388535032, C.Color(10, 10, 10))) and \
    (color_comp(0.39204545454545453, 0.6719745222929936, C.Color(112, 18, 10)))

def test_top_bar():
    if(color_comp(0.19318181818181818, 0.05573248407643312, C.Color(168, 13, 15))) and \
    (color_comp(0.4005681818181818, 0.06050955414012739, C.Color(89, 9, 4))) and \
    (color_comp(0.9090909090909091, 0.06847133757961783, C.Color(3, 34, 48))):
        return True
    else:
        print('test_top_bar returned False')
        return False

def test_bookmarks():
    if(color_comp(0.05965909090909091, 0.6767515923566879, C.Color(139, 54, 62))) and \
    (color_comp(0.04261363636363636, 0.6942675159235668, C.Color(109, 43, 49))) and \
    (color_comp(0.08522727272727272, 0.695859872611465, C.Color(132, 55, 58))):
        return True
    else:
        print('test_bookmarks returned False!')
        return False

def test_mapandsearch():
    if(color_comp(0.05965909090909091, 0.7786624203821656, C.Color(89, 73, 44))) and \
    (color_comp(0.05397727272727273, 0.7961783439490446, C.Color(216, 197, 153))) and \
    (color_comp(0.9346590909090909, 0.7818471337579618, C.Color(182, 133, 92))) and \
    (color_comp(0.9630681818181818, 0.7770700636942676, C.Color(210, 170, 113))):
        return True
    else:
        print('test_mapandsearch returned False!')
        return False

def test_mapload():
    wait_for_buffering(False, 20)
    return test_top_bar() and test_bookmarks() and test_mapandsearch()

def test_suggestedquest():
    return (color_comp(0.11647727272727272, 0.8487261146496815, C.Color(82, 5, 3))) and \
    (color_comp(0.0625, 0.8423566878980892, C.Color(7, 87, 36))) and \
    (color_comp(0.3181818181818182, 0.5828025477707006, C.Color(196, 182, 157))) and \
    (color_comp(0.5909090909090909, 0.5414012738853503, C.Color(174, 172, 150)))
def test_baseload():
    wait_for_buffering(False, 20)
    return test_suggestedquest() and test_top_bar()

def test_is_ad():
    return simple_color_comp(433, 88, 241, 222, 225) or \
           simple_color_comp(431, 87, 181, 137, 141) or \
           simple_color_comp(435, 91, 184, 131, 134) or \
           simple_color_comp(461, 66, 241, 222, 225)

def test_safe_tile():
    return analyze_rss_menu()


#------------------find functions----------------------





#------------------compound functions------------------
def attack_monster():
    click_map_search()
    click_monster_search()
    click_search_go()
    click_monster()
    click_monster_attackbutton()
    click_army4()
    click_include_monster()
    click_send_attack()

def input_coords(xval, yval):
    click_xinput()
    typewrite(xval)
    click_ok_and_wait()
    click_yinput()
    typewrite(yval)
    click_ok_and_wait()

def move_to(xcoord, ycoord):
    click_coord_input()
    input_coords(xcoord, ycoord)
    click_coord_go()
    wait_for_mapload()

def screen_test():
    click_lordmenuicon()
    click_lordmenuback()

def reload_map():
    detect_context()
    open_map()

#assumes city view as base
def open_map():
    wait_for_baseload()
    click_map_button()

def attack_monsters():
    click_map_button()
    attack_monster()

def clear_interference():
    print('clear_interference')
    if(test_monster_attackscreen()):
        debug_screenshot('clear_interference')
        click_safe_area_north()
    wait_for_mapload()

def test_accountdetection(accountview):
    accountaccountview = accountview.get_connection('accountaccountview')
    switchaccountview = accountaccountview.get_connection('switchaccountview')
    googleplayloginview = switchaccountview.get_connection('googleplayloginview')
    for i in range(0,11):
        farmview = googleplayloginview.get_connection('farms'+str(i))
        print(farmview.name + str(farmview.getbutton().detect()))

def test_farm01pos(accountview):
    accountaccountview = accountview.get_connection('accountaccountview')
    switchaccountview = accountaccountview.get_connection('switchaccountview')
    googleplayloginview = switchaccountview.get_connection('googleplayloginview')
    farmview = googleplayloginview.get_connection('farms0')
    farm0pos = farmview.get_connection('farm0pos')
    farm1pos = farmview.get_connection('farm1pos')
    for i in range(0, 100):
        print('farm0pos: ' + str(farm0pos.getbutton().detect()))
        print('farm1pos: ' + str(farm1pos.getbutton().detect()))
        robot_sleep(250)

def test_donationview(cityview):
    allianceview = cityview.get_connection('allianceview')
    allianceview.click_and_wait()
    alliancetechview = allianceview.get_connection('alliancetechview')
    alliancetechview.click_and_wait()
    alliancedonateview = alliancetechview.get_connection('alliancedonateview')
    alliancedonateview.click_and_wait()
    alliancedonatepostview = alliancedonateview.get_connection('alliancedonatepostview')
    alliancedonatepostview.click()
    for i in range(0,100):
        for option in alliancedonatepostview.optionlist:
            print(option.name + ': ' + str(option.detect()))



#INCOMPLETE (expand to more modes)
#makes sure that game view is set to the city view
def clear_screen():
    print('detect_context')
    if (test_is_ad()):
        print('detected ad!')
        click_close_ad()
    if (test_monster_attackscreen()):
        print('detected monster screen!')
        click_safe_area_north()

def detect_context():
    wait_for_buffering(False,10)
    clear_screen()
    if (test_mapload()):
        print('detected map!')
        click_city_button()
    if (test_baseload()):
        print('detected base!')
        robot_sleep(250)
    else:
        debug_screenshot('set_context')

def clear_spaces(stringy):
    for i in range(0, len(stringy)):
        if stringy[i] == ' ':
            stringy[i] = '_'
    return stringy



def analyze_rss_menu():
    print('analyze_rss_menu')
    #RssType&Level
    im = grab_phone_area(0.2727272727272727, 0.21337579617834396, 0.5511363636363636, 0.2356687898089172)
    header = clear_spaces(img_to_text(im))
    printstr = 'images/results/headers/header-' + header+'-'
    print(printstr)
    im.save(printstr+str(random.randint(0,100))+'.png')
    #Territory Tax
    im = grab_phone_area(0.3977272727272727, 0.28662420382165604, 0.48295454545454547, 0.3057324840764331)
    tax = clear_spaces(img_to_text(im))
    printstr = 'images/results/taxes/tax-' + tax+'-'
    print(printstr)
    im.save(printstr + str(random.randint(0, 100)) + '.png')
    #Reserves
    im = grab_phone_area(0.4460227272727273, 0.3105095541401274, 0.5625, 0.3328025477707006)
    reserves = clear_spaces(img_to_text(im))
    printstr = 'images/results/reserves/reserves-'+reserves+'-'
    print(printstr)
    im.save(printstr + str(random.randint(0, 100)) + '.png')
    #Gathered By
    im = grab_phone_area(0.5227272727272727, 0.3614649681528662, 0.7244318181818182, 0.3837579617834395)
    gatherer = clear_spaces(img_to_text(im))
    printstr = 'images/results/gatherers/gatherer-'+gatherer+'-'
    print(printstr)
    im.save(printstr + str(random.randint(0, 100)) + '.png')
    #Close Menu
    click_screen_area(0.8522727272727273, 0.2054140127388535, 0.9034090909090909, 0.23089171974522293)
    wait_for_mapload()


#----------click functions-----------




def send_gatherers(farmtype, marches):
    #will start from farm tile menu
    #click gather
    #wait for load
    if(marches == 1):
        if(farmtype == 0):
            print('INCOMPLETE')
            #so on



def navigate_section(ft, marches):
    ptlist = IM.find_tiles(1)
    for pt in ptlist:
        print('pt: '+str(pt))
        print('point: ' + str(pt[0])+','+str(pt[1]))
        click_tile_check(pt[0],pt[1])
    if(test_safe_tile()):
        send_gatherers(ft, marches)
    clear_interference()



#should return number of marches sent out
def execute_lane(lane, farmtype, marches):
    move_to(str(lane.startx),str(lane.starty))
    for i in range(0, int(lane.paces)):
        lanepace = SV.getxwidth()
        # negative bc have to drag in opposite direction
        screen_move(-lanepace*lane.direction[0],-lanepace*lane.direction[1])
        wait_for_buffering(False, 20)
        navigate_section(farmtype, marches)



def nav_map(mode, farmtype, marches):
    #moves in a spiral from top
    laneslist = mm.generate_lanes(mode)
    print('pre-shuffle')
    for lane in laneslist:
        print(str(lane))
    random.shuffle(laneslist)
    for lane in laneslist:
        print('executing lane: ' + str(lane))
        if(marches > 0):
            execute_lane(lane, farmtype, marches)
            marches-=1
        else:
            break

def map_navigate(cityview):
    mapview = cityview.get_connection('mapview')
    print('accessing mapview!')
    mapview.click_button()
    mapview.waitforload()
    zoom_out()
    woodtileview = mapview.get_connection('woodtileview')

    def screen_scan():
        mapview.waitforload()
        woodtileview.create_buttons()
        while (woodtileview.hasnextbutton()):
            woodtileview.click_button()
            robot_sleep(2000)
            woodtileview.next_button()

    for i in range(0, 15):
        spiral_move(50, waitfunc=screen_scan)




def open_airdroid(): #redundancy because airdoid is rather unresponsive
    subprocess.call(["open", "-a", "airdroid.app"])
    simple_click(766, 44)
    robot_sleep(1000)
    simple_click(766, 44)
    robot_sleep(3000)
    print('airdroid opened')

def click_phone_start():
    simple_click(838, 157)
    time.sleep(5)

def click_vysor_fullscreen():
    simple_click(470, 35)
    robot_sleep(500)
    simple_click(904, 181)
    robot_sleep(500)
    simple_click(925,56)
    robot_sleep(500)

#this has to be hard coded
def open_vysor():
    subprocess.call(["open", "-a", "vysor.app"])
    countdown_sleep(5)
    click_phone_start()
    countdown_sleep(12) #wait for ad to load
    if(test_is_ad()):
        click_close_ad()
    click_vysor_fullscreen()
    if(test_is_ad()):
        click_close_ad()

def init_screen(): #click phone screen in a safe area to get airdroid warmed up
    wait_for_baseload()
    click_safe_area_north()
    robot_sleep(1000)

def init_script():
    open_memu()
    init_screen()
    print('finished init!')