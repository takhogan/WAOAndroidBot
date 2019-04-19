import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyautogui
import random
import config.SystemVars
import util.MapManager as MM
import popo.Color as C
import popo.Context as Context
import time
import numpy
import subprocess
import pyscreenshot as ImageGrab
import pytesseract
import pyperclip
import util.ImageMatcher as IM
from PIL import ImageDraw
import math
import cv2 as cv
from datetime import datetime


SV = config.SystemVars.SystemVars()
xscroll = SV.getxscroll()
yscroll = SV.getyscroll()
mm = MM.MapManager(3, 5)
xwidth = SV.getxwidth()
screenwidth = xwidth
yheight = SV.getyheight()
screenheight = yheight
screenx = SV.getscreenx()
screeny = SV.getscreeny()
mapangle = SV.getmapangle()

#-----------quickarea-------------




#-----------issues-------------
#a lot of false positives with wait for buffering
#there is a little lane in TOD territory that we should delete

#-----------init functions-------------
def init():
    open_memu()

def open_memu():
    subprocess.Popen(['cmd', '/c', 'C:\\"Program Files"\\Microvirt\\MEmu\\MEmu.exe'])
    subprocess.Popen(r"C:\Program Files\Microvirt\MEmu\MEmu.exe")
    print('here')

def close_memu():
    simple_click(1662, 125)

def open_warandorder():
    wait_warandordericon()
    click_screen_area(0.285, 0.52890625, 0.35125, 0.57109375)
    show_button_area('appicon',0.285, 0.52890625, 0.35125, 0.57109375)

def wait_warandordericon():
    timeout = 20
    while (not color_comp(0.28125, 0.52734375, C.Color(51, 52, 49))) or \
            (not color_comp(0.35625, 0.528125, C.Color(68, 69, 67))) or \
            (not color_comp(0.28, 0.571875, C.Color(20, 21, 20))) or \
            (not color_comp(0.35625, 0.57265625, C.Color(23, 24, 23))) or \
            (not color_comp(0.345, 0.5578125, C.Color(223, 46, 25))) or \
            (not color_comp(0.28375, 0.53671875, C.Color(218, 188, 141))):
        if(timeout>0):
            robot_sleep(250)
            timeout-=0.25
            if(timeout%4==0):
                print('waiting for warandordericon...' + str(timeout))
        else:
            print('wait_warandordericon timeout')
            break







def detect_context_new():
    #will detect and return the current context
    return
def detect_context_switch(context):
    #will cycle through the context switch options and detect which context has been switched to
    return


#--------------------------------------------------util functions------------------------------------------------------

def zoom_out():
    print('zooming out!')
    move_to_screen_area(0.4,0.4,0.6,0.6)
    for j in range (0,4):
        pyautogui.keyDown('ctrl')
        x,y=percent_to_absolute(0.5,0.5)
        for i in range(0,10):
            pyautogui.scroll(-100,x,y)
            robot_sleep(250)
        pyautogui.keyUp('ctrl')
        robot_sleep(210)


def debug_screenshot(message):
    im = full_screen_shot()
    im.save(message + '_debug' + str(random.randint(0,100))+'.png')


def show_button_area(name,cx1,cy1,cx2,cy2):
    im = full_screen_shot()
    draw_click_areas(im, cx1, cy1, cx2, cy2)
    # idk if im is an object
    im.save(name+'-button-area.png', 'PNG')

def draw_click_areas(im, cx1, cy1, cx2, cy2):
    x1, y1 = percent_to_absolute(cx1,cy1)
    x2, y2 = percent_to_absolute(cx2, cy2)
    draw = ImageDraw.Draw(im)
    draw.rectangle([x1, y1, x2, y2], fill=None, outline=128)
    del draw


def countdown_sleep(seconds):
    for i in range(seconds, 0, -1):
        print(str(i)+'...')
        time.sleep(1)


def generate_delay(ms):
    norm = numpy.random.randn()
    if (norm < -2):
        norm = -2
    norm = norm * 100
    secs = (ms+norm)/1000
    return secs


def robot_sleep(ms):
    if(ms < 210):
        ms = 210
    secs = generate_delay(ms)
    time.sleep(secs)


def percent_to_absolute(cx, cy):
    x = xwidth * cx + screenx
    y = yheight * cy + screeny
    return x,y


#there are 2 copies of this functions
def coord_to_percent(x,y):
    adjx = x - SV.getscreenx()
    adjy = y - SV.getscreeny()
    percentx = adjx/SV.getxwidth()
    percenty = adjy/SV.getyheight()
    return percentx,percenty

def simple_click(x,y):
    pyautogui.click(x,y)
    robot_sleep(500)

#there are two copies of this function
def get_pixel(x, y):
    width, height = pyautogui.size()
    xr = x+1
    xl = x-1
    yr = y+1
    yl = y-1
    target = (1,1)
    if(xl<0):
        xr+=1
        xl+=1
        yr+=1
        yl+=1
        target = (0,0)
    elif(xr>width-1):
        xr -= 1
        xl -= 1
        yr -= 1
        yl -= 1
        target = (2,2)
    #print(str(xl)+","+str(yl)+","+str(xr)+","+str(yr)+",")
    im = ImageGrab.grab(bbox=(xl, yl, xr, yr), childprocess=False)
    p=im.getpixel(target)
    return p

def get_color(cx, cy):
    x,y = percent_to_absolute(cx,cy)
    if(SV.getIsMac()):
        r,g,b,_ = get_pixel(x,y)
    else:
        r,g,b = get_pixel(x,y)
    return C.Color(r,g,b)

def grab_phone_area(cx1, cy1, cx2, cy2):
    x1, y1 = percent_to_absolute(cx1, cy1)
    x2, y2 = percent_to_absolute(cx2, cy2)
    width = x2-x1
    height = y2-y1
    img = ImageGrab.grab(bbox=(x1,y1,x2,y2), childprocess=False)
    if(SV.isMac):
        img = img.crop((0,0,width*2,height*2)) #this has to be *2 because resolution is x 2
    img = img.crop((0,0,width,height))
    return img


def img_to_text(im):
    return pytesseract.image_to_string(im, lang='eng')

def numimg_to_text(im):
    return pytesseract.image_to_string(im, lang='eng', config = '--tessedit_char_whitelist 0123456789')


def scan_numarea(cx1, cy1, cx2, cy2):
    im = grab_phone_area(cx1,cy1,cx2,cy2)
    return numimg_to_text(im)

def debug_scan_textarea(cx1, cy1, cx2, cy2, name):
    im = grab_phone_area(cx1, cy1, cx2, cy2)
    im.save(name + '.png', 'PNG')
    return img_to_text(im)

def debug_invert_scan_textarea(cx1, cy1, cx2, cy2, name):
    im = grab_phone_area(cx1, cy1, cx2, cy2)
    im.save('init_scanarea.png','PNG')
    im = cv.imread('init_scanarea.png')
    im = cv.bitwise_not(im)
    cv.imwrite('debug' + name +str(random.randint(0,99)) + '.png', im)
    return img_to_text(im)

def invert_scan_numarea(cx1, cy1, cx2, cy2):
    im = grab_phone_area(cx1, cy1, cx2, cy2)
    im.save('init_scanarea.png','PNG')
    im = cv.imread('init_scanarea.png')
    im = cv.bitwise_not(im)
    # cv.imwrite('debug' + name +str(random.randint(0,99)) + '.png', im)
    return numimg_to_text(im)

def colorsimscore(base, comp):
    redscore =(base.r-comp.r)
    greenscore = (base.g-comp.g)
    bluescore = (base.b-comp.b)
    return (redscore*redscore+greenscore*greenscore+bluescore*bluescore)**0.5


def wait_for_point(cx, cy, r, g, b):
    x,y = percent_to_absolute(cx,cy)
    print('x: ' + str(x) + ', y: ' + str(y))
    base = C.Color(r, g, b)
    print('base: ' + str(base))
    comp = get_color(cx, cy)
    print('comp: ' + str(comp))
    compscore = colorsimscore(base, comp)
    print(compscore)
    while(compscore > 60):
        comp = get_color(cx,cy)
        compscore = colorsimscore(base, comp)
        print('comp: ' + str(comp))
        print(compscore)
        robot_sleep(250)

def simple_wait(x,y,r,g,b):
    base = C.Color(r, g, b)
    cr,cg,cb,_ = get_pixel(x, y)
    comp = C.Color(cr,cg,cb)
    compscore = colorsimscore(base, comp)
    print('compscore: ' + compscore)
    while(compscore>60):
        cr, cg, cb, _ = get_pixel(x, y)
        comp = C.Color(cr, cg, cb)
        compscore = colorsimscore(base, comp)
        robot_sleep(250)

def spiral_move(limit, distance = 1, counter = 0, waitfunc = robot_sleep(500)):
    while(counter < limit):
        for i in range(0, 2):
            #NESW
            direction = counter%4
            if(direction == 0):
                funcname = drag_up
            elif(direction == 1):
                funcname = drag_right
            elif(direction == 2):
                funcname = drag_down
            else:
                funcname = drag_left
            for i in range(0, distance):
                funcname()
                waitfunc()
            counter+=1
        distance+=1





#there are 2 color comp definitions
def color_comp(cx,cy,color):
    comp = get_color(cx, cy)
    base = color
    compscore = colorsimscore(base, comp)
    if (compscore < 60):
        return True
    else:
        robot_sleep(200)
        return False

def simple_color_comp(x,y,r,g,b):
    base = C.Color(r, g, b)
    cr, cg, cb, _ = get_pixel(x, y)
    comp = C.Color(cr, cg, cb)
    compscore = colorsimscore(base, comp)
    if (compscore < 60):
        return True
    else:
        print('comp: ' + str(comp))
        print(compscore)
        robot_sleep(200)
        return False


def paste_text(text):
    pyperclip.copy(text)
    pyautogui.hotkey('command', 'v')
    robot_sleep(250)

def typewrite(stringy):
    for i in range(0,len(stringy)):
        pyautogui.typewrite(stringy[i])
        robot_sleep(210)

def click_screen_loc(cx, cy):
    x, y = percent_to_absolute(cx, cy)
    pyautogui.click(x,y)
    robot_sleep(200)

def click_screen_loc_fast(cx, cy):
    x, y = percent_to_absolute(cx, cy)
    pyautogui.click(x,y)

def double_click_screen_loc(cx, cy):
    x, y = percent_to_absolute(cx, cy)
    pyautogui.doubleClick(x,y)
    robot_sleep(200)

#INCOMPLETE (should make a circle method bc it is more realistic)
def click_screen_area(cx1, cy1, cx2, cy2):
    x1, y1 = percent_to_absolute(cx1, cy1)
    x2, y2 = percent_to_absolute(cx2, cy2)
    width = x2-x1
    height = y2-y1
    clickx = x1 + width * random.uniform(0,1)
    clicky = y1 + height * random.uniform(0,1)
    pyautogui.click(clickx,clicky)
    robot_sleep(200)

def click_screen_area_fast(cx1, cy1, cx2, cy2, n):
    x1, y1 = percent_to_absolute(cx1, cy1)
    x2, y2 = percent_to_absolute(cx2, cy2)
    width = x2 - x1
    height = y2 - y1
    clickx = x1 + width * random.uniform(0, 1)
    clicky = y1 + height * random.uniform(0, 1)
    for i in range (0, n):
        pyautogui.click(clickx,clicky)
        time.sleep(1/5)


def double_click_screen_area(cx1, cy1, cx2, cy2):
    x1, y1 = percent_to_absolute(cx1, cy1)
    x2, y2 = percent_to_absolute(cx2, cy2)
    width = x2 - x1
    height = y2 - y1
    clickx = x1 + width * random.uniform(0, 1)
    clicky = y1 + height * random.uniform(0, 1)
    pyautogui.click(clickx, clicky)
    robot_sleep(200)

def move_to_screen_area(cx1, cy1, cx2, cy2):
    x1, y1 = percent_to_absolute(cx1, cy1)
    x2, y2 = percent_to_absolute(cx2, cy2)
    width = x2 - x1
    height = y2 - y1
    movex = x1 + width * random.uniform(0, 1)
    movey = y1 + height * random.uniform(0, 1)
    pyautogui.moveTo(movex, movey)

def drag_relative(startx, starty, xdist, ydist):
    pyautogui.mouseDown(startx, starty)
    pyautogui.moveRel(xdist,ydist, generate_delay(500))
    pyautogui.mouseUp()

def drag_right():
    center_screen_move(-xwidth/2,0)
def drag_east():
    drag_right()
def init_drag_east():
    center_screen_move(-xwidth/20,0)

def drag_left():
    center_screen_move(xwidth/2,0)
def drag_west():
    drag_left()
def drag_west_south_west():
    center_screen_move(xwidth/2, -xwidth/4)


def drag_up():
    center_screen_move(0,yheight/2)

def drag_up_half():
    center_screen_move(0,yheight/4)

def drag_north():
    drag_up()

def drag_down():
    center_screen_move(0,-xwidth/2)
def drag_south():
    drag_down()

def drag_southeast():
    center_screen_move(-xwidth/2, -xwidth/2)

def drag_screen(cx1,cy1, cx2, cy2, xdist, ydist):
    x1, y1 = percent_to_absolute(cx1, cy1)
    x2, y2 = percent_to_absolute(cx2, cy2)
    width = x2 - x1
    height = y2 - y1
    clickx = x1 + width * random.uniform(0, 1)
    clicky = y1 + height * random.uniform(0, 1)

    xmax = (screenx + xwidth)
    if clickx > xmax - 1:
        print('clickx: ' + str(clickx) + ' is over max')
        clickx = xmax - 1
    if clickx < screenx:
        print('clickx: ' + str(clickx) + ' is under min')
        clickx = screenx + 1

    if(xdist > 0):
        if(clickx+xdist > xmax-1):
            xdist -= ((clickx+xdist)-(xmax-1))
    else:
        if(clickx+xdist-1 < screenx):
            xdist += screenx-(clickx+xdist-1)
    pyautogui.moveTo(clickx, clicky)
    pyautogui.dragRel(xdist, ydist, generate_delay(600))

def center_screen_move(xdist,ydist):
    drag_screen(0.4, 0.4, 0.6, 0.6, xdist, ydist)
    robot_sleep(500)

def screen_move(xdist, ydist):
    if(xdist < 0):
        drag_screen(0.8011363636363636, 0.21337579617834396, 0.9801136363636364, 0.6464968152866242, xdist, ydist)
    else:
        drag_screen(0.019886363636363636, 0.2945859872611465, 0.17045454545454544, 0.643312101910828, xdist, ydist)
    robot_sleep(500)

def full_screen_shot():
    return grab_phone_area(0, 0, 1, 1)


def create_init_file():
    init_file = open('init_file.txt','r')
    linecounter = 0
    timestamp = None
    default_time_format = '%Y-%m-%d %H:%M:%S.%f'
    for line in init_file:
        timestamp = datetime.strptime(line,default_time_format)
        break

    init_file.close()
    nowtime = datetime.utcnow()
    if nowtime.date() > timestamp.date():
        init_file = open('init_file.txt','w')
        init_file.write(nowtime)




#----------------------------------------------------bot scripts-----------------------------------------------------




def process_collectionbuildings(cityview):
    lowerright = cityview.get_connection('lowerright')
    def lowerrighttimeout():
        zoom_out()
        lowerright.click_until(extraiterations=5, ontimeout=lowerrighttimeout)
    lowerright.click_until(extraiterations=5, ontimeout=lowerrighttimeout)
    zoom_out()

    lowermiddle = lowerright.get_connection('lowermiddle')
    stonequarryview = cityview.get_connection('stonequarryview')
    ironmineview = cityview.get_connection('ironmineview')
    foodfarmview = cityview.get_connection('foodfarmview')
    woodyardview = cityview.get_connection('woodyardview')
    # collection_buildings = [stonequarryview, ironmineview, foodfarmview, woodyardview]
    # home_view = np.repeat(cityview, 4)
    # map(Context.ImageContext.click_all, home_view, collection_buildings)
    nclicks = 0
    nclicks += stonequarryview.click_all(cityview)
    nclicks += ironmineview.click_all(cityview)
    nclicks += foodfarmview.click_all(cityview)
    nclicks += woodyardview.click_all(cityview)

    timeout = 8
    while (not lowermiddle.detect()):
        robot_sleep(250)
        lowermiddle.click_button()
        if(nclicks > 0):
            lowermiddle.click_button()
        if(not cityview.detect()):
            cityview.waitforload(timeout = 1)
        timeout-=1
        nclicks = 0
        nclicks += stonequarryview.click_all(cityview)
        nclicks += ironmineview.click_all(cityview)
        nclicks += foodfarmview.click_all(cityview)
        nclicks += woodyardview.click_all(cityview)
        if not (timeout > 0):
            cityview.waitforload()
            return


def accountview_to_googleplayloginview(accountview):
    accountview.click_button()
    accountview.waitforload()
    accountaccountview = accountview.get_connection('accountaccountview')
    accountaccountview.click_button()
    accountaccountview.waitforload()
    switchaccountview = accountaccountview.get_connection('switchaccountview')
    switchaccountview.click_button()
    switchaccountview.waitforload()
    googleplayloginview = switchaccountview.get_connection('googleplayloginview')
    googleplayloginview.click_button()
    googleplayloginview.waitforload(timeout=20)
    return googleplayloginview

def switch_account(cityview, farmname):
    accountview = cityview.get_connection('accountview')
    googleplayloginview = accountview_to_googleplayloginview(accountview)
    farms = googleplayloginview.get_connection(farmname).click_and_wait()
    farm0pos = farms.get_connection('farm0pos')
    if(farm0pos.getbutton().detect()):
        farm0pos.click_button()
        farm0pos.waitforload()
    else:
        farm1pos = farms.get_connection('farm1pos')
        farm1pos.click_button()
        farm1pos.waitforload()
    farmswitchconfirm = farm0pos.get_connection('cityview')
    return farmswitchconfirm.click_and_wait(timeout=10)

def process_harvestskill(cityview):
    skillactivateview = cityview.get_connection('skillactivateview').click_and_wait()
    skillactivateview = skillactivateview.get_connection('skillactivateview').click_and_wait()
    cityview = skillactivateview.get_connection('cityview')
    cityview.click_and_wait()

def process_donation(cityview):
    allianceview = cityview.get_connection('allianceview').click_and_wait()
    alliancetechview = allianceview.get_connection('alliancetechview').click_and_wait()
    alliancedonateview = alliancetechview.get_connection('alliancedonateview').click_and_wait()
    alliancedonateview = alliancedonateview.get_connection('alliancedonateview').click_and_wait()
    alliancetechreturnview = alliancedonateview.get_connection('alliancetechview').click_and_wait()
    allianceview = alliancetechreturnview.get_connection('allianceview').click_and_wait()
    return allianceview.get_connection('cityview').click_and_wait()

def process_rewardscart(cityview):
    rewardscartview = cityview.get_connection('rewardscartview')
    rewardscartview.click_all()
    rewardscartreceiptview = rewardscartview.get_connection('rewardscartreceiptview')
    if(rewardscartreceiptview.detect()):
        returncityview = rewardscartreceiptview.get_connection('cityview')
        returncityview.click_and_wait()
    else:
        cityview.waitforload()

def process_alliancehelps(cityview):
    alliancehelpbirdview = cityview.get_connection('alliancehelpbirdview')
    clicked = 0
    clicked += alliancehelpbirdview.click_all()
    if(clicked > 0):
        cityview.waitforload()

def process_alliancequests(cityview):
    alliancequestview = cityview.get_connection('alliancequestview')
    clicked = 0
    clicked += alliancequestview.click_all()
    if(clicked):
        alliancequestview.waitforload()
        alliancequestcollectview = alliancequestview.get_connection('alliancequestcollectview')
        alliancequestcollectview.click()
        if(alliancequestcollectview.detect()):
            alliancequestreturnview = alliancequestcollectview.get_connection('alliancequestreturnview')
            alliancequestreturnview.click_and_wait()
        returncityview = alliancequestview.get_connection('cityview')
        returncityview.click_and_wait()
    return

def process_depotview(cityview):
    depotview = cityview.get_connection('depotview')
    clicked = 0
    clicked += depotview.click_all()
    if(clicked > 0):
        returncityview = depotview.get_connection('cityview')
        returncityview.click_and_wait()



def clear_mail(mailview):
    mailselectview = mailview.get_connection('mailselectview')
    mailselectview.click()
    robot_sleep(500)
    mailselectallview = mailselectview.get_connection('mailselectallview')
    mailselectallview.click()
    robot_sleep(500)
    mailselectdeleteview = mailselectallview.get_connection('mailview').click_and_wait()

def process_alliancestatus_mailrewards(alliancestatusmailview):
    alliancestatusmailview.click_and_wait()
    topmailview = alliancestatusmailview.get_connection('topmailview')
    while topmailview.getbutton().detect():
        print('start')
        topmailview.click_and_wait()
        print('getting mailrewardview')
        mailrewardview = topmailview.get_connection('mailrewardview')
        mailrewardview.click_and_wait(ontimeout=topmailview.blank_timeout, timeout=1)
        rewardreceiptview = mailrewardview.get_connection('topmailview')
        print('finished mailrewards')
        if mailrewardview.detect():
            rewardreceiptview.click_and_wait()
        else:
            print('no reward')
        print('delete')
        maildeleteview = rewardreceiptview.get_connection('alliancestatusmailview')
        maildeleteview.click_and_wait(ontimeout=maildeleteview.blank_timeout)
    maildeleteview.get_connection('mailview').click_and_wait()

def process_systemnotice_mailrewards(systemnoticemailview):
    while systemnoticemailview.getbutton().detect():
        systemnoticemailview.click_and_wait()
        topmailview = systemnoticemailview.get_connection('topmailview')
        while topmailview.getbutton().detect():
            topmailview.click_and_wait()
            mailrewardview = topmailview.get_connection('mailrewardview')
            mailrewardview.click_and_wait(ontimeout=topmailview.blank_timeout, timeout=1)
            rewardreceiptview = mailrewardview.get_connection('topmailview')
            if mailrewardview.detect():
                rewardreceiptview.click_and_wait()
            maildeleteview = rewardreceiptview.get_connection('alliancestatusmailview')
            maildeleteview.click_and_wait(ontimeout=maildeleteview.blank_timeout)
        returnmailview = maildeleteview.get_connection('mailview').click_and_wait()
        robot_sleep(2000)

def process_mailrewards(cityview):
    mailview = cityview.get_connection('mailview').click_and_wait()
    clear_mail(mailview)
    alliancestatusmailview = mailview.get_connection('alliancestatusmailview')
    if alliancestatusmailview.getbutton().detect():
        process_alliancestatus_mailrewards(alliancestatusmailview)
    else:
        robot_sleep(3000)
        if alliancestatusmailview.getbutton().detect():
            process_alliancestatus_mailrewards(alliancestatusmailview)

    systemnoticemailview = mailview.get_connection('systemnoticemailview')
    if systemnoticemailview.getbutton().detect():
        process_alliancestatus_mailrewards(alliancestatusmailview)
    else:
        robot_sleep(3000)
        if systemnoticemailview.getbutton().detect():
            process_alliancestatus_mailrewards(alliancestatusmailview)
    process_systemnotice_mailrewards(systemnoticemailview)

    mailview.get_connection('cityview').click_and_wait()

def fortreinreturn(mapview):
    fortreinview = mapview.get_connection('fortreinforceview').click_and_wait()
    returnmapview = fortreinview.get_connection('mapview').click_and_wait()


def get_to_ruinsview(mapview):
    coordinputview = mapview.get_connection('coordinputview').click_and_wait()
    ruinsxinputview = coordinputview.get_connection('ruinsxinputview').click_and_wait()
    returncoordinputview = ruinsxinputview.get_connection('coordinputview').click_and_wait()
    ruinsyinputview = returncoordinputview.get_connection('ruinsyinputview').click_and_wait()
    returncoordinputview = ruinsyinputview.get_connection('coordinputview').click_and_wait()
    ruinsview = coordinputview.get_connection('ruinsview').click_and_wait()
    if not ruinsview.get_connection('rallyrebelsview').getbutton().detect():
        robot_sleep(1000)
    return ruinsview


def process_ruinsrally(mapview):
    ruinsview = get_to_ruinsview(mapview)
    rallyrebelsview = ruinsview.get_connection('rallyrebelsview').click_and_wait()
    rally10minview = rallyrebelsview.get_connection('rally10minview').click_and_wait()
    rallyaddbeastview = rallyrebelsview.get_connection('rallyaddbeastview').click_and_wait()
    rallysetoutmapview = rallyrebelsview.get_connection('mapview').click_and_wait()

def process_battlerebels(mapview):
    ruinsview = get_to_ruinsview(mapview)
    battlerebelsview = ruinsview.get_connection('battlerebelsview').click_and_wait()
    battlerebels1 = battlerebelsview.get_connection('battlerebels1').click_and_wait()
    battlerebelssuppressview = battlerebels1.get_connection('battlerebelssuppressview')
    if battlerebelssuppressview.getbutton().detect():
        battlerebelssuppressview.click_and_wait()
        marchsetoutview = battlerebelssuppressview.get_connection('mapview').click_and_wait()
    else:
        print('you didn\'t implement this you dumb fck')
        mapview.waitforload(timeout=0)

def process_full_battlerebels(cityview):
    mapview = cityview.get_connection('mapview')
    mapview.click_and_wait()
    process_battlerebels(mapview)
    mapview.get_connection('cityview').click_and_wait()


def process_joinrally(cityview):
    allianceview = cityview.get_connection('allianceview').click_and_wait()
    alliancebattleview = allianceview.get_connection('alliancebattleview').click_and_wait()
    rallyjoinview = alliancebattleview.get_connection('rallyjoinview').click_and_wait()
    rallyjoinsetoutview = rallyjoinview.get_connection('alliancebattleview').click_and_wait()
    returnallianceview = rallyjoinsetoutview.get_connection('allianceview').click_and_wait()
    returncityview = returnallianceview.get_connection('cityview').click_and_wait()



def process_buildingrewards(cityview):
    process_rewardscart(cityview)
    # process_alliancehelps(cityview)
    # process_alliancequests(cityview)
    # process_depotview(cityview)
    # drag_west()
    # process_rewardscart(cityview)
    # process_alliancehelps(cityview)
    # process_alliancequests(cityview)
    # process_depotview(cityview)
    # drag_west()
    # process_rewardscart(cityview)
    # process_alliancehelps(cityview)
    # process_alliancequests(cityview)
    # process_depotview(cityview)

def process_keprotocol(cityview):
    allianceview = cityview.get_connection('allianceview')
    allianceview.click_and_wait()
    alliancebuildingview = allianceview.get_connection('alliancebuildingview')
    alliancebuildingview.click_and_wait()
    alliancebuildinghallview = alliancebuildingview.get_connection('alliancebuildinghallview')
    alliancebuildinghallview.click_and_wait()
    alliancefortview = alliancebuildinghallview.get_connection('alliancefortview')
    alliancefortview.click_and_wait()
    reinforceview = alliancefortview.get_connection('reinforceview')
    reinforceview.click_and_wait()
    marchsetupview = reinforceview.get_connection('marchsetupview')
    marchsetupview.click_and_wait()
    marchsetoutview = marchsetupview.get_connection('marchsetupview')
    marchsetoutview.click_and_wait()

def process_elitegather(cityview):

    allianceview = cityview.get_connection('allianceview')
    allianceview.click_and_wait()
    alliancebuildingview = allianceview.get_connection('alliancebuildingview')
    alliancebuildingview.click_and_wait()
    alliancebuildingeliteview = alliancebuildingview.get_connection('alliancebuildingeliteview').click_and_wait()

    allianceeliteironview = alliancebuildingeliteview.get_connection('allianceeliteironview')
    allianceelitestoneview = alliancebuildingeliteview.get_connection('allianceelitestoneview')
    allianceelitefoodview = alliancebuildingeliteview.get_connection('allianceelitefoodview')
    allianceelitewoodview = alliancebuildingeliteview.get_connection('allianceelitewoodview')
    allianceeliteminescrollview = allianceelitefoodview.get_connection('allianceeliteminescrollview')
    food_coordlist = []
    wood_coordlist = []
    stone_coordlist = []
    iron_coordlist = []
    full_coordlist = []

    while not allianceeliteminescrollview.detect():
        food_coordlist += allianceelitefoodview.find()
        wood_coordlist += allianceelitewoodview.find()
        stone_coordlist += allianceelitestoneview.find()
        iron_coordlist += allianceeliteironview.find()
        full_coordlist += food_coordlist + wood_coordlist + stone_coordlist + iron_coordlist
        allianceeliteminescrollview.click()
        robot_sleep(100)

    if(len(full_coordlist) > 0):
        print('testing: ')
        for coordpair in full_coordlist:
            print(coordpair)
            topcorner = coordpair[0]
            bottomcorner = coordpair[1]
            print(bottomcorner)
            print(topcorner)
            height = bottomcorner[1]-topcorner[1]
            width = bottomcorner[0]-topcorner[0]
            endx = screenx+screenwidth
            print('-----')
            print('left: ')
            leftscantopresult = scan_numarea(bottomcorner[0], topcorner[1], 0.54875, topcorner[1]+.039)
            leftscanmiddleresult = scan_numarea(bottomcorner[0], topcorner[1]+.039, 0.54875, topcorner[1]+.039+.0375)
            leftscanbottomresult = scan_numarea(bottomcorner[0], topcorner[1]+.039+.0375, 0.54875, topcorner[1]+.039+.0375+.0315)
            print(leftscantopresult)
            print(leftscanmiddleresult)
            print(leftscanbottomresult)
            print('right: ')
            rightscan = invert_scan_numarea(.82, topcorner[1], .91, topcorner[1]+0.046875)
            print('current gatherers: ' + str(rightscan))
        print('-----')



def process_account(cityview, farmname, switchaccount = True):
    if(switchaccount):
        cityview = switch_account(cityview, farmname)

    # process_keprotocol(cityview)
    # process_full_battlerebels(cityview)
    # process_donation(cityview)
    process_mailrewards(cityview)
    # process_full_battlerebels(cityview)
    # process_harvestskill(cityview)
    # zoom_out()
    # process_buildingrewards(cityview)
    # process_collectionbuildings(cityview)
    # process_full_battlerebels(cityview)

def process_accounts(cityview, start = 0):
    truestart = int(start)
    modstart = (start * 4) % 4
    if modstart == 0:
        process_account(cityview, 'farms' + str(truestart))
        process_account(cityview, 'farms' + str(truestart))
    elif modstart == 1:
        process_account(cityview, 'farms' + str(truestart), switchaccount=False)
        process_account(cityview, 'farms' + str(truestart))
    elif modstart == 2:
        process_account(cityview, 'farms' + str(truestart))
    elif modstart == 3:
        process_account(cityview, 'farms' + str(truestart), switchaccount=False)
    for i in range(truestart+1,8 ):
        process_account(cityview, 'farms' + str(i))
        if i == 7:
            continue
        else:
            process_account(cityview,'farms'+str(i))

def default_process(start=0):
    print('stating from: ' + str(start))
    init()
    phonehomescreen = Context.Context.default_context()
    if (not phonehomescreen.detect()):
        phonehomescreenbutton = phonehomescreen.getbutton()
        phonehomescreenbutton.waitforbuttonload()
        phonehomescreen.click_and_wait(timeout=10)
    cityview = phonehomescreen.get_connection('cityview').click_and_wait(ontimeout=phonehomescreen.blank_timeout)
    if cityview is None:
        cityview = cityview.click_and_wait()

    # process_ruinsrally(mapview=cityview.get_connection('mapview').click_and_wait())
    # cityview = switch_account(cityview, 'farms5')
    # process_joinrally(cityview)
    # exit(0)

    # change the print here
    # cityview = adorrewardview.get_option('cityview')
    # process_elitegather(cityview)
    process_accounts(cityview, start=start)
    return phonehomescreen

if __name__=='__main__':
    # test_map_manager()
    start = 3
    default_process(start)


    # accountview = adorrewardview.get_option('cityview').get_connection('accountview')
    # accountview_to_googleplayloginview(accountview)
    # test_farm01pos(accountview)
    # test_accountdetection(accountview)
    # test_donationview(adorrewardview.get_option('cityview'))


    # process_donation(adorrewardview.get_option('cityview'))
    # process_keprotocol(adorrewardview.get_option('cityview'))

    close_memu()



    #THERE IS A BUILT IN switch to farm otherpos somewhere that we should change to a conditional


    print('complete!')

