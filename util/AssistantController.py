#! python3
import pyautogui
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyscreenshot as ImageGrab
import subprocess
import config.SystemVars
import time


#To use: run this program from command line:
#cd [filelocation]
#$python3 AssistantController.py

SV = config.SystemVars.SystemVars()
isMac = False

#Note some functions here are duplicates of other functions (this is to make sure the 'CONFIG' option works properly)

#why don't I just use pyautogui? good question

#-----------------util functions--------------------

def array_to_codearr(arr, header = '', footer = ''):
    codearr = '['
    arrlen = len(arr)
    for i in range(0, arrlen - 1):
        codearr += header+str(arr[i])+footer + ','
    if (arrlen > 0):
        codearr += header+str(arr[arrlen - 1])+footer
    codearr += ']'
    return codearr


#there are two copies of this function
def get_pixel(x, y):
    width,height = pyautogui.size()
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
    #print(target)
    #print(str(xl)+','+str(yl)+','+str(xr)+','+str(yr))
    p=im.getpixel(target)
    return p

#there are 2 copies of this function
def coord_to_percent(x,y):
    adjx = x - SV.getscreenx()
    adjy = y - SV.getscreeny()
    percentx = adjx/SV.getxwidth()
    percenty = adjy/SV.getyheight()
    return percentx,percenty

def percent_to_absolute(cx, cy):
    x = SV.getxwidth() * cx + SV.getscreenx()
    y = SV.getyheight() * cy + SV.getscreeny()
    return x,y

def get_percentcoords():
    x, y = pyautogui.position()
    return coord_to_percent(x, y)

def get_color(x, y):
    color = get_pixel(x, y)
    colorstr = str(color)
    if(isMac):
        colorstr = colorstr[1:-6]
    else:
        colorstr = colorstr[1:-1]
    return colorstr


def record_point(functionname, datatype):
    x, y = pyautogui.position()
    cx,cy = coord_to_percent(x,y)
    pointstr = functionname + "(" + str(cx) + ", " + str(cy)
    if(datatype == 1): #point
        return pointstr + ")\n"
    elif(datatype == 2): #color
        colorstr = get_color(x,y)
        return pointstr + ", " + colorstr + ")\n"
def record_area(functionname, cx1, cy1, cx2, cy2):
    pointstr = functionname + "("+str(cx1)+", "+str(cy1)+", "+str(cx2)+", "+str(cy2)+")\n"
    return pointstr


def record_mult(statement, evallist, nevals):
    head = 'while '
    for i in range(0, nevals-1):
        head+='(not ' + evallist[i] +') ' + statement +' \\\n'
    head+= '(not ' + evallist[nevals-1] +'):\n'

    return head

def mult_compare(evallist, statement = 'and'):
    compareblock = '\treturn '
    evallistlen = len(evallist)
    for i in range(0, evallistlen-1):
        compareblock+='\t'+evallist[i] +' ' +statement +' \\\n'
    if(evallistlen > 0):
        compareblock+='\t'+evallist[evallistlen-1]+' \n'
    return compareblock

def extraoptions(funcname,funcbody):
    print('INCOMPLETE')

def checktimeout(funcstring):
    while True:
        hastimeout = input('Include timeout? Y/N: ')
        if (hastimeout == 'N') or (hastimeout == 'n'):
            funcstring += '\trobot_sleep(250)'
            break
        elif (hastimeout == 'Y') or (hastimeout == 'y'):
            timeoutsecs = input('Enter timeout length (seconds):')
            try:
                int(timeoutsecs)
                funcstring = 'timeout = ' + timeoutsecs + '\n' + funcstring
                funcstring += '\tif(timeout>0):\n'
                funcstring += '\t\trobot_sleep(250)\n\t\ttimeout-=0.25\n'
                break
            except NameError:
                print('invalid timeout value')
    return funcstring

def grab_phone_area(cx1, cy1, cx2, cy2):
    x1, y1 = percent_to_absolute(cx1, cy1)
    x2, y2 = percent_to_absolute(cx2, cy2)
    width = x2-x1
    height = y2-y1
    print(str(x1) + ', ' + str(y1)+', ' + str(x2) + ', ' + str(y2))
    img = ImageGrab.grab(bbox=(x1,y1,x2,y2), childprocess=False)
    if(SV.isMac):
        img = img.crop((0,0,width*2,height*2)) #this has to be *2 because resolution is x 2
    img = img.crop((0,0,width,height))
    return img

#-------------------create functions-------------------

def create_detectfunction(funcname, colorconstr='C.Color',evaluator='color_comp'):
    cxlist = []
    cylist = []
    clist = []
    print('creating detectfunction ' + funcname)
    contextdetect = 'def ' + funcname + '():\n'
    while True:
        print('to use the default detect function press D')
        exittext = input('mouse over wait point and hit enter: (X to exit)')
        if (exittext == 'X') or (exittext == 'x'):
            break
        if (exittext == 'D') or (exittext == 'd'):
            contextdetect += '\tMN.robot_sleep(500)\n'
            contextdetect += '\treturn True\n'
            return contextdetect
        x, y = pyautogui.position()
        cx, cy = coord_to_percent(x, y)
        c = get_color(x, y)
        cxlist.append(cx)
        cylist.append(cy)
        clist.append(c)
        print('point recorded')

    contextdetect+='\t' + funcname + '.cxlist = '+array_to_codearr(cxlist)+'\n'
    contextdetect+='\t' + funcname + '.cylist = '+array_to_codearr(cylist)+'\n'
    contextdetect+='\t' + funcname + '.clist = '+array_to_codearr(clist, header = 'C.Color(', footer=')')+'\n'
    contextdetect+='\treturn all(map('+evaluator+', ' + funcname + '.cxlist, ' + funcname + '.cylist, ' +funcname + '.clist))\n'
    return contextdetect +'\n'

def create_clickfunction(funcname,clickfunction = 'click_screen_area'):
    input('select top left corner & press enter:')
    cx1, cy1 = get_percentcoords()
    input('select bottom right corner & press enter:')
    cx2, cy2 = get_percentcoords()
    clickfunction += '('+str(cx1)+', '+str(cy1)+', '+str(cx2)+', '+str(cy2)+')'
    return 'def '+funcname+'():\n\t'+clickfunction+'\n'

def create_button(buttonname,buttonconstr='B.Button'):
    buttondetectname = 'detect_' + buttonname
    print('Creating button detector ' + buttondetectname)
    buttondetectfunc = create_detectfunction(buttondetectname, evaluator='MN.color_comp')
    buttonclickname = 'click_' + buttonname
    print('Creating button clicker ' + buttonclickname)
    buttonclickfunc = create_clickfunction(buttonclickname, clickfunction='MN.click_screen_area')
    buttonconstr += '(' + buttondetectname + ', ' + buttonclickname + ')'
    buttonassignment = buttonname + ' = ' + buttonconstr
    buttondefs = buttondetectfunc + '\n' + buttonclickfunc + '\n'
    return buttondefs+buttonassignment+'\n'

def create_context(contextname, buttonconstr = 'B.Button', contextconstr = 'Context'):
    addbutton = input('Is this context accesible via a button? (Y/N)')
    buttondefs = None
    buttonname = None
    if (addbutton == 'Y') or (addbutton == 'y'):
        buttonname = contextname + 'button'
        buttondefs = create_button(buttonname)

    contextdetectname = 'detect_' + contextname
    contextdetector = create_detectfunction(contextdetectname, evaluator='MN.color_comp')
    fullstring = ''
    if (buttondefs != None):
        fullstring += buttondefs
    fullstring += contextdetector
    fullstring += contextname + ' = ' + contextconstr + '(\"' + contextname + '\", ' + str(buttonname) + ', ' + contextdetectname + ')\n'
    return fullstring +'\n'

def create_image_template(objectname):
    templatelist = []
    print('creating template images...')
    while True:
        print('Press X to exit')
        tlc = input('select top left corner & press enter:')
        if(tlc == 'X'):
            break
        cx1, cy1 = get_percentcoords()
        brc = input('select bottom right corner & press enter:')
        if (brc == 'X'):
            break
        cx2, cy2 = get_percentcoords()
        im = grab_phone_area(cx1,cy1,cx2,cy2)
        filename = input('choose a filename **.png for the template: ')
        if(filename == ''):
            break
        filepath = 'images/templates/'+filename+'.png'
        im.save(filepath,'PNG')
        templatelist.append(filepath)
        print('saved file ' + filename + '.png')
    return templatelist

def create_image_area(funcname = 'grab_phone_area'):
    print('creating image scan area: ')
    input('select top left corner & press enter:')
    cx1, cy1 = get_percentcoords()
    input('select bottom right corner & press enter:')
    cx2, cy2 = get_percentcoords()
    return record_area(funcname, cx1, cy1, cx2, cy2)

def create_relative_click_area(funcname = 'click_screen_area', iterate = True):
    print('Press X to exit')
    origin = input('mouse over origin point & hit enter: ')
    if (origin == 'X'):
        return ''
    cxorigin, cyorigin = get_percentcoords()
    clickfunctions = ''
    while True:
        tlc = input('mouse over relative point top left corner & hit enter: ')
        if (tlc == 'X'):
            break
        cx, cy = get_percentcoords()
        rcx1 = cx - cxorigin
        rcy1 = cy - cyorigin
        brc = input('mouse over relative point bottom right corner & hit enter: ')
        if (brc == 'X'):
            break
        cx, cy = get_percentcoords()
        rcx2 = cx - cxorigin
        rcy2 = cy - cyorigin
        clickfunctions += (funcname + '(' + str(rcx1) + '+cx, ' + str(rcy1) + '+cy, ' + str(rcx2) + '+cx, ' + str(
            rcy2) + '+cy)\n')
        print('point recorded')
        if not iterate:
            break
    return clickfunctions

def create_context_links(contextname):
    createlinks = input('Create Context Links? (Y/N) ')
    linkstring = ''
    if (createlinks == 'Y') or (createlinks == 'y'):
        connectionadder = 'add_connection'
        print('X/Enter to exit')
        while True:
            linkedcontextname = input('Enter Linked Context Name: ')
            if (linkedcontextname == 'X') or (linkedcontextname == 'x') or (linkedcontextname == ''):
                break
            else:
                linkstring += contextname + '.' + connectionadder + '(' + linkedcontextname + ')\n'
                continue
    return linkstring



def mousecolor_finder():

    commandarr = []
    extramode = False
    colorconstr = 'C.Color'


    print('Reccomended usage: run an android simulator in view only mode and run this program from the terminal')
    print('Make sure you configure the system variables in config/SystemVars.py!')
    print('Note: Use B instead of C whenever possible to increase randomness')
    print("--Key--")
    print('CONFIG: Set the screen start and end locations')
    print('EXTRA: Toggle extra function creation options')
    print('P: click a point outside the phone screen')
    print('W: wait for a point outside the phone screen')
    print("C: Mouse Click Location within phone screen")
    print("B: Mouse Click Box within phone screen")
    print('R: Relative Location within phone screen')
    print("WP: Point Wait Location within phone screen")
    print("WM: Wait for Multiple within phone screen")
    print('WO: Wait for At Least One within phone screen')
    print("IMGCONTEXT: Create a context that requires image screening")
    print('RELCONTEXT: Create a context that will require runtime initialization')
    print("CONTEXT: Create a new context")
    print("DETECT: Create a detect function")
    print("BUTTON: Create a new button")
    print("MANUAL: print relative coords")
    print("X/Enter: Exit")
    print('-------')

    while (True):
        funcstring = ""
        functionname = ""
        if(extramode):
            print('Extra function options are enabled')
        mode = input('Mouse over location & choose type: ')
        if(mode == 'CONFIG') or (mode == 'config'):
            input('select top left corner of screen & press enter:')
            x1, y1 = pyautogui.position()
            input('select bottom right corner of screen & press enter:')
            x2, y2 = pyautogui.position()
            xwidth = x2-x1
            print(xwidth)
            yheight = y2-y1
            print(yheight)
            SV.setscreenx(x1)
            SV.setscreeny(y1)
            SV.setxwidth(xwidth)
            SV.setyheight(yheight)
            print('screen dimensions are now set. screenx = ' +str(SV.getscreenx())+', screeny = '+str(SV.getscreeny())+
                  ', xwidth = '+str(SV.getxwidth())+', yheight = '+str(SV.getyheight()))
        elif(mode == 'EXTRA') or (mode == 'extra'):
            extramode = not extramode
        else:
            if(mode == 'P') or (mode == 'p'):
                if (extramode):
                    functionname = 'click_' + input('Enter your function name: click_')
                commandarr.append('P:')
                funcname = 'simple_click'
                x,y=pyautogui.position()
                funcstring+=(funcname+'('+str(x) +", "+str(y)+")")
                print('point recorded')
                commandarr.append(funcstring)
            elif(mode == 'W') or (mode == 'w'):
                if (extramode):
                    functionname = 'wait_' + input('Enter your function name: wait_')
                commandarr.append('W:')
                funcname = 'simple_wait'
                x,y=pyautogui.position()
                color = get_color(x,y)
                funcstring+=(funcname+'('+str(x)+','+str(y)+', '+color+')')
                print('point recorded')
                if (extramode):
                    funcstring = checktimeout(funcstring)
                else:
                    funcstring += '\trobot_sleep(250)'
                commandarr.append(funcstring)
            #1 == point, 2 == color
            elif(mode == 'C') or (mode == 'c'):
                if (extramode):
                    functionname = 'click_' + input('Enter your function name: click_')
                commandarr.append('C:')
                funcname = 'click_screen_loc'
                funcstring+=record_point(funcname, 1)
                print('point recorded')
                commandarr.append(funcstring)
            elif (mode == 'B') or (mode == 'b'):
                if (extramode):
                    functionname = 'click_' + input('Enter your function name: click_')
                commandarr.append('B:')
                funcname = 'click_screen_area'
                input('select top left corner & press enter:')
                cx1,cy1 = get_percentcoords()
                input('select bottom right corner & press enter:')
                cx2, cy2 = get_percentcoords()
                funcstring+=(record_area(funcname, cx1, cy1, cx2, cy2))
                print('point recorded')
                commandarr.append(funcstring)
            elif (mode == 'R') or (mode == 'r'):
                if (extramode):
                    functionname = 'click_' + input('Enter your function name: click_')
                commandarr.append('R: ')
                funcname = 'click_screen_area'
                input('mouse over origin point & hit enter: ')
                cxorigin, cyorigin = get_percentcoords()
                npoints = input('how many points would you like to choose?')
                for i in range(0,int(npoints)):
                    input('mouse over relative point top left corner & hit enter: ')
                    cx, cy = get_percentcoords()
                    rcx1 = cx - cxorigin
                    rcy1 = cy - cyorigin
                    input('mouse over relative point bottom right corner & hit enter: ')
                    cx, cy = get_percentcoords()
                    rcx2 = cx - cxorigin
                    rcy2 = cy - cyorigin
                    funcstring+=(funcname + '('+str(rcx1)+'+cx, '+str(rcy1)+'+cy, '+str(rcx2)+'+cx, '+str(rcy2)+'+cy)\n')
                    print('point recorded')
                commandarr.append(funcstring)
            elif (mode == 'WP') or (mode == 'wp'):
                if (extramode):
                    functionname = 'wait_' + input('Enter your function name: wait_')
                commandarr.append('WP:')
                funcname = 'wait_for_point'
                funcstring+=(record_point(funcname, 2))
                print('point recorded')
                if (extramode):
                    funcstring = checktimeout(funcstring)
                else:
                    funcstring += '\trobot_sleep(250)'
                commandarr.append(funcstring)

            elif (mode == 'WM') or (mode == 'wm'):
                if (extramode):
                    functionname = 'wait_' + input('Enter your function name: wait_')
                commandarr.append('WM:')
                evaluator = 'color_comp'
                statement = 'or'
                npoints = input('how many points would you like to choose?:')
                npoints = int(npoints)
                evallist = []
                for i in range(0, npoints):
                    input('choose point and hit enter:')
                    x,y = pyautogui.position()
                    cx,cy = coord_to_percent(x,y)
                    c = get_color(x,y)
                    funcvars = str(cx) + ', ' + str(cy) + ', ' + colorconstr + '(' + c + ')'
                    evallist.append(evaluator+'('+funcvars+')')
                    print('point recorded')
                funcstring+=(record_mult(statement, evallist, npoints))
                if (extramode):
                    funcstring = checktimeout(funcstring)
                else:
                    funcstring += '\trobot_sleep(250)'
                commandarr.append(funcstring)
            elif (mode == 'WO') or (mode == 'wo'):
                if (extramode):
                    functionname = 'wait_' + input('Enter your function name: wait_')
                commandarr.append('WO:')
                evaluator = 'color_comp'

                statement = 'and'
                npoints = input('how many points would you like to choose?:')
                npoints = int(npoints)
                evallist = []
                for i in range(0, npoints):
                    input('choose point and hit enter:')
                    x, y = pyautogui.position()
                    cx, cy = coord_to_percent(x, y)
                    c = get_color(x, y)
                    funcvars = str(cx) + ', ' + str(cy) + ', ' + colorconstr + '(' + c + ')'
                    evallist.append(evaluator + '(' + funcvars + ')')
                    print('point recorded')
                funcstring+=(record_mult(statement, evallist, npoints))
                if (extramode):
                    funcstring = checktimeout(funcstring)
                else:
                    funcstring += '\trobot_sleep(250)'
                commandarr.append(funcstring)


            # avoid using if possible
            # elif (mode == 'WI') or (mode == 'wi'):
            #     commandarr.append('WI:')
            #     funcname = 'wait_for_area'
            #     input('select top left corner & press enter:')
            #     cx1, cy1 = get_percentcoords()
            #     input('select bottom right corner & press enter:')
            #     cx2, cy2 = get_percentcoords()
            #     commandarr.append(record_area(funcname, cx1, cy1, cx2, cy2))
            elif (mode == 'CONTEXT') or (mode == 'context'):
                while True:
                    print('Press X/Enter to exit')
                    contextname = input('Enter Context Name: ')
                    if(contextname == 'X') or (contextname == 'x') or (contextname == ''):
                        break
                    commandarr.append('CONTEXT')
                    contextstr = create_context(contextname)
                    contextstr += create_context_links(contextname)
                    commandarr.append(contextstr)
            elif (mode == 'IMGCONTEXT') or (mode == 'imgcontext'):
                print('Press X/Enter to exit')
                contextname = input('Enter Context Name: ')
                if (contextname == 'X') or (contextname == 'x') or (contextname == ''):
                    break
                commandarr.append('IMGCONTEXT')
                findname = 'find_'+contextname
                print('creating find function: ' + findname)
                commandstr = 'def ' + findname +'(debug=False):\n'
                filepath = 'images/results/' + contextname + '.png'
                commandstr += "\tscanpath = \'"+filepath+"\'\n"
                while True:
                    specificarea = input('Scan specific area? (N = full screen) Y/N: ')
                    print('(specific area is not working atm need to make sure to scale the relative screen points in the image matching)')
                    if (specificarea == 'X') or (specificarea == 'x') or (specificarea == ''):
                        break
                    elif(specificarea == 'Y') or (specificarea == 'y'):
                        commandstr += '\tim = '+create_image_area(funcname = 'MN.grab_phone_area')
                        break
                    elif(specificarea == 'N') or (specificarea == 'n'):
                        commandstr += '\tim = MN.full_screen_shot()\n'
                        break

                commandstr+='\tim.save(scanpath,\'PNG\')\n'
                templatelist = create_image_template(contextname)
                templates = array_to_codearr(templatelist, header = '\'', footer = '\'')
                commandstr+='\tif(debug):\n'
                commandstr+='\t\treturn IM.match_template_debug(scanpath, ' + templates +', \''+contextname+'\')\n'
                commandstr+='\treturn IM.match_template(scanpath, '+ templates +')\n'
                contextconstr = 'ImageContext'
                detectname = 'detect_'+contextname
                commandstr += create_detectfunction(detectname,evaluator='MN.color_comp')
                commandstr+=contextname + ' = ' + contextconstr + '(\"' + contextname + '\", ' + detectname + ', ' + findname + ')\n'
                commandstr+=create_context_links(contextname)
                commandarr.append(commandstr)

            elif (mode == 'RELCONTEXT') or (mode == 'relcontext'):
                print('Press X/Enter to exit')
                contextname = input('Enter Context Name: ')
                if (contextname == 'X') or (contextname == 'x') or (contextname == ''):
                    break
                commandstr = ''
                clickfuncname = 'click_'+contextname
                commandstr += 'def ' + clickfuncname +'(cx, cy):\n'
                commandstr += '\t'+create_relative_click_area('MN.click_screen_area', iterate = False)
                detectname = 'detect_'+contextname
                commandstr += create_detectfunction(detectname, evaluator='MN.color_comp')
                contextconstr = 'RelativeContext'
                commandstr += contextname + ' = ' + contextconstr + '(\"' + contextname + '\", ' + clickfuncname + ', ' + detectname + ')\n'
                commandstr += create_context_links(contextname)
                commandarr.append(commandstr)

            elif (mode == 'BUTTON') or (mode == 'button'):
                buttonname = input('Choose a button name: ')
                buttonstr = ''
                buttonstr += create_button(buttonname)
                commandarr.append(buttonstr)
                continue
            elif (mode == 'DETECT') or (mode == 'detect'):
                funcname = input('Choose a name for your detect function detect_: ')
                detectstr = create_detectfunction('detect_'+funcname, evaluator = 'MN.color_comp')
                commandarr.append(detectstr)
                continue
            elif (mode == 'MANUAL') or (mode == 'manual'):
                while True:
                    try:
                        print(get_percentcoords())
                        time.sleep(0.25)
                    except KeyboardInterrupt:
                        break
                continue
            elif (mode == 'X') or (mode == 'x') or (mode == '\n') or (mode == ''):
                break




    print("------------------arrstart-------------------")
    for i in range(len(commandarr)-1, -1, -1):
        print(commandarr[i])
    print("------------------arrfinish-------------------")




if __name__ == '__main__':
    mousecolor_finder()

