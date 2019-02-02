#takes photo, processes image, matches image, creates result map, outputs resultmap and original image
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyscreenshot as ImageGrab
import cv2 as cv
import numpy as np
import util.MapNavigator as MN
import config.SystemVars as SystemVars
import random
import math


SV = SystemVars.SystemVars()
screenx = SV.getscreenx()
screeny = SV.getscreeny()

def distance(lastpt,pt):
    lastptx = lastpt[0]
    lastpty = lastpt[1]
    ptx = pt[0]
    pty = pt[1]
    return abs(lastptx-ptx)+abs(lastpty-pty)

def debug_template_match(img_rgb, img_gray, template, filename, threshold, fullcoord):
    w,h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    lastpt = None
    lastinsertpt = None
    pointlist = []
    for pt in zip(*loc[::-1]):
        print('point: ' + str(pt))
        if (lastpt == None):
            lastpt = pt
            lastinsertpt = pt
            if fullcoord:
                topcornerx = screenx + pt[0]
                topcornery = screeny + pt[1]
                bottomcornerx = screenx + pt[0] + w
                bottomcornery = screeny + pt[1] + h
                coordpair = [MN.coord_to_percent(topcornerx, topcornery),
                             MN.coord_to_percent(bottomcornerx, bottomcornery)]
                print(coordpair)
                pointlist.append(coordpair)
            else:
                xcentered = screenx + pt[0] + w / 2
                ycentered = screeny + pt[1] + h / 2
                print(str(xcentered) + ', ' + str(ycentered))
                pointlist.append(MN.coord_to_percent(xcentered, ycentered))
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        else:
            dist = distance(lastpt, pt)
            lastpt = pt
            if (dist > 1):
                insertdist = distance(lastinsertpt, pt)
                lastinsertpt = pt
                if (insertdist > 6):
                    if fullcoord:
                        topcornerx = screenx + pt[0]
                        topcornery = screeny + pt[1]
                        bottomcornerx = screenx + pt[0] + w
                        bottomcornery = screeny + pt[1] + h
                        coordpair = [MN.coord_to_percent(topcornerx, topcornery),
                                          MN.coord_to_percent(bottomcornerx,bottomcornery)]
                        print(coordpair)
                        pointlist.append(coordpair)
                    else:
                        xcentered = screenx + pt[0] + w / 2
                        ycentered = screeny + pt[1] + h / 2
                        print(str(xcentered) + ', ' + str(ycentered))
                        pointlist.append(MN.coord_to_percent(xcentered, ycentered))
                    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)


    cv.imwrite('images/results/' + filename+'.png', img_rgb)
    return pointlist
def template_match(img_gray, template, threshold, fullcoord):
    w,h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    lastpt = None
    lastinsertpt = None
    pointlist = []
    for pt in zip(*loc[::-1]):
        if (lastpt == None):
            lastpt = pt
            lastinsertpt = pt
            if fullcoord:
                topcornerx = screenx + pt[0]
                topcornery = screeny + pt[1]
                bottomcornerx = screenx + pt[0] + w
                bottomcornery = screeny + pt[1] + h
                pointlist.append([MN.coord_to_percent(topcornerx, topcornery),
                                  MN.coord_to_percent(bottomcornerx, bottomcornery)])
            else:
                xcentered = screenx + pt[0] + w / 2
                ycentered = screeny + pt[1] + h / 2
                pointlist.append(MN.coord_to_percent(xcentered, ycentered))
        else:
            dist = distance(lastpt, pt)
            lastpt = pt
            if (dist > 1):
                insertdist = distance(lastinsertpt, pt)
                lastinsertpt = pt
                if (insertdist > 6):
                    if fullcoord:
                        topcornerx = screenx + pt[0]
                        topcornery = screeny + pt[1]
                        bottomcornerx = screenx + pt[0] + w
                        bottomcornery = screeny + pt[1] + h
                        pointlist.append([MN.coord_to_percent(topcornerx, topcornery),
                                          MN.coord_to_percent(bottomcornerx,bottomcornery)])
                    else:
                        xcentered = screenx + pt[0] + w / 2
                        ycentered = screeny + pt[1] + h / 2
                        pointlist.append(MN.coord_to_percent(xcentered, ycentered))
    return pointlist


def match_template_debug(rgbname,templist, mod, threshold = 0.5, fullcoord = False):
    ptlist = []
    img_rgb = cv.imread(rgbname)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    counter = 0
    rnum = str(random.randint(0, 100))
    for temp in templist:
        template = cv.imread(temp, 0)
        ptlist += debug_template_match(img_rgb, img_gray, template, mod+rnum+'-'+str(counter), threshold, fullcoord)
        counter+=1
    for pt in ptlist:
        print(pt)
    return ptlist



def match_template(rgbname,templist, threshold = 0.5, fullcoord = False):
    ptlist = []
    img_rgb = cv.imread(rgbname)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

    for temp in templist:
        template = cv.imread(temp, 0)
        ptlist += template_match(img_gray, template, threshold, fullcoord)
    return ptlist

#INCOMPLETE (do some advanced detection here)
def find_tiles(type):
    im = MN.full_screen_shot()
    savename = 'tile_search.png'
    im.save(savename)
    if(type == 1):
        templist = ['images/templates/farmstead1.png','images/templates/farmstead2.png']
    elif(type == 2):
        templist = []
    elif(type == 3):
        templist = []
    elif(type == 4):
        templist = []
    else:
        templist = []
    return match_template_debug(savename,templist,'farm_tiles')

def main():
    templist = ['images/templates/template24.png']
    match_template('images/search_area3.png',templist)

if __name__=='__main__':
    main()
