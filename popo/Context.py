import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import copy
import util.MapNavigator as MN
import popo.Color as C
import popo.Button as B
import util.ImageMatcher as IM
import random
import time

def default_waitfunc():
    MN.robot_sleep(500)
    return True

class Context:
    def __init__(self, name, button, detector):
        self.name = name
        self.contextlist = []
        self.optionlist = []
        self.button = button
        self.detector = detector
        self.visited = False #will be used to implement traversal methods

    def getname(self):
        return self.name

    def add_connection(self, context):
        self.contextlist.append(context)

    def add_connections(self, contextlist):
        self.contextlist += contextlist

    def get_connection(self, name):
        for context in self.contextlist:
            if(context.getname()==name):
                return context
        print(name +' not found')
        return None

    def add_option(self, context):
        self.optionlist.append(context)

    def get_option(self, name):
        print('searching optionlist...')
        for context in self.optionlist:
            if(context.getname()==name):
                return context
        print(name +' not found')
        return None

    def get_context(self,name):
        return self.get_connection(name)

    def get_one_connection(self):
        return self.contextlist[0]

    def add_extrabutton(self, button):
        self.extrabutton = button

    def click_extrabutton(self):
        self.extrabutton.click()


    def detect(self):
        if(self.detector == None):
            return False
        return self.detector()

    def getbutton(self):
        return self.button
    def get_button(self):
        return self.getbutton()

    def setbutton(self, button):
        self.button = button

    def setdetector(self, detector):
        self.detector = detector

    def detect_button(self):
        return self.getbutton().detect()

    def click_button(self):
        selfbutton = self.getbutton()
        if not selfbutton.detect == None:
            if not selfbutton.detect():
                print('WARNING:' +self.name + ' button not detected!')
        selfbutton.click()

    def click(self):
        return self.click_button()
    def click_and_wait(self, timeout = 5, ontimeout=None):
        self.getbutton().click()
        return self.waitforload(timeout, ontimeout)


    def click_until(self, extraiterations = 1, ontimeout = None):
        self.click_button()
        while(not self.detect()) and extraiterations > 0:
            print('performing extra iteration for ' + self.name)
            self.click_button()
            extraiterations -= 1
        if(extraiterations == 0):
            if(ontimeout != None):
                ontimeout()

    def wait_for_button(self):
        return self.getbutton().waitforbuttonload()

    def waitforload(self, timeout = 5, ontimeout=None):
        while(not self.detect()):
            if(Context.detect_camelloadingscreen()):
                print('detected camelloadingscreen')
                MN.robot_sleep(4000)
            elif(Context.detect_waoclientsideload()):
                print('detected camelloadingscreen')
                MN.robot_sleep(4000)
            elif(Context.detect_waoserverfetch()):
                print('detected camelloadingscreen')
                MN.robot_sleep(4000)
            else:
                if(timeout>0):
                    MN.robot_sleep(350)
                    timeout -= 0.5
                    if(timeout % 1 == 0):
                        print('waiting for ' + self.getname()+' load... '+str(timeout))
                else:
                    print(self.getname() + ' timed out!')
                    if (ontimeout == None):
                        return self.return_context()
                    else:
                        return ontimeout()
        return self


    def wait_for_load(self,timeout=5,ontimeout=None):
        return self.waitforload(timeout, ontimeout)

    @staticmethod
    def waitformultiload(contextlist, timeout = 5, ontimeout = None):
        timeoutstr = ''
        for context in contextlist:
            timeoutstr += context.name + ' '
        while(timeout > 0):
            if (Context.detect_camelloadingscreen()):
                print('detected camelloadingscreen')
                MN.robot_sleep(4000)
            elif (Context.detect_waoserverfetch()):
                print('detected waoserverfetch')
                MN.robot_sleep(4000)
            elif (Context.detect_waoclientsideload()):
                print('detected waoclientsideload')
                MN.robot_sleep(4000)
            else:
                for context in contextlist:
                    if(context.detect()):
                        return context
                    else:
                        MN.robot_sleep(350)
                        timeout -= 0.5
                        if (timeout % 1 == 0):
                            print('waiting for or(' + timeoutstr + ') load... ' + str(timeout))

        print(timeoutstr + 'timed out!')
        if (ontimeout == None):
            return None
        else:
            ontimeout()


    def reset_context(self):
        print('resetting context from start')
        phonehomescreen = self.default_context()
        phonehomescreen.click_and_wait(ontimeout=self.blank_timeout)
        for i in range(0,3):
            if not phonehomescreen.detect():
                phonehomescreen.click_and_wait(ontimeout=self.blank_timeout)
        MN.robot_sleep(1000)
        phonehomescreen.click_extrabutton()
        MN.robot_sleep(4000)
        phonehomescreen.click_and_wait(ontimeout=self.blank_timeout)
        cityview = phonehomescreen.get_connection('cityview').click_and_wait()
        tunnel = cityview.tunnel_context(self.name)
        print('tunnelling back')
        print(tunnel)
        for context in tunnel:
            print(context.name + '->', end = '')
            contextbutton = context.get_button()
            if contextbutton is not None:
                print(contextbutton)
                if contextbutton.accessor is not None:
                    context.click_and_wait(ontimeout=self.blank_timeout)
            else:
                print('no button for ' + context.name)
        print()
        if self.detect():
            return self
        else:
            print('reset unsuccesful!')
            MN.close_memu()
            MN.robot_sleep(4000)
            MN.default_process()
            MN.close_memu()
            exit(0)

    def check_tunnel_context(self, findname):
        if (self.visited == True):
            print(self.name + ' already visited')
            return None
        else:
            print('visiting : ' + self.name)
            self.visited = True
            if (self.name == findname):
                print('found ' + findname + '!')
                return [self]
            else:
                tunnel = self.tunnel_context(findname)
                if tunnel is not None:
                    return [self] + tunnel
                else:
                    return None

    def tunnel_context(self, findname):
        print('tunneling to ' + findname)
        for context in self.contextlist:
            checkresult = context.check_tunnel_context(findname)
            if checkresult is not None:
                return checkresult
            else:
                print(findname + ' not found in ' + context.name)
        return None




    def return_context(self):
        if (Context.detect_waocrash() or Context.detect_fullwaocrash()):
            MN.close_memu()
            MN.open_memu()
            return self.reset_context()
        print('returning to context: '+self.name)
        found = self.cycle_contexts()
        if found is None:
            found = self.reset_context()
        return found

    def cycle(self):
        for context in self.contextlist:
            contbutton = context.getbutton()
            if (contbutton != None):
                contbutton.click()
                self.waitforload()
                self.return_context()
                return

    def blank_timeout(self):
        print(self.name + ' blank timeout!')
        return None

    def cycle_contexts(self):
        if (self.detect()):
            print('found context!')
            return self
        selfbutton = self.get_button()
        if(selfbutton != None):
            if (selfbutton.detect != None):
                if (selfbutton.detect()):
                    print('found original button')
                    selfbutton.click()
                    if self.waitforload(ontimeout = self.blank_timeout) is not None:
                        return self
        firstcontextlist = []
        for context in self.contextlist:
            print(context.name)
            if (context.detect()):
                print('detected!')
                returncontext = context.get_connection(self.name)
                if (returncontext == None):
                    print('detected context not in context list')
                else:
                    returncontextbutton = returncontext.getbutton()
                    if (returncontextbutton.accessor == None):
                        print('no button to access detected context')
                    else:
                        returncontextbutton.click()
                        if returncontext.waitforload(ontimeout = self.blank_timeout) is not None:
                            return self
            firstcontextlist.append(context)
        for context in firstcontextlist:
            print(context.name)
            for cont in context.contextlist:
                print('\t' + cont.name)
                if (cont.detect()):
                    print('detected ' + cont.name + '!')
                    print('grabbing ' + context.name + ' from ' + cont.name)
                    firstreturncontext = cont.get_connection(context.name)
                    if (firstreturncontext == None):
                        print('could not find ' + context.name + ' in ' + cont.name)
                    else:
                        firstreturncontextbutton = firstreturncontext.getbutton()
                        if (firstreturncontextbutton != None):
                            if (firstreturncontextbutton.accessor == None):
                                print('no button to access detected context')
                            else:
                                firstreturncontextbutton.click()
                                if firstreturncontext.wait_for_load(ontimeout = self.blank_timeout):
                                    returncontext = context.get_connection(self.name)
                                    if (returncontext == None):
                                        print('could not find path from ' + context.name + ' to ' + self.name)
                                    else:
                                        returncontextbutton = returncontext.getbutton()
                                        if (returncontextbutton.accessor == None):
                                            print('no button to access detected context')
                                        else:
                                            returncontextbutton.click()
                                            if returncontext.waitforload(ontimeout=self.blank_timeout) is not None:
                                                print('return context complete!')
                                                return self
                                            else:
                                                print(context.name + ' button unsuccessfull')
                                else:
                                    print(firstreturncontext.name + ' button unsuccessfull')

        if(self.detect()):
            return self
        else:
            print('unable to find context')
            return None

    def tostr(self, spaces):
        return (spaces*'\t')+'[' + self.name + ': ' + str(self.button) + ', ' + str(self.detector) + ']\n'

    def tostrrec(self, spaces):
        printstr = self.tostr(spaces)
        if(self.visited == True):
            return printstr
        self.visited = True
        for context in self.contextlist:
            if(context.visited == False):
                printstr += context.tostrrec(spaces+1)
            else:
                printstr += context.tostr(spaces+1)
        return printstr

    def full_print(self):
        visitedlist = []
        printstr = self.tostrrec(0)
        print(printstr)
        self.resetvisits()

    def __str__(self):
        printstr = self.tostr(0)
        for context in self.contextlist:
            printstr+=context.tostr(1)
        return printstr

    def resetvisits(self):
        self.visited = False
        for context in self.contextlist:
            if(context.visited == True):
                context.resetvisits()


    @staticmethod
    def detect_camelloadingscreen():
        Context.detect_camelloadingscreen.cxlist = [0.455, 0.57875, 0.4425, 0.24375, 0.39375, 0.63375, 0.8525]
        Context.detect_camelloadingscreen.cylist = [0.74375, 0.5546875, 0.52578125, 0.50390625, 0.4328125, 0.46328125,
                                            0.0796875]
        Context.detect_camelloadingscreen.clist = [C.Color(0, 0, 0), C.Color(153, 51, 34), C.Color(255, 187, 34),
                                           C.Color(153, 51, 34), C.Color(0, 0, 0), C.Color(255, 187, 34),
                                           C.Color(0, 0, 0)]
        return all(map(MN.color_comp, Context.detect_camelloadingscreen.cxlist, Context.detect_camelloadingscreen.cylist,
                       Context.detect_camelloadingscreen.clist))
    @staticmethod
    def detect_waoclientsideload():
        return MN.color_comp(0.38, 0.5359375, C.Color(0, 0, 0)) and \
                MN.color_comp(0.17375, 0.26171875, C.Color(0, 0, 0)) and \
                MN.color_comp(0.37625, 0.4765625, C.Color(238, 189, 121)) and \
                MN.color_comp(0.71625, 0.46171875, C.Color(252, 220, 148)) and \
                MN.color_comp(0.36625, 0.39765625, C.Color(209, 152, 88))

    @staticmethod
    def detect_winterwaoserverfetch():
        Context.detect_winterwaoserverfetch.cxlist = [0.34875, 0.91375, 0.7425, 0.735, 0.395, 0.07, 0.945]
        Context.detect_winterwaoserverfetch.cylist = [0.75703125, 0.7046875, 0.23203125, 0.3640625, 0.5109375,
                                                      0.0546875,
                                                      0.8140625]
        Context.detect_winterwaoserverfetch.clist = [C.Color(110, 151, 169), C.Color(126, 153, 164),
                                                     C.Color(79, 105, 118),
                                                     C.Color(18, 32, 34), C.Color(8, 7, 9), C.Color(63, 107, 123),
                                                     C.Color(12, 26, 33)]
        return all(
            map(MN.color_comp, Context.detect_winterwaoserverfetch.cxlist, Context.detect_winterwaoserverfetch.cylist,
                Context.detect_winterwaoserverfetch.clist))
    @staticmethod
    def detect_waoserverfetch():
        Context.detect_waoserverfetch.cxlist = [0.64125, 0.5875, 0.38125, 0.17375, 0.36875, 0.75, 0.855, 0.915]
        Context.detect_waoserverfetch.cylist = [0.1375, 0.14140625, 0.12890625, 0.44375, 0.73984375, 0.59609375, 0.7234375,
                                        0.8234375]
        Context.detect_waoserverfetch.clist = [C.Color(183, 154, 145), C.Color(73, 47, 41), C.Color(55, 47, 31),
                                       C.Color(26, 26, 26), C.Color(36, 42, 43), C.Color(7, 2, 1), C.Color(48, 49, 50),
                                       C.Color(43, 45, 48)]
        return all(
            map(MN.color_comp, Context.detect_waoserverfetch.cxlist, Context.detect_waoserverfetch.cylist, Context.detect_waoserverfetch.clist)) or Context.detect_winterwaoserverfetch()

    @staticmethod
    def detect_waocrash():
        Context.detect_waocrash.cxlist = [0.12, 0.90625, 0.4325, 0.945, 0.9575, 0.2125, 0.65125, 0.54, 0.475, 0.44375]
        Context.detect_waocrash.cylist = [0.52734375, 0.47734375, 0.51796875, 0.0625, 0.6953125, 0.75390625, 0.7546875,
                                  0.17578125, 0.4609375, 0.5625]
        Context.detect_waocrash.clist = [C.Color(238, 238, 238), C.Color(238, 238, 238), C.Color(238, 238, 238),
                                 C.Color(0, 16, 32), C.Color(0, 35, 48), C.Color(0, 22, 30), C.Color(0, 66, 74),
                                 C.Color(41, 54, 62), C.Color(238, 238, 238), C.Color(238, 238, 238)]
        return all(map(MN.color_comp, Context.detect_waocrash.cxlist, Context.detect_waocrash.cylist, Context.detect_waocrash.clist))
    @staticmethod
    def detect_fullwaocrash():
        Context.detect_fullwaocrash.cxlist = [0.0575, 0.23875, 0.9675, 0.76625, 0.4875, 0.03, 0.23, 0.53125, 0.82875, 0.96625,
                                      0.74625, 0.52625, 0.3925, 0.25, 0.1275]
        Context.detect_fullwaocrash.cylist = [0.0328125, 0.0421875, 0.03359375, 0.040625, 0.01953125, 0.96640625, 0.96640625,
                                      0.9546875, 0.95, 0.94921875, 0.4546875, 0.4546875, 0.45390625, 0.44921875,
                                      0.44921875]
        Context.detect_fullwaocrash.clist = [C.Color(0, 0, 0), C.Color(0, 0, 0), C.Color(0, 0, 0), C.Color(0, 0, 0),
                                     C.Color(0, 0, 0), C.Color(0, 0, 0), C.Color(0, 0, 0), C.Color(0, 0, 0),
                                     C.Color(0, 0, 0), C.Color(0, 0, 0), C.Color(0, 0, 0), C.Color(0, 0, 0),
                                     C.Color(0, 0, 0), C.Color(0, 0, 0), C.Color(0, 0, 0)]
        return all(
            map(MN.color_comp, Context.detect_fullwaocrash.cxlist, Context.detect_fullwaocrash.cylist, Context.detect_fullwaocrash.clist))

    @staticmethod
    def default_context():
        contextlist = []
        def detect_returnbutton():
            return MN.color_comp(0.08875, 0.01484375, C.Color(140, 124, 91)) and \
                   MN.color_comp(0.0475, 0.0234375, C.Color(73, 60, 40)) and \
                   MN.color_comp(0.03625, 0.0359375, C.Color(147, 131, 98))

        def click_returnbutton():
            MN.click_screen_area(0.02, 0.0125, 0.095, 0.04375)

        returnbutton = B.Button(detect_returnbutton, click_returnbutton)

        def detect_cityview():
            detect_cityview.cxlist = [0.3575, 0.18875, 0.8025, 0.105, 0.0725, 0.06875]
            detect_cityview.cylist = [0.0640625, 0.06015625, 0.06875, 0.5609375, 0.5484375, 0.96015625]
            detect_cityview.clist = [C.Color(109, 6, 0), C.Color(166, 12, 0), C.Color(0, 33, 47), C.Color(38, 21, 13),
                                     C.Color(255, 253, 236), C.Color(191, 194, 77)]
            return all(map(MN.color_comp, detect_cityview.cxlist, detect_cityview.cylist, detect_cityview.clist))

        def detect_phonehomescreenreturnbutton():
            detect_phonehomescreenreturnbutton.cxlist = [0.4275]
            detect_phonehomescreenreturnbutton.cylist = [0.51875]
            detect_phonehomescreenreturnbutton.clist = [C.Color(27, 39, 41)]
            return all(
                map(MN.color_comp, detect_phonehomescreenreturnbutton.cxlist, detect_phonehomescreenreturnbutton.cylist,
                    detect_phonehomescreenreturnbutton.clist))

        def click_phonehomescreenreturnbutton():
            MN.click_screen_area(0.4425, 0.5125, 0.5225, 0.5265625)

        phonehomescreenreturnbutton = B.Button(detect_phonehomescreenreturnbutton, click_phonehomescreenreturnbutton)

        def detect_phonehomescreenreturn():
            detect_phonehomescreenreturn.cxlist = []
            detect_phonehomescreenreturn.cylist = []
            detect_phonehomescreenreturn.clist = []
            return all(map(MN.color_comp, detect_phonehomescreenreturn.cxlist, detect_phonehomescreenreturn.cylist,
                           detect_phonehomescreenreturn.clist))

        phonehomescreenreturn = Context("phonehomescreenreturn", phonehomescreenreturnbutton,
                                        detect_phonehomescreenreturn)



        def detect_memucrash():
            detect_memucrash.cxlist = [0.12875, 0.12875, 0.345, 0.555, 0.63125, 0.75125, 1.03, 0.85375, 0.52125,
                                       0.21625, 0.875]
            detect_memucrash.cylist = [0.38203125, 0.38203125, 0.5109375, 0.38046875, 0.4171875, 0.38359375, 0.51640625,
                                       0.51171875, 0.17109375, 0.0734375, 0.61328125]
            detect_memucrash.clist = [C.Color(0, 16, 13), C.Color(0, 16, 13), C.Color(27, 39, 41), C.Color(0, 16, 13),
                                      C.Color(27, 39, 41), C.Color(0, 16, 13), C.Color(27, 39, 41), C.Color(27, 39, 41),
                                      C.Color(103, 124, 143), C.Color(0, 18, 51), C.Color(1, 83, 112)]
            return all(map(MN.color_comp, detect_memucrash.cxlist, detect_memucrash.cylist, detect_memucrash.clist))

        memucrash = Context("memucrash", None, detect_memucrash)

        def detect_wintermapview():
            detect_wintermapview.cxlist = [0.3875, 0.90125, 0.92875, 0.055, 0.0425]
            detect_wintermapview.cylist = [0.06328125, 0.06953125, 0.6609375, 0.759375, 0.67109375]
            detect_wintermapview.clist = [C.Color(97, 6, 0), C.Color(0, 33, 47), C.Color(232, 232, 232),
                                          C.Color(83, 67, 50), C.Color(110, 44, 49)]
            return all(map(MN.color_comp, detect_wintermapview.cxlist, detect_wintermapview.cylist,
                           detect_wintermapview.clist))

        def detect_mapview():
            return (MN.color_comp(0.305, 0.0109375, C.Color(21, 28, 26)) and
                   MN.color_comp(0.38875, 0.065625, C.Color(97, 6, 0)) and
                   MN.color_comp(0.03875, 0.66484375, C.Color(109, 43, 51)) and
                   MN.color_comp(0.06625, 0.76015625, C.Color(92, 76, 51)) and
                   MN.color_comp(0.0575, 0.77890625, C.Color(184, 168, 127)) and
                   MN.color_comp(0.91875, 0.7640625, C.Color(208, 167, 101)) and
                   MN.color_comp(0.955, 0.765625, C.Color(203, 162, 96)) and
                   MN.color_comp(0.92625, 0.66015625, C.Color(68, 68, 68)) and
                   MN.color_comp(0.12, 0.959375, C.Color(137, 79, 31)) and
                   MN.color_comp(0.15375, 0.928125, C.Color(56, 61, 64)) and
                   MN.color_comp(0.05125, 0.92578125, C.Color(63, 67, 69)) and
                   MN.color_comp(0.07875, 0.96953125, C.Color(233, 233, 200))) or detect_wintermapview()

        def detect_marchsetoutbutton():
            detect_marchsetoutbutton.cxlist = [0.745, 0.90875]
            detect_marchsetoutbutton.cylist = [0.96015625, 0.959375]
            detect_marchsetoutbutton.clist = [C.Color(50, 75, 2), C.Color(67, 96, 5)]
            return all(map(MN.color_comp, detect_marchsetoutbutton.cxlist, detect_marchsetoutbutton.cylist,
                           detect_marchsetoutbutton.clist))

        def click_marchsetoutbutton():
            MN.click_screen_area(0.73, 0.93984375, 0.9375, 0.96953125)

        marchsetoutbutton = B.Button(detect_marchsetoutbutton, click_marchsetoutbutton)

        def detect_inputconfirmbutton():
            detect_inputconfirmbutton.cxlist = [0.95125, 0.84875]
            detect_inputconfirmbutton.cylist = [0.96328125, 0.96953125]
            detect_inputconfirmbutton.clist = [C.Color(255, 255, 255), C.Color(255, 255, 255)]
            return all(map(MN.color_comp, detect_inputconfirmbutton.cxlist, detect_inputconfirmbutton.cylist,
                           detect_inputconfirmbutton.clist))

        def click_inputconfirmbutton():
            MN.click_screen_area(0.87625, 0.946875, 0.935, 0.978125)

        inputconfirmbutton = B.Button(detect_inputconfirmbutton, click_inputconfirmbutton)

        def detect_rally5minbutton():
            detect_rally5minbutton.cxlist = [0.4675]
            detect_rally5minbutton.cylist = [0.1953125]
            detect_rally5minbutton.clist = [C.Color(22, 13, 13)]
            return all(map(MN.color_comp, detect_rally5minbutton.cxlist, detect_rally5minbutton.cylist,
                           detect_rally5minbutton.clist))

        def click_rally5minbutton():
            MN.click_screen_area(0.445, 0.18125, 0.48625, 0.203125)

        rally5minbutton = B.Button(detect_rally5minbutton, click_rally5minbutton)

        def detect_rally30minbutton():
            detect_rally30minbutton.cxlist = [0.88125]
            detect_rally30minbutton.cylist = [0.19609375]
            detect_rally30minbutton.clist = [C.Color(24, 13, 13)]
            return all(map(MN.color_comp, detect_rally30minbutton.cxlist, detect_rally30minbutton.cylist,
                           detect_rally30minbutton.clist))

        def click_rally30minbutton():
            MN.click_screen_area(0.86625, 0.18125, 0.905, 0.2015625)

        rally30minbutton = B.Button(detect_rally30minbutton, click_rally30minbutton)

        def detect_rally10minbutton():
            detect_rally10minbutton.cxlist = [0.68125]
            detect_rally10minbutton.cylist = [0.19296875]
            detect_rally10minbutton.clist = [C.Color(22, 13, 13)]
            return all(map(MN.color_comp, detect_rally10minbutton.cxlist, detect_rally10minbutton.cylist,
                           detect_rally10minbutton.clist))

        def click_rally10minbutton():
            MN.click_screen_area(0.65625, 0.18046875, 0.6975, 0.203125)

        rally10minbutton = B.Button(detect_rally10minbutton, click_rally10minbutton)

        def detect_rallyaddbeastbutton():
            detect_rallyaddbeastbutton.cxlist = [0.935]
            detect_rallyaddbeastbutton.cylist = [0.37265625]
            detect_rallyaddbeastbutton.clist = [C.Color(43, 35, 25)]
            return all(map(MN.color_comp, detect_rallyaddbeastbutton.cxlist, detect_rallyaddbeastbutton.cylist,
                           detect_rallyaddbeastbutton.clist))

        def click_rallyaddbeastbutton():
            MN.click_screen_area(0.895, 0.3578125, 0.94625, 0.38984375)

        rallyaddbeastbutton = B.Button(detect_rallyaddbeastbutton, click_rallyaddbeastbutton)

        def detect_rallyrebelsviewbutton():
            detect_rallyrebelsviewbutton.cxlist = [0.7075, 0.75, 0.66875]
            detect_rallyrebelsviewbutton.cylist = [0.3875, 0.4078125, 0.40703125]
            detect_rallyrebelsviewbutton.clist = [C.Color(251, 241, 157), C.Color(40, 24, 8), C.Color(40, 24, 8)]
            return all(map(MN.color_comp, detect_rallyrebelsviewbutton.cxlist, detect_rallyrebelsviewbutton.cylist,
                           detect_rallyrebelsviewbutton.clist))

        def click_rallyrebelsviewbutton():
            MN.click_screen_area(0.67375, 0.36953125, 0.75375, 0.41015625)

        rallyrebelsviewbutton = B.Button(detect_rallyrebelsviewbutton, click_rallyrebelsviewbutton)


        def detect_marchsetupview():
            detect_marchsetupview.cxlist = [0.48, 0.4875, 0.37, 0.13625, 0.90875, 0.61, 0.53375]
            detect_marchsetupview.cylist = [0.29609375, 0.09921875, 0.2015625, 0.20625, 0.9640625, 0.92421875,
                                                      0.38359375]
            detect_marchsetupview.clist = [C.Color(31, 22, 14), C.Color(19, 12, 6), C.Color(29, 21, 13),
                                                     C.Color(179, 80, 6), C.Color(59, 85, 1), C.Color(35, 34, 33),
                                                     C.Color(204, 179, 136)]
            return all(
                map(MN.color_comp, detect_marchsetupview.cxlist, detect_marchsetupview.cylist,
                    detect_marchsetupview.clist))

        def detect_rallysetupview():
            detect_rallysetupview.cxlist = [0.38125, 0.10125, 0.08125, 0.42625, 0.14, 0.49875, 0.91625, 0.585,
                                            0.135]
            detect_rallysetupview.cylist = [0.0328125, 0.1984375, 0.1109375, 0.128125, 0.26796875, 0.35234375,
                                            0.965625, 0.92265625, 0.92734375]
            detect_rallysetupview.clist = [C.Color(134, 35, 26), C.Color(60, 14, 9), C.Color(14, 13, 12),
                                           C.Color(25, 20, 19), C.Color(174, 75, 3), C.Color(31, 22, 14),
                                           C.Color(61, 86, 7), C.Color(32, 32, 31), C.Color(32, 32, 31)]
            return all(map(MN.color_comp, detect_rallysetupview.cxlist, detect_rallysetupview.cylist,
                           detect_rallysetupview.clist))


        rallyrebelsview = Context("rallyrebelsview", rallyrebelsviewbutton, detect_rallysetupview)
        rally5minview = Context('rally5minview', rally5minbutton, detect_rallysetupview)
        rally10minview = Context('rally10minview',rally10minbutton, detect_rallysetupview)
        rally30minview = Context('rally30minview', rally30minbutton, detect_rallysetupview)
        rallyaddbeastview = Context('rallyaddbeastview', rallyaddbeastbutton, detect_rallysetupview)
        rallyrebelsview.add_connection(rally5minview)
        rallyrebelsview.add_connection(rally10minview)
        rallyrebelsview.add_connection(rally30minview)
        rallyrebelsview.add_connection(rallyaddbeastview)
        rallyloopview = copy.copy(rallyrebelsview)
        rallyloopview.setbutton(None)
        rally5minview.add_connection(rallyloopview)
        rally10minview.add_connection(rallyloopview)
        rally30minview.add_connection(rallyloopview)
        rallyaddbeastview.add_connection(rallyloopview)



        def detect_battlerebelssuppressviewbutton():
            detect_battlerebelssuppressviewbutton.cxlist = [0.40125, 0.5975]
            detect_battlerebelssuppressviewbutton.cylist = [0.94296875, 0.9515625]
            detect_battlerebelssuppressviewbutton.clist = [C.Color(88, 14, 0), C.Color(94, 12, 4)]
            return all(map(MN.color_comp, detect_battlerebelssuppressviewbutton.cxlist,
                           detect_battlerebelssuppressviewbutton.cylist, detect_battlerebelssuppressviewbutton.clist))

        def click_battlerebelssurpressviewbutton():
            MN.click_screen_area(0.385, 0.93046875, 0.60875, 0.96171875)

        battlerebelssuppressviewbutton = B.Button(detect_battlerebelssuppressviewbutton,
                                                  click_battlerebelssurpressviewbutton)



        battlerebelssuppressview = Context("battlerebelssuppressview", battlerebelssuppressviewbutton,
                                           detect_marchsetupview)


        def detect_battlerebels1button():
            detect_battlerebels1button.cxlist = [0.58375, 0.83375]
            detect_battlerebels1button.cylist = [0.40390625, 0.40625]
            detect_battlerebels1button.clist = [C.Color(44, 39, 31), C.Color(47, 47, 39)]
            return all(map(MN.color_comp, detect_battlerebels1button.cxlist, detect_battlerebels1button.cylist,
                           detect_battlerebels1button.clist))

        def click_battlerebels1button():
            MN.click_screen_area(0.07875, 0.3578125, 0.92375, 0.44765625)

        battlerebels1button = B.Button(detect_battlerebels1button, click_battlerebels1button)

        def detect_battlerebelsx():
            detect_battlerebelsx.cxlist = [0.81125, 0.24625, 0.92375, 0.84375, 0.8975, 0.9025, 0.9075, 0.885, 0.86375,
                                           0.095, 0.21125, 0.0775]
            detect_battlerebelsx.cylist = [0.95234375, 0.95, 0.6578125, 0.54765625, 0.5109375, 0.4640625, 0.36328125,
                                           0.2703125, 0.2328125, 0.22890625, 0.55234375, 0.61640625]
            detect_battlerebelsx.clist = [C.Color(212, 187, 143), C.Color(211, 186, 143), C.Color(97, 75, 49),
                                          C.Color(114, 36, 8), C.Color(211, 186, 143), C.Color(90, 72, 48),
                                          C.Color(90, 72, 48), C.Color(97, 75, 49), C.Color(211, 186, 143),
                                          C.Color(211, 186, 143), C.Color(113, 35, 8), C.Color(97, 75, 48)]
            return all(map(MN.color_comp, detect_battlerebelsx.cxlist, detect_battlerebelsx.cylist,
                           detect_battlerebelsx.clist))

        battlerebels1 = Context("battlerebels1", battlerebels1button, detect_battlerebelsx)
        battlerebels1.add_connection(battlerebelssuppressview)


        def detect_battlerebelsviewbutton():
            detect_battlerebelsviewbutton.cxlist = [0.49625, 0.4525, 0.54]
            detect_battlerebelsviewbutton.cylist = [0.24453125, 0.2546875, 0.25625]
            detect_battlerebelsviewbutton.clist = [C.Color(159, 159, 159), C.Color(109, 192, 0), C.Color(109, 188, 4)]
            return all(map(MN.color_comp, detect_battlerebelsviewbutton.cxlist, detect_battlerebelsviewbutton.cylist,
                           detect_battlerebelsviewbutton.clist))

        def click_battlerebelsviewbutton():
            MN.click_screen_area(0.46375, 0.24375, 0.53375, 0.278125)

        battlerebelsviewbutton = B.Button(detect_battlerebelsviewbutton, click_battlerebelsviewbutton)

        def detect_battlerebelsview():
            detect_battlerebelsview.cxlist = [0.57875, 0.92625, 0.9425, 0.67, 0.64375, 0.36, 0.06875]
            detect_battlerebelsview.cylist = [0.328125, 0.328125, 0.40546875, 0.41328125, 0.03828125, 0.1375,
                                              0.21015625]
            detect_battlerebelsview.clist = [C.Color(88, 110, 19), C.Color(31, 31, 22), C.Color(200, 178, 131),
                                             C.Color(34, 33, 25), C.Color(99, 27, 23), C.Color(232, 240, 240),
                                             C.Color(26, 59, 68)]
            return all(map(MN.color_comp, detect_battlerebelsview.cxlist, detect_battlerebelsview.cylist,
                           detect_battlerebelsview.clist))

        battlerebelsview = Context("battlerebelsview", battlerebelsviewbutton, detect_battlerebelsview)
        battlerebelsview.add_connection(battlerebels1)



        def detect_ruinsviewbutton():
            detect_ruinsviewbutton.cxlist = [0.45375, 0.55125]
            detect_ruinsviewbutton.cylist = [0.60703125, 0.6046875]
            detect_ruinsviewbutton.clist = [C.Color(77, 110, 0), C.Color(80, 113, 0)]
            return all(map(MN.color_comp, detect_ruinsviewbutton.cxlist, detect_ruinsviewbutton.cylist,
                           detect_ruinsviewbutton.clist))

        def click_ruinsviewbutton():
            MN.click_screen_area(0.35625, 0.5890625, 0.63375, 0.62578125)

        ruinsviewbutton = B.Button(detect_ruinsviewbutton, click_ruinsviewbutton)


        ruinsview = Context("ruinsview", ruinsviewbutton, detect_mapview)
        ruinsview.add_connection(battlerebelsview)
        ruinsview.add_connection(rallyrebelsview)

        def detect_ruinsxinputviewbutton():
            detect_ruinsxinputviewbutton.cxlist = [0.44, 0.2475]
            detect_ruinsxinputviewbutton.cylist = [0.484375, 0.48671875]
            detect_ruinsxinputviewbutton.clist = [C.Color(166, 133, 84), C.Color(166, 133, 84)]
            return all(map(MN.color_comp, detect_ruinsxinputviewbutton.cxlist, detect_ruinsxinputviewbutton.cylist,
                           detect_ruinsxinputviewbutton.clist))

        def click_ruinsxinputviewbutton():
            MN.click_screen_area(0.23625, 0.47890625, 0.45625, 0.50078125)
            MN.typewrite('745')

        ruinsxinputviewbutton = B.Button(detect_ruinsxinputviewbutton, click_ruinsxinputviewbutton)

        def detect_ruinsxinputview():
            detect_ruinsxinputview.cxlist = [0.575, 0.72125, 0.3425, 0.4525, 0.865]
            detect_ruinsxinputview.cylist = [0.6125, 0.3953125, 0.48828125, 0.965625, 0.9703125]
            detect_ruinsxinputview.clist = [C.Color(81, 114, 2), C.Color(210, 185, 142), C.Color(166, 134, 84),
                                            C.Color(255, 255, 255), C.Color(255, 255, 255)]
            return all(map(MN.color_comp, detect_ruinsxinputview.cxlist, detect_ruinsxinputview.cylist,
                           detect_ruinsxinputview.clist))

        ruinsxinputview = Context("ruinsxinputview", ruinsxinputviewbutton, detect_ruinsxinputview)

        def detect_ruinsyinputviewbutton():
            detect_ruinsyinputviewbutton.cxlist = [0.63375, 0.7625]
            detect_ruinsyinputviewbutton.cylist = [0.490625, 0.43515625]
            detect_ruinsyinputviewbutton.clist = [C.Color(166, 133, 83), C.Color(210, 185, 142)]
            return all(map(MN.color_comp, detect_ruinsyinputviewbutton.cxlist, detect_ruinsyinputviewbutton.cylist,
                           detect_ruinsyinputviewbutton.clist))

        def click_ruinsyinputviewbutton():
            MN.click_screen_area(0.59, 0.4765625, 0.8275, 0.50078125)
            MN.typewrite('741')

        ruinsyinputviewbutton = B.Button(detect_ruinsyinputviewbutton, click_ruinsyinputviewbutton)

        ruinsyinputview = Context("ruinsyinputview", ruinsyinputviewbutton, detect_ruinsxinputview)




        def click_coordinputviewbutton():
            MN.click_screen_area(0.39125, 0.83046875, 0.6625, 0.84375)

        coordinputviewbutton = B.Button(None, click_coordinputviewbutton)

        def detect_coordinputview():
            detect_coordinputview.cxlist = [0.79, 0.22, 0.1825, 0.8, 0.6125, 0.38]
            detect_coordinputview.cylist = [0.3859375, 0.39609375, 0.596875, 0.59921875, 0.61171875, 0.06953125]
            detect_coordinputview.clist = [C.Color(210, 185, 142), C.Color(210, 185, 142), C.Color(210, 185, 142),
                                           C.Color(211, 186, 143), C.Color(59, 84, 0), C.Color(60, 11, 6)]
            return all(map(MN.color_comp, detect_coordinputview.cxlist, detect_coordinputview.cylist,
                           detect_coordinputview.clist))

        coordinputview = Context("coordinputview", coordinputviewbutton, detect_coordinputview)
        coordinputview.add_connection(ruinsxinputview)
        coordinputview.add_connection(ruinsyinputview)

        returncoordinputview = copy.copy(coordinputview)
        returncoordinputview.setbutton(inputconfirmbutton)
        ruinsxinputview.add_connection(returncoordinputview)
        ruinsyinputview.add_connection(returncoordinputview)

        coordinputview.add_connection(ruinsview)

        def detect_accountaccountviewbutton():
            detect_accountaccountviewbutton.cxlist = [0.18, 0.2275, 0.105]
            detect_accountaccountviewbutton.cylist = [0.48359375, 0.453125, 0.4890625]
            detect_accountaccountviewbutton.clist = [C.Color(237, 237, 237), C.Color(17, 8, 0), C.Color(39, 22, 4)]
            return all(
                map(MN.color_comp, detect_accountaccountviewbutton.cxlist, detect_accountaccountviewbutton.cylist,
                    detect_accountaccountviewbutton.clist))

        def click_accountaccountviewbutton():
            MN.click_screen_area(0.0925, 0.43984375, 0.23125, 0.5265625)

        accountaccountviewbutton = B.Button(detect_accountaccountviewbutton, click_accountaccountviewbutton)

        def detect_accountaccountview():
            detect_accountaccountview.cxlist = [0.62125, 0.4025, 0.66125, 0.6575, 0.32375, 0.3875, 0.46625, 0.64875,
                                                0.62375, 0.44875]
            detect_accountaccountview.cylist = [0.0328125, 0.03125, 0.32890625, 0.40078125, 0.48359375, 0.27265625,
                                                0.15859375, 0.6734375, 0.7578125, 0.8796875]
            detect_accountaccountview.clist = [C.Color(134, 32, 24), C.Color(135, 33, 24), C.Color(1, 73, 89),
                                               C.Color(121, 14, 0), C.Color(210, 186, 142), C.Color(210, 184, 142),
                                               C.Color(211, 187, 143), C.Color(83, 112, 1), C.Color(133, 17, 2),
                                               C.Color(209, 185, 142)]
            return all(map(MN.color_comp, detect_accountaccountview.cxlist, detect_accountaccountview.cylist,
                           detect_accountaccountview.clist))

        accountaccountview = Context("accountaccountview", accountaccountviewbutton, detect_accountaccountview)

        def detect_dailyrewardreceiptviewbutton():
            detect_dailyrewardreceiptviewbutton.cxlist = [0.3975, 0.62375]
            detect_dailyrewardreceiptviewbutton.cylist = [0.75390625, 0.77890625]
            detect_dailyrewardreceiptviewbutton.clist = [C.Color(92, 175, 35), C.Color(48, 108, 16)]
            return all(map(MN.color_comp, detect_dailyrewardreceiptviewbutton.cxlist,
                           detect_dailyrewardreceiptviewbutton.cylist, detect_dailyrewardreceiptviewbutton.clist))

        def click_dailyrewardreceiptviewbutton():
            MN.click_screen_area(0.34875, 0.753125, 0.64125, 0.784375)

        dailyrewardreceiptviewbutton = B.Button(detect_dailyrewardreceiptviewbutton, click_dailyrewardreceiptviewbutton)

        def detect_dailyrewardreceiptview():
            detect_dailyrewardreceiptview.cxlist = [0.2025, 0.7825, 0.6875, 0.7, 0.4725]
            detect_dailyrewardreceiptview.cylist = [0.3171875, 0.321875, 0.39140625, 0.2890625, 0.31015625]
            detect_dailyrewardreceiptview.clist = [C.Color(211, 185, 142), C.Color(211, 186, 143),
                                                   C.Color(165, 133, 83), C.Color(193, 4, 0), C.Color(112, 1, 0)]
            return all(map(MN.color_comp, detect_dailyrewardreceiptview.cxlist, detect_dailyrewardreceiptview.cylist,
                           detect_dailyrewardreceiptview.clist))

        dailyrewardreceiptview = Context("dailyrewardreceiptview", dailyrewardreceiptviewbutton,
                                         detect_dailyrewardreceiptview)

        def detect_dailyrewardcityviewbutton():
            detect_dailyrewardcityviewbutton.cxlist = [0.3975, 0.6325]
            detect_dailyrewardcityviewbutton.cylist = [0.75234375, 0.7625]
            detect_dailyrewardcityviewbutton.clist = [C.Color(91, 174, 34), C.Color(77, 142, 43)]
            return all(
                map(MN.color_comp, detect_dailyrewardcityviewbutton.cxlist, detect_dailyrewardcityviewbutton.cylist,
                    detect_dailyrewardcityviewbutton.clist))

        def click_dailyrewardcityviewbutton():
            MN.click_screen_area(0.3475, 0.7515625, 0.6475, 0.78203125)

        dailyrewardcityviewbutton = B.Button(detect_dailyrewardcityviewbutton, click_dailyrewardcityviewbutton)

        def detect_dailyrewardview():
            detect_dailyrewardview.cxlist = [0.22375, 0.77625, 0.7075, 0.22125, 0.39875, 0.18625]
            detect_dailyrewardview.cylist = [0.3609375, 0.36328125, 0.315625, 0.32109375, 0.75234375, 0.746875]
            detect_dailyrewardview.clist = [C.Color(209, 185, 141), C.Color(210, 186, 142), C.Color(46, 46, 38),
                                            C.Color(46, 46, 38), C.Color(89, 172, 32), C.Color(210, 185, 143)]
            return all(map(MN.color_comp, detect_dailyrewardview.cxlist, detect_dailyrewardview.cylist,
                           detect_dailyrewardview.clist))

        dailyrewardview = Context("dailyrewardview", None, detect_dailyrewardview)

        dailyrewardview.add_connection(dailyrewardreceiptview)

        def detect_adexitviewbutton():
            detect_adexitviewbutton.cxlist = [0.92375, 0.94]
            detect_adexitviewbutton.cylist = [0.075, 0.084375]
            detect_adexitviewbutton.clist = [C.Color(124, 4, 4), C.Color(124, 4, 4)]
            return all(map(MN.color_comp, detect_adexitviewbutton.cxlist, detect_adexitviewbutton.cylist,
                           detect_adexitviewbutton.clist))

        def click_adexitviewbutton():
            MN.click_screen_area(0.9225, 0.07421875, 0.95875, 0.0953125)

        adexitviewbutton = B.Button(detect_adexitviewbutton, click_adexitviewbutton)


        def detect_adview():
            detect_adview.cxlist = [0.0825, 0.3325, 0.72, 0.94125]
            detect_adview.cylist = [0.084375, 0.0859375, 0.090625, 0.08515625]
            detect_adview.clist = [C.Color(59, 2, 2), C.Color(59, 2, 2), C.Color(59, 2, 2), C.Color(124, 4, 4)]
            return all(map(MN.color_comp, detect_adview.cxlist, detect_adview.cylist, detect_adview.clist))

        adview = Context("adview", None, detect_adview)

        def detect_altadview():
            detect_altadview.cxlist = [0.17875, 0.77625, 0.925, 0.52375, 0.71375, 0.3675]
            detect_altadview.cylist = [0.15234375, 0.1578125, 0.15546875, 0.17109375, 0.065625, 0.06640625]
            detect_altadview.clist = [C.Color(59, 2, 2), C.Color(59, 2, 2), C.Color(159, 142, 106), C.Color(59, 2, 2),
                                      C.Color(74, 120, 140), C.Color(63, 7, 5)]
            return all(map(MN.color_comp, detect_altadview.cxlist, detect_altadview.cylist, detect_altadview.clist))

        altadview = Context("altadview", None, detect_altadview)

        def detect_altaltadview():
            detect_altaltadview.cxlist = [0.12125, 0.225, 0.785, 0.9025]
            detect_altaltadview.cylist = [0.11953125, 0.11640625, 0.12109375, 0.10625]
            detect_altaltadview.clist = [C.Color(59, 2, 2), C.Color(59, 2, 2), C.Color(59, 2, 2),
                                               C.Color(143, 126, 94)]
            return all(map(MN.color_comp, detect_altaltadview.cxlist, detect_altaltadview.cylist,
                           detect_altaltadview.clist))

        altaltadview = Context("altaltadview", None, detect_altaltadview)


        def detect_farmswitchconfirmbutton():
            return MN.color_comp(0.24375, 0.54921875, C.Color(68, 92, 2)) and \
                   MN.color_comp(0.40875, 0.55390625, C.Color(64, 97, 0))

        def click_farmswitchconfirmbutton():
            MN.click_screen_area(0.20625, 0.53828125, 0.43375, 0.5640625)
            process_blockers()

        farmswitchconfirmbutton = B.Button(detect_farmswitchconfirmbutton, click_farmswitchconfirmbutton)


        def detect_farmswitchconfirmwindow():
            detect_farmswitchconfirmwindow.cxlist = [0.2275, 0.41, 0.5925, 0.7725, 0.94125, 0.94, 0.93125, 0.9325]
            detect_farmswitchconfirmwindow.cylist = [0.553125, 0.55078125, 0.546875, 0.546875, 0.9359375, 0.68671875,
                                                     0.1078125, 0.03046875]
            detect_farmswitchconfirmwindow.clist = [C.Color(59, 84, 2), C.Color(67, 93, 2), C.Color(2, 68, 68),
                                                    C.Color(0, 72, 80), C.Color(123, 107, 79), C.Color(123, 108, 80),
                                                    C.Color(124, 108, 81), C.Color(8, 8, 7)]
            return all(map(MN.color_comp, detect_farmswitchconfirmwindow.cxlist, detect_farmswitchconfirmwindow.cylist,
                           detect_farmswitchconfirmwindow.clist))

        def detect_alreadyisposbutton():
            detect_alreadyisposbutton.cxlist = [0.84125]
            detect_alreadyisposbutton.cylist = [0.26015625]
            detect_alreadyisposbutton.clist = [C.Color(138, 122, 89)]
            return all(map(MN.color_comp, detect_alreadyisposbutton.cxlist, detect_alreadyisposbutton.cylist,
                           detect_alreadyisposbutton.clist))

        def click_alreadyisposbutton():
            MN.click_screen_area(0.81625, 0.2609375, 0.85875, 0.28515625)

        alreadyisposbutton = B.Button(detect_alreadyisposbutton, click_alreadyisposbutton)

        def detect_alreadyispos():
            detect_alreadyispos.cxlist = [0.65625, 0.3675]
            detect_alreadyispos.cylist = [0.3484375, 0.3453125]
            detect_alreadyispos.clist = [C.Color(93, 117, 63), C.Color(93, 117, 63)]
            return all(map(MN.color_comp, detect_alreadyispos.cxlist, detect_alreadyispos.cylist, detect_alreadyispos.clist))

        def detect_farm1posbutton():
            return MN.color_comp(0.33875, 0.28046875, C.Color(73, 29, 24))

        def click_farm1posbutton():
            MN.click_screen_area(0.15625, 0.39609375, 0.84125, 0.434375)

        farm1posbutton = B.Button(detect_farm1posbutton, click_farm1posbutton)

        def detect_farm1pos():
            return detect_farmswitchconfirmwindow()

        farm1pos = Context("farm1pos", farm1posbutton, detect_farm1pos)

        def detect_farm0posbutton():
            detect_farm0posbutton.cxlist = [0.14375, 0.37125, 0.85]
            detect_farm0posbutton.cylist = [0.346875, 0.34609375, 0.35]
            detect_farm0posbutton.clist = [C.Color(40, 62, 74), C.Color(45, 78, 108), C.Color(43, 70, 88)]
            return all(map(MN.color_comp, detect_farm0posbutton.cxlist, detect_farm0posbutton.cylist,
                           detect_farm0posbutton.clist))

        def click_farm0posbutton():
            MN.click_screen_area(0.1475, 0.32890625, 0.8575, 0.3703125)

        farm0posbutton = B.Button(detect_farm0posbutton, click_farm0posbutton)


        def detect_farm0pos():
            return detect_farmswitchconfirmwindow()

        farm0pos = Context("farm0pos", farm0posbutton, detect_farm0pos)



        def detect_farmswitchview():
            return MN.color_comp(0.2375, 0.2734375, C.Color(77, 30, 24)) and \
                   MN.color_comp(0.6725, 0.28125, C.Color(73, 29, 24)) and \
                   MN.color_comp(0.28, 0.6171875, C.Color(189, 171, 135)) and \
                   MN.color_comp(0.7425, 0.62734375, C.Color(187, 169, 134)) and \
                   MN.color_comp(0.81875, 0.27578125, C.Color(150, 130, 90))

        def detect_farms10button():
            detect_farms10button.cxlist = [0.1875, 0.19375, 0.19]
            detect_farms10button.cylist = [0.95703125, 0.94921875, 0.9375]
            detect_farms10button.clist = [C.Color(37, 139, 0), C.Color(249, 255, 251), C.Color(224, 33, 15)]
            return all(map(MN.color_comp, detect_farms10button.cxlist, detect_farms10button.cylist,
                           detect_farms10button.clist))

        def click_farms10button():
            MN.click_screen_area(0.1675, 0.93515625, 0.56625, 0.9640625)

        farms10button = B.Button(detect_farms10button, click_farms10button)



        def detect_farms9button():
            detect_farms9button.cxlist = [0.19, 0.18875, 0.19]
            detect_farms9button.cylist = [0.88828125, 0.8796875, 0.8703125]
            detect_farms9button.clist = [C.Color(117, 170, 219), C.Color(0, 0, 0), C.Color(117, 170, 219)]
            return all(
                map(MN.color_comp, detect_farms9button.cxlist, detect_farms9button.cylist, detect_farms9button.clist))

        def click_farms9button():
            MN.click_screen_area(0.16875, 0.86640625, 0.645, 0.89765625)

        farms9button = B.Button(detect_farms9button, click_farms9button)

        def detect_farms8button():
            detect_farms8button.cxlist = [0.19, 0.1875, 0.19]
            detect_farms8button.cylist = [0.82421875, 0.81328125, 0.80234375]
            detect_farms8button.clist = [C.Color(255, 0, 0), C.Color(0, 0, 255), C.Color(255, 255, 255)]
            return all(
                map(MN.color_comp, detect_farms8button.cxlist, detect_farms8button.cylist, detect_farms8button.clist))

        def click_farms8button():
            MN.click_screen_area(0.16875, 0.796875, 0.44375, 0.8296875)

        farms8button = B.Button(detect_farms8button, click_farms8button)

        def detect_farms7button():
            detect_farms7button.cxlist = [0.2, 0.17625]
            detect_farms7button.cylist = [0.75078125, 0.73984375]
            detect_farms7button.clist = [C.Color(125, 253, 56), C.Color(0, 0, 0)]
            return all(
                map(MN.color_comp, detect_farms7button.cxlist, detect_farms7button.cylist, detect_farms7button.clist))

        def click_farms7button():
            MN.click_screen_area(0.16125, 0.72734375, 0.51375, 0.7609375)

        farms7button = B.Button(detect_farms7button, click_farms7button)

        def detect_farms6button():
            detect_farms6button.cxlist = [0.1875, 0.19, 0.19]
            detect_farms6button.cylist = [0.66640625, 0.67890625, 0.68515625]
            detect_farms6button.clist = [C.Color(1, 0, 5), C.Color(0, 56, 251), C.Color(1, 0, 5)]
            return all(
                map(MN.color_comp, detect_farms6button.cxlist, detect_farms6button.cylist, detect_farms6button.clist))

        def click_farms6button():
            MN.click_screen_area(0.16875, 0.6609375, 0.48125, 0.69140625)

        farms6button = B.Button(detect_farms6button, click_farms6button)

        def detect_farms5button():
            detect_farms5button.cxlist = [0.185, 0.20125]
            detect_farms5button.cylist = [0.61328125, 0.60703125]
            detect_farms5button.clist = [C.Color(0, 152, 0), C.Color(0, 0, 206)]
            return all(
                map(MN.color_comp, detect_farms5button.cxlist, detect_farms5button.cylist, detect_farms5button.clist))

        def click_farms5button():
            MN.click_screen_area(0.1675, 0.59296875, 0.54875, 0.621875)

        farms5button = B.Button(detect_farms5button, click_farms5button)

        def detect_farms4button():
            detect_farms4button.cxlist = [0.19625, 0.18875]
            detect_farms4button.cylist = [0.54765625, 0.5328125]
            detect_farms4button.clist = [C.Color(24, 64, 247), C.Color(246, 53, 20)]
            return all(
                map(MN.color_comp, detect_farms4button.cxlist, detect_farms4button.cylist, detect_farms4button.clist))

        def click_farms4button():
            MN.click_screen_area(0.16625, 0.52421875, 0.5, 0.55390625)

        farms4button = B.Button(detect_farms4button, click_farms4button)

        def detect_farms3button():
            detect_farms3button.cxlist = [0.17875, 0.19125, 0.1925]
            detect_farms3button.cylist = [0.33671875, 0.33125, 0.33984375]
            detect_farms3button.clist = [C.Color(253, 206, 18), C.Color(251, 15, 12), C.Color(23, 42, 140)]
            return all(
                map(MN.color_comp, detect_farms3button.cxlist, detect_farms3button.cylist, detect_farms3button.clist))

        def click_farms3button():
            MN.click_screen_area(0.175, 0.32265625, 0.49875, 0.34921875)

        farms3button = B.Button(detect_farms3button, click_farms3button)

        def detect_farms2button():
            detect_farms2button.cxlist = [0.1825, 0.2025]
            detect_farms2button.cylist = [0.26953125, 0.26953125]
            detect_farms2button.clist = [C.Color(10, 2, 0), C.Color(238, 211, 8)]
            return all(
                map(MN.color_comp, detect_farms2button.cxlist, detect_farms2button.cylist, detect_farms2button.clist))

        def click_farms2button():
            MN.click_screen_area(0.1675, 0.253125, 0.4425, 0.284375)

        farms2button = B.Button(detect_farms2button, click_farms2button)

        def detect_farms1button():
            detect_farms1button.cxlist = [0.18, 0.205]
            detect_farms1button.cylist = [0.39375, 0.403125]
            detect_farms1button.clist = [C.Color(1, 1, 1), C.Color(249, 5, 2)]
            return all(
                map(MN.color_comp, detect_farms1button.cxlist, detect_farms1button.cylist, detect_farms1button.clist))

        def click_farms1button():
            MN.click_screen_area(0.1725, 0.38828125, 0.50625, 0.42265625)

        farms1button = B.Button(detect_farms1button, click_farms1button)

        def detect_farms0button():
            detect_farms0button.cxlist = [0.1775, 0.19625]
            detect_farms0button.cylist = [0.4671875, 0.471875]
            detect_farms0button.clist = [C.Color(255, 255, 255), C.Color(0, 0, 0)]
            return all(
                map(MN.color_comp, detect_farms0button.cxlist, detect_farms0button.cylist, detect_farms0button.clist))

        def click_farms0button():
            MN.click_screen_area(0.17, 0.4546875, 0.49875, 0.4875)

        farms0button = B.Button(detect_farms0button, click_farms0button)




        farms10 = Context("farms10", farms10button, detect_farmswitchview)
        farms10.add_connection(farm0pos)
        farms10.add_connection(farm1pos)
        farms10.add_connection(accountaccountview)




        farms9 = Context("farms9", farms9button, detect_farmswitchview)
        farms9.add_connection(farm0pos)
        farms9.add_connection(farm1pos)
        farms9.add_connection(accountaccountview)




        farms8 = Context("farms8", farms8button, detect_farmswitchview)
        farms8.add_connection(farm0pos)
        farms8.add_connection(farm1pos)
        farms8.add_connection(accountaccountview)


        farms7 = Context("farms7", farms7button, detect_farmswitchview)
        farms7.add_connection(farm0pos)
        farms7.add_connection(farm1pos)
        farms7.add_connection(accountaccountview)



        farms6 = Context("farms6", farms6button, detect_farmswitchview)
        farms6.add_connection(farm0pos)
        farms6.add_connection(farm1pos)
        farms6.add_connection(accountaccountview)




        farms5 = Context("farms5", farms5button, detect_farmswitchview)
        farms5.add_connection(farm0pos)
        farms5.add_connection(farm1pos)
        farms5.add_connection(accountaccountview)




        farms4 = Context("farms4", farms4button, detect_farmswitchview)
        farms4.add_connection(farm0pos)
        farms4.add_connection(farm1pos)
        farms4.add_connection(accountaccountview)



        farms3 = Context("farms3", farms3button, detect_farmswitchview)

        farms3.add_connection(farm0pos)
        farms3.add_connection(farm1pos)
        farms3.add_connection(accountaccountview)


        farms2 = Context("farms2", farms2button, detect_farmswitchview)

        farms2.add_connection(farm0pos)
        farms2.add_connection(farm1pos)
        farms2.add_connection(accountaccountview)


        farms1 = Context("farms1", farms1button, detect_farmswitchview)

        farms1.add_connection(farm0pos)
        farms1.add_connection(farm1pos)
        farms1.add_connection(accountaccountview)

        farms0 = Context("farms0", farms0button, detect_farmswitchview)

        farms0.add_connection(farm0pos)
        farms0.add_connection(farm1pos)
        farms0.add_connection(accountaccountview)

        def detect_googleplayfailreturnbutton():
            detect_googleplayfailreturnbutton.cxlist = [0.88125]
            detect_googleplayfailreturnbutton.cylist = [0.55]
            detect_googleplayfailreturnbutton.clist = [C.Color(238, 238, 238)]
            return all(map(MN.color_comp, detect_googleplayfailreturnbutton.cxlist, detect_googleplayfailreturnbutton.cylist,
                           detect_googleplayfailreturnbutton.clist))

        def click_googleplayfailreturnbutton():
            MN.click_screen_area(0.86375, 0.5328125, 0.89875, 0.54296875)

        googleplayfailreturnbutton = B.Button(detect_googleplayfailreturnbutton, click_googleplayfailreturnbutton)

        def detect_googleplayfailview():
            detect_googleplayfailview.cxlist = [0.0875, 0.48625, 0.905, 0.94125, 0.45375, 0.08625, 0.08625, 0.94,
                                                0.9025, 0.8325, 0.3025, 0.4625, 0.4675]
            detect_googleplayfailview.cylist = [0.4609375, 0.46171875, 0.46328125, 0.56015625, 0.55546875, 0.55625,
                                                0.31484375, 0.278125, 0.04375, 0.91171875, 0.93125, 0.5171875, 0.71875]
            detect_googleplayfailview.clist = [C.Color(238, 238, 238), C.Color(238, 238, 238), C.Color(238, 238, 238),
                                               C.Color(238, 238, 238), C.Color(238, 238, 238), C.Color(238, 238, 238),
                                               C.Color(84, 74, 57), C.Color(84, 74, 54), C.Color(4, 4, 4),
                                               C.Color(84, 74, 57), C.Color(84, 74, 57), C.Color(238, 238, 238),
                                               C.Color(84, 75, 57)]
            return all(map(MN.color_comp, detect_googleplayfailview.cxlist, detect_googleplayfailview.cylist,
                           detect_googleplayfailview.clist))

        googleplayfailview = Context("googleplayfailview", None, detect_googleplayfailview)

        def detect_googleplayloginviewbutton():
            return MN.color_comp(0.32875, 0.54609375, C.Color(178, 203, 56)) and \
                   MN.color_comp(0.42625, 0.5609375, C.Color(0, 80, 84))

        def click_googleplayloginviewbutton():
            MN.click_screen_area(0.2875, 0.5375, 0.70625, 0.56640625)

        googleplayloginviewbutton = B.Button(detect_googleplayloginviewbutton, click_googleplayloginviewbutton)

        def detect_googleplayloginview():
            detect_googleplayloginview.cxlist = [0.47, 0.48, 0.19375, 0.75375, 0.93875, 0.94875, 0.95375, 0.3975]
            detect_googleplayloginview.cylist = [0.07734375, 0.096875, 0.08515625, 0.10546875, 0.09765625, 0.69609375,
                                                 0.94609375, 0.03515625]
            detect_googleplayloginview.clist = [C.Color(30, 125, 73), C.Color(0, 226, 107), C.Color(255, 255, 255),
                                                C.Color(255, 255, 255), C.Color(78, 66, 48), C.Color(81, 70, 51),
                                                C.Color(82, 68, 48), C.Color(50, 12, 9)]
            return all(map(MN.color_comp, detect_googleplayloginview.cxlist, detect_googleplayloginview.cylist,
                           detect_googleplayloginview.clist))

        googleplayloginview = Context("googleplayloginview", googleplayloginviewbutton, detect_googleplayloginview)

        googleplayloginview.add_connection(farms0)
        googleplayloginview.add_connection(farms1)
        googleplayloginview.add_connection(farms2)
        googleplayloginview.add_connection(farms3)
        googleplayloginview.add_connection(farms4)
        googleplayloginview.add_connection(farms5)
        googleplayloginview.add_connection(farms6)
        googleplayloginview.add_connection(farms7)
        googleplayloginview.add_connection(farms8)
        googleplayloginview.add_connection(farms9)
        googleplayloginview.add_connection(farms10)
        googleplayloginview.add_connection(accountaccountview)


        def detect_fbloginviewbutton():
            return MN.color_comp(0.31375, 0.4890625, C.Color(31, 65, 133)) and \
                   MN.color_comp(0.465, 0.4796875, C.Color(1, 83, 92))

        def click_fbloginviewbutton():
            MN.click_screen_area(0.29, 0.46875, 0.69625, 0.4921875)

        fbloginviewbutton = B.Button(detect_fbloginviewbutton, click_fbloginviewbutton)

        def detect_fbloginview():
            return detect_switchaccountview()

        fbloginview = Context("fbloginview", fbloginviewbutton, detect_fbloginview)

        def detect_switchaccountviewbutton():
            return MN.color_comp(0.34125, 0.67421875, C.Color(67, 100, 0)) and \
                   MN.color_comp(0.66375, 0.67578125, C.Color(72, 105, 1))

        def click_switchaccountviewbutton():
            MN.click_screen_area(0.18625, 0.6625, 0.8125, 0.6890625)

        switchaccountviewbutton = B.Button(detect_switchaccountviewbutton, click_switchaccountviewbutton)

        def detect_switchaccountview():
            return MN.color_comp(0.29375, 0.35390625, C.Color(108, 26, 21)) and \
                   MN.color_comp(0.695, 0.35625, C.Color(107, 24, 20)) and \
                   MN.color_comp(0.6475, 0.48203125, C.Color(2, 76, 91)) and \
                   MN.color_comp(0.315, 0.48671875, C.Color(40, 73, 139)) and \
                   MN.color_comp(0.46375, 0.55546875, C.Color(1, 83, 92)) and \
                   MN.color_comp(0.7175, 0.640625, C.Color(188, 170, 135))

        switchaccountview = Context("switchaccountview", switchaccountviewbutton, detect_switchaccountview)

        switchaccountview.add_connection(fbloginview)
        switchaccountview.add_connection(googleplayloginview)
        switchaccountview.add_connection(googleplayfailview)



        def detect_accountaccountviewbutton():
            return MN.color_comp(0.15125, 0.4984375, C.Color(204, 66, 67)) and \
                   MN.color_comp(0.1775, 0.48125, C.Color(236, 236, 236)) and \
                   MN.color_comp(0.2175, 0.45546875, C.Color(30, 16, 2))

        def click_accountaccountviewbutton():
            if(detect_accountaccountviewbutton()):
                MN.click_screen_area(0.1075, 0.45078125, 0.22, 0.51796875)
            else:
               MN.click_screen_area(0.10625, 0.58828125, 0.21875, 0.65390625)

        accountaccountviewbutton = B.Button(detect_accountaccountviewbutton, click_accountaccountviewbutton)



        accountaccountview = Context("accountaccountview", accountaccountviewbutton, detect_accountaccountview)

        accountaccountview.add_connection(switchaccountview)



        def detect_appresetbutton():
            detect_appresetbutton.cxlist = [1.02125]
            detect_appresetbutton.cylist = [0.959375]
            detect_appresetbutton.clist = [C.Color(0, 16, 13)]
            return all(map(MN.color_comp, detect_appresetbutton.cxlist, detect_appresetbutton.cylist,
                           detect_appresetbutton.clist))

        def click_appresetbutton():
            MN.click_screen_area(1.01625, 0.95625, 1.02875, 0.96328125)

        appresetbutton = B.Button(detect_appresetbutton, click_appresetbutton)

        def detect_phonehomescreenbutton():
            return MN.color_comp(1.02125, 0.934375, C.Color(2,16,13))

        def click_phonehomescreenbutton():
            MN.click_screen_area(1.01375, 0.9296875, 1.0275, 0.93984375)

        phonehomescreenbutton = B.Button(detect_phonehomescreenbutton, click_phonehomescreenbutton)

        def detect_phonehomescreen():
            return MN.color_comp(0.165, 0.07265625, C.Color(0, 20, 54)) and \
                   MN.color_comp(0.77625, 0.28828125, C.Color(2, 127, 167)) and \
                   MN.color_comp(0.68, 0.740625, C.Color(0, 169, 188)) and \
                   MN.color_comp(0.0925, 0.66953125, C.Color(2, 42, 63)) and \
                   MN.color_comp(0.43375, 0.475, C.Color(0, 53, 76))

        phonehomescreen = Context("phonehomescreen", phonehomescreenbutton, detect_phonehomescreen)
        phonehomescreen.add_extrabutton(appresetbutton)





        def detect_questviewbutton():
            return MN.color_comp(0.2825, 0.95390625, C.Color(235, 202, 136)) and \
                   MN.color_comp(0.33375, 0.971875, C.Color(212, 179, 97)) and \
                   MN.color_comp(0.32625, 0.9578125, C.Color(229, 220, 204)) and \
                   MN.color_comp(0.24625, 0.97265625, C.Color(138, 154, 160))

        def click_questviewbutton():
            MN.click_screen_area(0.27625, 0.9546875, 0.32, 0.9765625)

        questviewbutton = B.Button(detect_questviewbutton, click_questviewbutton)

        def detect_questview_old():
            return MN.color_comp(0.08875, 0.0171875, C.Color(147, 131, 98)) and \
                   MN.color_comp(0.4225, 0.03125, C.Color(168, 41, 28)) and \
                   MN.color_comp(0.815, 0.0375, C.Color(21, 20, 20)) and \
                   MN.color_comp(0.94875, 0.1015625, C.Color(117, 21, 12)) and \
                   MN.color_comp(0.6475, 0.1, C.Color(62, 11, 11)) and \
                   MN.color_comp(0.06625, 0.1046875, C.Color(231, 44, 61)) and \
                   MN.color_comp(0.165, 0.4234375, C.Color(170, 129, 71)) and \
                   MN.color_comp(0.1475, 0.3921875, C.Color(212, 196, 163)) and \
                   MN.color_comp(0.7275, 0.428125, C.Color(41, 41, 34)) and \
                   MN.color_comp(0.93625, 0.4234375, C.Color(236, 224, 195))

        def detect_altquestview():
            detect_altquestview.cxlist = [0.76875, 0.7675, 0.6525, 0.35875, 0.1, 0.0375, 0.115, 0.26375, 0.2775,
                                          0.27875]
            detect_altquestview.cylist = [0.3109375, 0.23515625, 0.0234375, 0.02578125, 0.2203125, 0.2734375,
                                          0.31953125, 0.4234375, 0.4703125, 0.52578125]
            detect_altquestview.clist = [C.Color(0, 72, 72), C.Color(210, 185, 143), C.Color(99, 24, 21),
                                         C.Color(106, 28, 23), C.Color(170, 143, 77), C.Color(196, 157, 105),
                                         C.Color(205, 179, 137), C.Color(39, 39, 33), C.Color(24, 24, 16),
                                         C.Color(38, 38, 32)]
            return all(
                map(MN.color_comp, detect_altquestview.cxlist, detect_altquestview.cylist, detect_altquestview.clist))

        def detect_questview():
            detect_questview.cxlist = [0.41375, 0.585, 0.05875, 0.05375, 0.06125, 0.0525, 0.055, 0.79625, 0.2875]
            detect_questview.cylist = [0.03359375, 0.03203125, 0.42421875, 0.52578125, 0.60625, 0.565625, 0.47265625,
                                       0.32421875, 0.32734375]
            detect_questview.clist = [C.Color(147, 33, 24), C.Color(161, 37, 25), C.Color(39, 39, 33),
                                      C.Color(38, 38, 32), C.Color(39, 39, 32), C.Color(18, 18, 10),
                                      C.Color(19, 19, 11), C.Color(79, 120, 2), C.Color(191, 166, 123)]
            return detect_questview_old() or detect_altquestview() or all(map(MN.color_comp, detect_questview.cxlist, detect_questview.cylist, detect_questview.clist))



        questview = Context("questview", questviewbutton, detect_questview)

        def detect_packviewbutton():
            p1 = MN.color_comp(0.47, 0.9421875, C.Color(244, 195, 121))
            p2 = MN.color_comp(0.4875, 0.95546875, C.Color(70, 44, 28))
            p3 = MN.color_comp(0.45875, 0.971875, C.Color(154, 106, 65))
            p4 = MN.color_comp(0.42375, 0.97734375, C.Color(68, 47, 25))
            return p1 and p2 and p3 and p4

        def click_packviewbutton():
            MN.click_screen_area(0.42875, 0.94609375, 0.49375, 0.9828125)

        packviewbutton = B.Button(detect_packviewbutton, click_packviewbutton)

        def detect_packview():
            return MN.color_comp(0.42625, 0.02734375, C.Color(155, 35, 22)) and \
                   MN.color_comp(0.77625, 0.034375, C.Color(0, 34, 51)) and \
                   MN.color_comp(0.05, 0.0203125, C.Color(74, 60, 39)) and \
                   MN.color_comp(0.5, 0.2015625, C.Color(33, 67, 96)) and \
                   MN.color_comp(0.9025, 0.20625, C.Color(26, 59, 80)) and \
                   MN.color_comp(0.70125, 0.2609375, C.Color(73, 54, 37)) and \
                   MN.color_comp(0.26375, 0.18984375, C.Color(196, 187, 172))


        packview = Context("packview", packviewbutton, detect_packview)

        def detect_maildeletebutton():
            detect_maildeletebutton.cxlist = [0.92625, 0.88375]
            detect_maildeletebutton.cylist = [0.015625, 0.034375]
            detect_maildeletebutton.clist = [C.Color(232, 198, 130), C.Color(23, 26, 28)]
            return all(map(MN.color_comp, detect_maildeletebutton.cxlist, detect_maildeletebutton.cylist,
                           detect_maildeletebutton.clist))

        def click_maildeletebutton():
            MN.click_screen_area(0.90375, 0.0203125, 0.9425, 0.05234375)

        maildeletebutton = B.Button(detect_maildeletebutton, click_maildeletebutton)

        def detect_getmailrewardviewbutton():
            detect_getmailrewardviewbutton.cxlist = [0.61, 0.3875]
            detect_getmailrewardviewbutton.cylist = [0.93515625, 0.9265625]
            detect_getmailrewardviewbutton.clist = [C.Color(58, 83, 3), C.Color(48, 77, 2)]
            return all(map(MN.color_comp, detect_getmailrewardviewbutton.cxlist, detect_getmailrewardviewbutton.cylist,
                           detect_getmailrewardviewbutton.clist))

        def click_getmailrewardviewbutton():
            MN.click_screen_area(0.3725, 0.9171875, 0.61875, 0.95234375)

        getmailrewardviewbutton = B.Button(detect_getmailrewardviewbutton, click_getmailrewardviewbutton)

        mailrewardview = Context('mailrewardview', getmailrewardviewbutton, detect_dailyrewardreceiptview)

        def detect_topmailviewbutton():
            detect_topmailviewbutton.cxlist = [0.15, 0.05625, 0.12, 0.92625]
            detect_topmailviewbutton.cylist = [0.15390625, 0.134375, 0.14375, 0.16875]
            detect_topmailviewbutton.clist = [C.Color(189, 176, 153), C.Color(179, 159, 133), C.Color(118, 60, 60),
                                              C.Color(201, 181, 143)]
            return all(map(MN.color_comp, detect_topmailviewbutton.cxlist, detect_topmailviewbutton.cylist,
                           detect_topmailviewbutton.clist))

        def click_topmailviewbutton():
            MN.click_screen_area(0.0425, 0.09765625, 0.9475, 0.203125)

        topmailviewbutton = B.Button(detect_topmailviewbutton, click_topmailviewbutton)

        def detect_postcollecttopmailview():
            detect_postcollecttopmailview.cxlist = [0.2625, 0.935, 0.12875, 0.83875, 0.48125, 0.075, 0.65375]
            detect_postcollecttopmailview.cylist = [0.12109375, 0.13203125, 0.95078125, 0.928125, 0.8390625, 0.38515625,
                                                    0.0296875]
            detect_postcollecttopmailview.clist = [C.Color(210, 185, 142), C.Color(211, 185, 143),
                                                   C.Color(213, 188, 145), C.Color(210, 185, 142),
                                                   C.Color(210, 184, 141), C.Color(210, 185, 142), C.Color(109, 27, 21)]
            return all(map(MN.color_comp, detect_postcollecttopmailview.cxlist, detect_postcollecttopmailview.cylist,
                           detect_postcollecttopmailview.clist))

        def detect_alttopmailview():
            detect_alttopmailview.cxlist = [0.61625, 0.7875, 0.94125, 0.90375, 0.1425, 0.86375, 0.29875]
            detect_alttopmailview.cylist = [0.940625, 0.93671875, 0.85078125, 0.59140625, 0.4125, 0.3625, 0.09140625]
            detect_alttopmailview.clist = [C.Color(50, 75, 2), C.Color(210, 186, 142), C.Color(208, 182, 134),
                                           C.Color(210, 186, 142), C.Color(210, 185, 142), C.Color(211, 186, 143),
                                           C.Color(184, 150, 100)]
            return all(map(MN.color_comp, detect_alttopmailview.cxlist, detect_alttopmailview.cylist,
                           detect_alttopmailview.clist))

        def detect_topmailview():
            detect_topmailview.cxlist = [0.3575, 0.26875, 0.94875, 0.1425, 0.595, 0.86125, 0.12625]
            detect_topmailview.cylist = [0.03046875, 0.11484375, 0.12109375, 0.3046875, 0.92890625, 0.9328125,
                                         0.5109375]
            detect_topmailview.clist = [C.Color(109, 27, 23), C.Color(211, 186, 143), C.Color(203, 177, 128),
                                        C.Color(211, 186, 143), C.Color(59, 92, 2), C.Color(209, 184, 141),
                                        C.Color(212, 187, 144)]
            return all(
                map(MN.color_comp, detect_topmailview.cxlist, detect_topmailview.cylist, detect_topmailview.clist)) or \
                   detect_alttopmailview() or detect_postcollecttopmailview()

        topmailview = Context("topmailview", topmailviewbutton, detect_topmailview)
        topmailview.add_connection(mailrewardview)

        topmailreturnview = copy.copy(topmailview)
        topmailreturnview.setbutton(dailyrewardcityviewbutton)
        mailrewardview.add_connection(topmailreturnview)

        def detect_mailselectdeleteviewbutton():
            detect_mailselectdeleteviewbutton.cxlist = [0.75, 0.7775]
            detect_mailselectdeleteviewbutton.cylist = [0.98046875, 0.95546875]
            detect_mailselectdeleteviewbutton.clist = [C.Color(25, 26, 28), C.Color(232, 198, 130)]
            return all(map(MN.color_comp, detect_mailselectdeleteviewbutton.cxlist, detect_mailselectdeleteviewbutton.cylist,
                           detect_mailselectdeleteviewbutton.clist))

        def click_mailselectdeleteviewbutton():
            MN.click_screen_area(0.75375, 0.95546875, 0.80375, 0.98828125)

        mailselectdeleteviewbutton = B.Button(detect_mailselectdeleteviewbutton, click_mailselectdeleteviewbutton)





        def detect_mailselectallviewbutton():
            detect_mailselectallviewbutton.cxlist = [0.185]
            detect_mailselectallviewbutton.cylist = [0.95]
            detect_mailselectallviewbutton.clist = [C.Color(8, 12, 18)]
            return all(map(MN.color_comp, detect_mailselectallviewbutton.cxlist, detect_mailselectallviewbutton.cylist,
                           detect_mailselectallviewbutton.clist))

        def click_mailselectallviewbutton():
            MN.click_screen_area(0.18875, 0.95390625, 0.23875, 0.98984375)

        mailselectallviewbutton = B.Button(detect_mailselectallviewbutton, click_mailselectallviewbutton)


        mailselectallview = Context("mailselectallview", mailselectallviewbutton, None)


        def detect_mailselectviewbutton():
            detect_mailselectviewbutton.cxlist = [0.895, 0.97125]
            detect_mailselectviewbutton.cylist = [0.03828125, 0.04453125]
            detect_mailselectviewbutton.clist = [C.Color(2, 76, 76), C.Color(11, 77, 77)]
            return all(map(MN.color_comp, detect_mailselectviewbutton.cxlist, detect_mailselectviewbutton.cylist,
                           detect_mailselectviewbutton.clist))

        def click_mailselectviewbutton():
            MN.click_screen_area(0.855, 0.0171875, 0.97125, 0.04609375)

        mailselectviewbutton = B.Button(detect_mailselectviewbutton, click_mailselectviewbutton)


        mailselectview = Context("mailselectview", mailselectviewbutton, None)


        def detect_regularmailview():
            detect_regularmailview.cxlist = [0.11, 0.11625, 0.11375, 0.055, 0.0525]
            detect_regularmailview.cylist = [0.1078125, 0.13671875, 0.18046875, 0.20234375, 0.096875]
            detect_regularmailview.clist = [C.Color(182, 162, 134), C.Color(119, 40, 40), C.Color(172, 154, 125),
                                             C.Color(211, 193, 154), C.Color(227, 208, 173)]
            return all(map(MN.color_comp, detect_regularmailview.cxlist, detect_regularmailview.cylist,
                           detect_regularmailview.clist))


        def detect_alliancestatusmailviewbutton():
            detect_alliancestatusmailviewbutton.cxlist = [0.15625, 0.1775, 0.13875, 0.10875, 0.07, 0.0925]
            detect_alliancestatusmailviewbutton.cylist = [0.36796875, 0.37265625, 0.3921875, 0.4171875, 0.4109375,
                                                      0.34296875]
            detect_alliancestatusmailviewbutton.clist = [C.Color(195, 88, 16), C.Color(175, 153, 121),
                                                     C.Color(236, 219, 154), C.Color(80, 52, 20),
                                                     C.Color(169, 149, 118), C.Color(179, 155, 123)]
            return all(
                map(MN.color_comp, detect_alliancestatusmailviewbutton.cxlist, detect_alliancestatusmailviewbutton.cylist,
                    detect_alliancestatusmailviewbutton.clist))

        def click_alliancestatusmailviewbutton():
            MN.click_screen_area(0.035, 0.33203125, 0.95125, 0.43828125)

        alliancestatusmailviewbutton = B.Button(detect_alliancestatusmailviewbutton, click_alliancestatusmailviewbutton)



        alliancestatusmailview = Context("alliancestatusmailview", alliancestatusmailviewbutton, detect_regularmailview)


        def detect_systemnoticemailviewbutton():
            detect_systemnoticemailviewbutton.cxlist = [0.1325, 0.18, 0.055, 0.91125]
            detect_systemnoticemailviewbutton.cylist = [0.228125, 0.2453125, 0.2375, 0.2296875]
            detect_systemnoticemailviewbutton.clist = [C.Color(190, 177, 146), C.Color(173, 151, 120),
                                                   C.Color(175, 152, 120), C.Color(204, 180, 135)]
            return all(map(MN.color_comp, detect_systemnoticemailviewbutton.cxlist, detect_systemnoticemailviewbutton.cylist,
                           detect_systemnoticemailviewbutton.clist))

        def click_systemnoticemailviewbutton():
            MN.click_screen_area(0.035, 0.196875, 0.94125, 0.2953125)

        systemnoticemailviewbutton = B.Button(detect_systemnoticemailviewbutton, click_systemnoticemailviewbutton)



        systemnoticemailview = Context("systemnoticemailview", systemnoticemailviewbutton, detect_regularmailview)

        def detect_mailviewbutton():
            return MN.color_comp(0.60375, 0.94296875, C.Color(218, 214, 201)) and \
                   MN.color_comp(0.615, 0.95859375, C.Color(106, 48, 48)) and \
                   MN.color_comp(0.645, 0.9734375, C.Color(191, 182, 158)) and \
                   MN.color_comp(0.57, 0.971875, C.Color(195, 179, 146))

        def click_mailviewbutton():
            MN.click_screen_area(0.575, 0.94609375, 0.65375, 0.97890625)

        mailviewbutton = B.Button(detect_mailviewbutton, click_mailviewbutton)

        def detect_mailview():
            return MN.color_comp(0.93625, 0.04453125, C.Color(2, 76, 84)) and \
                   MN.color_comp(0.95875, 0.02890625, C.Color(213, 196, 151)) and \
                   MN.color_comp(0.92, 0.0265625, C.Color(203, 186, 135)) and \
                   MN.color_comp(0.88375, 0.02734375, C.Color(217, 212, 167)) and \
                   MN.color_comp(0.7875, 0.0296875, C.Color(215, 181, 96)) and \
                   MN.color_comp(0.80375, 0.0171875, C.Color(3, 87, 95)) and \
                   MN.color_comp(0.65375, 0.02890625, C.Color(109, 28, 23)) and \
                   MN.color_comp(0.34125, 0.0265625, C.Color(101, 24, 24)) and \
                   MN.color_comp(0.18, 0.0328125, C.Color(43, 43, 42))

        mailview = Context("mailview", mailviewbutton, detect_mailview)

        # mailview.add_connection(lordinfomail)
        mailview.add_connection(systemnoticemailview)
        mailview.add_connection(alliancestatusmailview)
        systemnoticemailview.add_connection(topmailview)
        alliancestatusmailview.add_connection(topmailview)

        # mailview.add_connection(battlereportmail)
        # mailview.add_connection(scoutreportmail)
        # mailview.add_connection(monsterreportmail)
        # mailview.add_connection(gatherreportmail)

        mailview.add_connection(mailselectview)
        mailselectview.add_connection(mailselectallview)
        mailselectdeleteview = copy.copy(mailview)
        mailselectdeleteview.setbutton(mailselectdeleteviewbutton)
        mailselectallview.add_connection(mailselectdeleteview)

        returnmailview = copy.copy(mailview)
        returnmailview.setbutton(returnbutton)
        systemnoticemailview.add_connection(returnmailview)
        alliancestatusmailview.add_connection(returnmailview)

        returnsystemnoticemailview = copy.copy(systemnoticemailview)
        returnsystemnoticemailview.setbutton(maildeletebutton)
        topmailview.add_connection(returnsystemnoticemailview)

        returnalliancestatusmailview = copy.copy(alliancestatusmailview)
        returnalliancestatusmailview.setbutton(maildeletebutton)
        topmailview.add_connection(returnalliancestatusmailview)





        def detect_alliancebuildingviewbutton():
            detect_alliancebuildingviewbutton.cxlist = [0.17125, 0.12375, 0.555]
            detect_alliancebuildingviewbutton.cylist = [0.81171875, 0.81015625, 0.81328125]
            detect_alliancebuildingviewbutton.clist = [C.Color(84, 101, 117), C.Color(91, 110, 124),
                                                       C.Color(37, 36, 29)]
            return all(
                map(MN.color_comp, detect_alliancebuildingviewbutton.cxlist, detect_alliancebuildingviewbutton.cylist,
                    detect_alliancebuildingviewbutton.clist))

        def click_alliancebuildingviewbutton():
            MN.click_screen_area(0.13375, 0.78828125, 0.83875, 0.81796875)

        alliancebuildingviewbutton = B.Button(detect_alliancebuildingviewbutton, click_alliancebuildingviewbutton)

        def detect_finisheliteminescroll():
            detect_finisheliteminescroll.cxlist = [0.18375, 0.29125, 0.8275, 0.53375]
            detect_finisheliteminescroll.cylist = [0.940625, 0.9234375, 0.89375, 0.98828125]
            detect_finisheliteminescroll.clist = [C.Color(12, 12, 12), C.Color(12, 12, 12), C.Color(12, 12, 12),
                                                  C.Color(12, 12, 12)]
            return all(map(MN.color_comp, detect_finisheliteminescroll.cxlist, detect_finisheliteminescroll.cylist,
                           detect_finisheliteminescroll.clist))

        def click_allianceeliteminescrollview():
            MN.drag_up()

        allianceeliteminescrollviewbutton = B.Button(None, click_allianceeliteminescrollview)
        allianceeliteminescrollview = Context('allianceeliteminescrollview', allianceeliteminescrollviewbutton, detect_finisheliteminescroll)

        def find_allianceelitewoodview(debug=True, fullcoord = True):
            scanpath = 'images/results/allianceelitewoodview.png'
            im = MN.full_screen_shot()
            im.save(scanpath, 'PNG')
            if (debug):
                return IM.match_template_debug(scanpath, ['images/templates/elitewoodview.png'],
                                               'allianceelitewoodview', threshold = 0.7, fullcoord=fullcoord)
            return IM.match_template(scanpath, ['images/templates/elitewoodview.png'], threshold = 0.7, fullcoord=fullcoord)


        allianceelitewoodview = ImageContext("allianceelitewoodview", detect_mapview,
                                             find_allianceelitewoodview)
        allianceelitewoodview.add_connection(allianceeliteminescrollview)


        def find_allianceelitefoodview(debug=True, fullcoord = True):
            scanpath = 'images/results/allianceelitefarmview.png'
            im = MN.full_screen_shot()
            im.save(scanpath, 'PNG')
            if (debug):
                return IM.match_template_debug(scanpath, ['images/templates/elitefarmview.png'],
                                               'allianceelitefarmview', threshold = 0.7, fullcoord=fullcoord)
            return IM.match_template(scanpath, ['images/templates/elitefarmview.png'], threshold = 0.7, fullcoord=fullcoord)


        allianceelitefoodview = ImageContext("allianceelitefoodview", detect_mapview,
                                             find_allianceelitefoodview)
        allianceelitefoodview.add_connection(allianceeliteminescrollview)

        def find_allianceelitestoneview(debug=True, fullcoord = True):
            scanpath = 'images/results/elitestoneallianceview.png'
            im = MN.full_screen_shot()
            im.save(scanpath, 'PNG')
            if (debug):
                return IM.match_template_debug(scanpath, ['images/templates/elitestoneallianceview.png'],
                                               'elitestoneallianceview', threshold=0.7, fullcoord=fullcoord)
            return IM.match_template(scanpath, ['images/templates/elitestoneallianceview.png'], threshold=0.7, fullcoord=fullcoord)

        allianceelitestoneview = ImageContext("allianceelitestoneview", detect_mapview,
                                         find_allianceelitestoneview)
        allianceelitestoneview.add_connection(allianceeliteminescrollview)

        def find_allianceeliteironview(debug=True, fullcoord = True):
            scanpath = 'images/results/eliteironallianceview.png'
            im = MN.full_screen_shot()
            im.save(scanpath, 'PNG')
            if (debug):
                return IM.match_template_debug(scanpath, ['images/templates/eliteironallianceview.png'],
                                               'eliteironallianceview', threshold=0.7, fullcoord=fullcoord)
            return IM.match_template(scanpath, ['images/templates/eliteironallianceview.png'], threshold=0.7, fullcoord=fullcoord)


        allianceeliteironview = ImageContext("allianceeliteironview", detect_mapview,
                                             find_allianceeliteironview)
        allianceeliteironview.add_connection(allianceeliteminescrollview)

        def detect_alliancebuildinghallviewbutton():
            detect_alliancebuildinghallviewbutton.cxlist = [0.07125, 0.555, 0.82875]
            detect_alliancebuildinghallviewbutton.cylist = [0.13125, 0.12578125, 0.128125]
            detect_alliancebuildinghallviewbutton.clist = [C.Color(38, 38, 33), C.Color(38, 38, 32),
                                                           C.Color(38, 38, 32)]
            return all(map(MN.color_comp, detect_alliancebuildinghallviewbutton.cxlist,
                           detect_alliancebuildinghallviewbutton.cylist, detect_alliancebuildinghallviewbutton.clist))

        def click_alliancebuildinghallviewbutton():
            MN.click_screen_area(0.0875, 0.11953125, 0.895, 0.14296875)

        alliancebuildinghallviewbutton = B.Button(detect_alliancebuildinghallviewbutton,
                                                  click_alliancebuildinghallviewbutton)


        def detect_alliancebuildinghallview():
            detect_alliancebuildinghallview.cxlist = [0.19, 0.34875, 0.65625, 0.82875, 0.505, 0.515, 0.33625, 0.17875,
                                                      0.48625, 0.6625, 0.98125, 0.45875]
            detect_alliancebuildinghallview.cylist = [0.2671875, 0.384375, 0.26796875, 0.4140625, 0.27109375,
                                                      0.40234375, 0.634375, 0.74609375, 0.709375, 0.65078125,
                                                      0.69296875, 0.13046875]
            detect_alliancebuildinghallview.clist = [C.Color(76, 4, 0), C.Color(68, 3, 1), C.Color(67, 3, 0),
                                                     C.Color(46, 0, 0), C.Color(27, 22, 19), C.Color(26, 22, 18),
                                                     C.Color(76, 4, 0), C.Color(71, 2, 0), C.Color(22, 22, 14),
                                                     C.Color(90, 5, 3), C.Color(15, 15, 7), C.Color(42, 42, 35)]
            return all(
                map(MN.color_comp, detect_alliancebuildinghallview.cxlist, detect_alliancebuildinghallview.cylist,
                    detect_alliancebuildinghallview.clist))

        alliancebuildinghallview = Context("alliancebuildinghallview", alliancebuildinghallviewbutton,
                                           detect_alliancebuildinghallview)

        def detect_alliancebuildingeliteviewbutton():
            detect_alliancebuildingeliteviewbutton.cxlist = [0.92, 0.53375, 0.0475]
            detect_alliancebuildingeliteviewbutton.cylist = [0.3953125, 0.40390625, 0.40390625]
            detect_alliancebuildingeliteviewbutton.clist = [C.Color(208, 190, 150), C.Color(41, 41, 35),
                                                            C.Color(39, 39, 33)]
            return all(map(MN.color_comp, detect_alliancebuildingeliteviewbutton.cxlist,
                           detect_alliancebuildingeliteviewbutton.cylist, detect_alliancebuildingeliteviewbutton.clist))

        def click_alliancebuildingeliteviewbutton():
            MN.click_screen_area(0.025, 0.3859375, 0.97, 0.4171875)

        alliancebuildingeliteviewbutton = B.Button(detect_alliancebuildingeliteviewbutton,
                                                   click_alliancebuildingeliteviewbutton)

        def detect_alliancebuildingeliteview():
            detect_alliancebuildingeliteview.cxlist = [0.92625, 0.33875, 0.69, 0.695, 0.64375, 0.65875, 0.44625,
                                                       0.46125, 0.46875, 0.45125, 0.46125, 0.91125]
            detect_alliancebuildingeliteview.cylist = [0.47109375, 0.4703125, 0.5921875, 0.72734375, 0.65546875,
                                                       0.03515625, 0.31640625, 0.26640625, 0.178125, 0.084375, 0.134375,
                                                       0.11953125]
            detect_alliancebuildingeliteview.clist = [C.Color(200, 183, 143), C.Color(200, 182, 145),
                                                      C.Color(27, 27, 21), C.Color(36, 29, 23), C.Color(33, 24, 16),
                                                      C.Color(104, 28, 22), C.Color(45, 45, 38), C.Color(22, 22, 14),
                                                      C.Color(26, 22, 14), C.Color(18, 18, 10), C.Color(38, 38, 32),
                                                      C.Color(213, 205, 180)]
            return all(
                map(MN.color_comp, detect_alliancebuildingeliteview.cxlist, detect_alliancebuildingeliteview.cylist,
                    detect_alliancebuildingeliteview.clist))

        alliancebuildingeliteview = Context("alliancebuildingeliteview", alliancebuildingeliteviewbutton,
                                            detect_alliancebuildingeliteview)

        alliancebuildingeliteview.add_connection(allianceeliteironview)
        alliancebuildingeliteview.add_connection(allianceelitefoodview)
        alliancebuildingeliteview.add_connection(allianceelitewoodview)
        alliancebuildingeliteview.add_connection(allianceelitestoneview)



        def detect_alliancebuildingview():
            detect_alliancebuildingview.cxlist = [0.34875, 0.66, 0.4275, 0.36875, 0.31375, 0.35125, 0.335, 0.37125,
                                                  0.91875, 0.91125, 0.91625, 0.8625]
            detect_alliancebuildingview.cylist = [0.02890625, 0.03359375, 0.08359375, 0.12890625, 0.18046875, 0.221875,
                                                  0.2734375, 0.309375, 0.30625, 0.35390625, 0.39296875, 0.45625]
            detect_alliancebuildingview.clist = [C.Color(109, 28, 23), C.Color(101, 27, 20), C.Color(18, 18, 10),
                                                 C.Color(40, 40, 34), C.Color(22, 22, 14), C.Color(42, 42, 35),
                                                 C.Color(31, 22, 14), C.Color(39, 39, 34), C.Color(207, 197, 163),
                                                 C.Color(31, 22, 14), C.Color(197, 181, 144), C.Color(28, 23, 18)]
            return all(map(MN.color_comp, detect_alliancebuildingview.cxlist, detect_alliancebuildingview.cylist,
                           detect_alliancebuildingview.clist))

        alliancebuildingview = Context("alliancebuildingview", alliancebuildingviewbutton, detect_alliancebuildingview)
        alliancebuildingview.add_connection(alliancebuildinghallview)
        alliancebuildingview.add_connection(alliancebuildingeliteview)


        def detect_alliancetechreturnviewbutton():
            detect_alliancetechreturnviewbutton.cxlist = [0.89, 0.8725, 0.8475]
            detect_alliancetechreturnviewbutton.cylist = [0.25390625, 0.2375, 0.25625]
            detect_alliancetechreturnviewbutton.clist = [C.Color(162, 145, 101), C.Color(149, 132, 104),
                                                               C.Color(150, 134, 92)]
            return all(map(MN.color_comp, detect_alliancetechreturnviewbutton.cxlist,
                           detect_alliancetechreturnviewbutton.cylist,
                           detect_alliancetechreturnviewbutton.clist))

        def click_alliancetechreturnviewbutton():
            MN.click_screen_area(0.85, 0.24296875, 0.8825, 0.265625)

        alliancetechreturnviewbutton = B.Button(detect_alliancetechreturnviewbutton,
                                                click_alliancetechreturnviewbutton)



        def click_alliancedonateresetreturnviewbutton():
            MN.click_screen_area(0.06125, 0.02265625, 0.92375, 0.1890625)

        alliancedonateresetreturnviewbutton = B.Button(None,
                                                       click_alliancedonateresetreturnviewbutton)


        def detect_alliancedonateresetview():
            detect_alliancedonateresetview.cxlist = [0.60375, 0.3725, 0.05, 0.96625, 0.4325]
            detect_alliancedonateresetview.cylist = [0.453125, 0.45625, 0.33828125, 0.33203125, 0.446875]
            detect_alliancedonateresetview.clist = [C.Color(64, 95, 0), C.Color(47, 72, 0), C.Color(21, 13, 12),
                                                    C.Color(20, 13, 12), C.Color(252, 240, 249)]
            return all(map(MN.color_comp, detect_alliancedonateresetview.cxlist, detect_alliancedonateresetview.cylist,
                           detect_alliancedonateresetview.clist))


        def detect_alliancedonateallreturnviewbutton():
            detect_alliancedonateallreturnviewbutton.cxlist = [0.425, 0.2775]
            detect_alliancedonateallreturnviewbutton.cylist = [0.546875, 0.55]
            detect_alliancedonateallreturnviewbutton.clist = [C.Color(63, 88, 6), C.Color(76, 109, 2)]
            return all(map(MN.color_comp, detect_alliancedonateallreturnviewbutton.cxlist,
                           detect_alliancedonateallreturnviewbutton.cylist, detect_alliancedonateallreturnviewbutton.clist))

        def click_alliancedonateallreturnviewbutton():
            MN.click_screen_area(0.2025, 0.5328125, 0.43375, 0.56796875)

        alliancedonateallreturnviewbutton = B.Button(detect_alliancedonateallreturnviewbutton,
                                                  click_alliancedonateallreturnviewbutton)



        def detect_alliancedonateallview():
            detect_alliancedonateallview.cxlist = [0.27375, 0.59, 0.77125, 0.06, 0.9475, 0.94625, 0.0425]
            detect_alliancedonateallview.cylist = [0.55546875, 0.55234375, 0.553125, 0.41640625, 0.41484375, 0.575,
                                                   0.59140625]
            detect_alliancedonateallview.clist = [C.Color(77, 110, 3), C.Color(2, 75, 75), C.Color(3, 69, 85),
                                                  C.Color(15, 13, 11), C.Color(16, 10, 8), C.Color(17, 10, 9),
                                                  C.Color(14, 12, 11)]
            MN.robot_sleep(1000)
            return all(map(MN.color_comp, detect_alliancedonateallview.cxlist, detect_alliancedonateallview.cylist,
                           detect_alliancedonateallview.clist))

        alliancedonateallview = Context("alliancedonateallview", None,
                                        detect_alliancedonateallview)

        alliancedonateresetview = Context("alliancedonateresetview", None,
                                          detect_alliancedonateresetview)


        def detect_alliancedonateviewbutton():
            detect_alliancedonateviewbutton.cxlist = [0.86625, 0.45125]
            detect_alliancedonateviewbutton.cylist = [0.35703125, 0.35859375]
            detect_alliancedonateviewbutton.clist = [C.Color(24, 21, 17), C.Color(24, 21, 17)]
            return all(
                map(MN.color_comp, detect_alliancedonateviewbutton.cxlist, detect_alliancedonateviewbutton.cylist,
                    detect_alliancedonateviewbutton.clist))

        def click_alliancedonateviewbutton():
            MN.click_screen_area(0.04375, 0.30625, 0.93375, 0.4109375)

        alliancedonateviewbutton = B.Button(detect_alliancedonateviewbutton, click_alliancedonateviewbutton)

        def detect_altalliancedonateview():
            detect_altalliancedonateview.cxlist = [0.5, 0.80125, 0.47875, 0.59, 0.805, 0.41375]
            detect_altalliancedonateview.cylist = [0.653125, 0.48359375, 0.3390625, 0.26640625, 0.64921875, 0.65234375]
            detect_altalliancedonateview.clist = [C.Color(210, 185, 142), C.Color(97, 75, 48), C.Color(209, 184, 142),
                                                  C.Color(101, 13, 16), C.Color(60, 84, 1), C.Color(3, 67, 69)]
            return all(map(MN.color_comp, detect_altalliancedonateview.cxlist, detect_altalliancedonateview.cylist,
                           detect_altalliancedonateview.clist))

        def detect_alliancedonateview():
            detect_alliancedonateview.cxlist = [0.41, 0.80875, 0.83375, 0.77625, 0.585, 0.4125, 0.49625]
            detect_alliancedonateview.cylist = [0.65546875, 0.65625, 0.4984375, 0.3234375, 0.26484375, 0.26015625,
                                                0.64921875]
            detect_alliancedonateview.clist = [C.Color(0, 63, 71), C.Color(53, 78, 2), C.Color(97, 75, 48),
                                               C.Color(209, 183, 142), C.Color(108, 15, 17), C.Color(119, 17, 17),
                                               C.Color(212, 187, 143)]
            return all(map(MN.color_comp, detect_alliancedonateview.cxlist, detect_alliancedonateview.cylist,
                           detect_alliancedonateview.clist)) or detect_altalliancedonateview()

        alliancedonateview = Context("alliancedonateview", alliancedonateviewbutton, detect_alliancedonateview)

        def detect_monsterswarm_alliancetechviewbutton():
            detect_monsterswarm_alliancetechviewbutton.cxlist = [0.12, 0.17625]
            detect_monsterswarm_alliancetechviewbutton.cylist = [0.728125, 0.7265625]
            detect_monsterswarm_alliancetechviewbutton.clist = [C.Color(14, 113, 187), C.Color(182, 96, 28)]
            return all(map(MN.color_comp, detect_monsterswarm_alliancetechviewbutton.cxlist, detect_monsterswarm_alliancetechviewbutton.cylist,
                           detect_monsterswarm_alliancetechviewbutton.clist))


        def click_monsterswarm_alliancetechviewbutton():
            MN.click_screen_area(0.035, 0.7140625, 0.95125, 0.7484375)

        monsterswarmalliancetechviewbutton = B.Button(detect_monsterswarm_alliancetechviewbutton, click_monsterswarm_alliancetechviewbutton)

        def detect_alliancetechviewbutton():
            detect_alliancetechviewbutton.cxlist = [0.17625, 0.11875]
            detect_alliancetechviewbutton.cylist = [0.65390625, 0.6546875]
            detect_alliancetechviewbutton.clist = [C.Color(183, 98, 30), C.Color(14, 113, 187)]
            return all(map(MN.color_comp, detect_alliancetechviewbutton.cxlist, detect_alliancetechviewbutton.cylist,
                           detect_alliancetechviewbutton.clist))

        def click_alliancetechviewbutton():
            if monsterswarmalliancetechviewbutton.detect():
                monsterswarmalliancetechviewbutton.click()
            else:
                MN.click_screen_area(0.04125, 0.640625, 0.94125, 0.68203125)

        alliancetechviewbutton = B.Button(detect_alliancetechviewbutton, click_alliancetechviewbutton)

        def detect_alliancetechview():
            detect_alliancetechview.cxlist = [0.8275, 0.1775, 0.4825, 0.6775, 0.3375, 0.21, 0.09375]
            detect_alliancetechview.cylist = [0.10625, 0.1078125, 0.1078125, 0.03203125, 0.0265625, 0.0328125,
                                              0.01484375]
            detect_alliancetechview.clist = [C.Color(64, 15, 10), C.Color(63, 15, 9), C.Color(75, 20, 12),
                                             C.Color(87, 22, 20), C.Color(104, 26, 24), C.Color(20, 20, 20),
                                             C.Color(150, 134, 101)]
            return all(map(MN.color_comp, detect_alliancetechview.cxlist, detect_alliancetechview.cylist,
                           detect_alliancetechview.clist))

        alliancetechview = Context("alliancetechview", alliancetechviewbutton, detect_alliancetechview)
        alliancetechview.add_connection(alliancedonateview)

        def detect_allianceview():
            detect_allianceview.cxlist = [0.71375, 0.52125, 0.51375, 0.47125, 0.17625, 0.155, 0.37625, 0.71375, 0.06125]
            detect_allianceview.cylist = [0.29375, 0.43984375, 0.4015625, 0.47421875, 0.4390625, 0.60078125, 0.034375,
                                          0.10390625, 0.09296875]
            detect_allianceview.clist = [C.Color(37, 28, 25), C.Color(42, 42, 36), C.Color(22, 17, 16),
                                         C.Color(20, 19, 13), C.Color(240, 36, 2), C.Color(105, 2, 4),
                                         C.Color(124, 30, 24), C.Color(178, 154, 116), C.Color(160, 25, 23)]
            return all(
                map(MN.color_comp, detect_allianceview.cxlist, detect_allianceview.cylist, detect_allianceview.clist))


        def detect_rallyjoinviewbutton():
            detect_rallyjoinviewbutton.cxlist = [0.37875]
            detect_rallyjoinviewbutton.cylist = [0.3171875]
            detect_rallyjoinviewbutton.clist = [C.Color(230, 164, 81)]
            return all(map(MN.color_comp, detect_rallyjoinviewbutton.cxlist, detect_rallyjoinviewbutton.cylist,
                           detect_rallyjoinviewbutton.clist))

        def click_rallyjoinviewbutton():
            MN.click_screen_area(0.35875, 0.3015625, 0.3975, 0.33125)

        rallyjoinviewbutton = B.Button(detect_rallyjoinviewbutton, click_rallyjoinviewbutton)


        def detect_alliancebattleviewbutton():
            return MN.color_comp(0.1475, 0.4515625, C.Color(255, 244, 57)) and \
                   MN.color_comp(0.1775, 0.43671875, C.Color(243, 23, 6)) and \
                   MN.color_comp(0.815, 0.43984375, C.Color(21, 21, 21)) and \
                   MN.color_comp(0.9025, 0.4359375, C.Color(203, 186, 145))

        def click_alliancebattleviewbutton():
            MN.click_screen_area(0.0525, 0.4234375, 0.9475, 0.4546875)

        alliancebattleviewbutton = B.Button(detect_alliancebattleviewbutton, click_alliancebattleviewbutton)

        def detect_alliancebattleview():
            return MN.color_comp(0.62125, 0.95234375, C.Color(136, 124, 99)) and \
                   MN.color_comp(0.2425, 0.95234375, C.Color(10, 10, 10)) and \
                   MN.color_comp(0.65125, 0.03359375, C.Color(111, 28, 24))

        alliancebattleview = Context("alliancebattleview", alliancebattleviewbutton, detect_alliancebattleview)


        rallyjoinview = Context('rallyjoinview', rallyjoinviewbutton, detect_marchsetupview)
        alliancebattleview.add_connection(rallyjoinview)

        rallyjoinsetoutview = copy.copy(alliancebattleview)
        rallyjoinsetoutview.setbutton(marchsetoutbutton)
        rallyjoinview.add_connection(rallyjoinsetoutview)


        #alliancebattleview.add_connection(battlelogview)

        def detect_allianceviewbutton():
            return MN.color_comp(0.7475, 0.959375, C.Color(122, 146, 171)) and \
                   MN.color_comp(0.79625, 0.95703125, C.Color(70, 36, 32)) and \
                   MN.color_comp(0.80375, 0.9796875, C.Color(229, 212, 144))

        def click_allianceviewbutton():
            MN.click_screen_area(0.7375, 0.94765625, 0.8075, 0.9765625)

        allianceviewbutton = B.Button(detect_allianceviewbutton, click_allianceviewbutton)

        allianceview = Context("allianceview", allianceviewbutton, detect_allianceview)



        allianceview.add_connection(alliancebattleview)
        # allianceview.add_connection(elitewarview)
        # allianceview.add_connection(eliteadventureview)
        allianceview.add_connection(alliancetechview)
        # allianceview.add_connection(alliancehelpview)
        allianceview.add_connection(alliancebuildingview)
        # allianceview.add_connection(alliancetempleview)
        # allianceview.add_connection(alliancememberview)
        # allianceview.add_connection(manageallianceview)
        # allianceview.add_connection(allianceshopview)
        # allianceview.add_connection(alliancegroupchatview)


        def detect_lordinfoviewbutton():
            return MN.color_comp(0.9, 0.97578125, C.Color(200, 63, 64)) and \
                   MN.color_comp(0.93, 0.96171875, C.Color(224, 224, 224)) and \
                   MN.color_comp(0.965, 0.97109375, C.Color(243, 62, 62))

        def click_lordinfoviewbutton():
            MN.click_screen_area(0.90125, 0.9515625, 0.95625, 0.9734375)

        lordinfoviewbutton = B.Button(detect_lordinfoviewbutton, click_lordinfoviewbutton)

        def detect_lordinfoview():
            return MN.color_comp(0.21625, 0.034375, C.Color(4, 3, 4)) and \
                   MN.color_comp(0.37875, 0.0265625, C.Color(125, 31, 24)) and \
                   MN.color_comp(0.47, 0.94453125, C.Color(130, 67, 13)) and \
                   MN.color_comp(0.78375, 0.946875, C.Color(130, 67, 12)) and \
                   MN.color_comp(0.7325, 0.82109375, C.Color(199, 172, 111)) and \
                   MN.color_comp(0.02, 0.62109375, C.Color(174, 109, 89)) and \
                   MN.color_comp(0.89875, 0.58359375, C.Color(26, 26, 35))

        lordinfoview = Context("lordinfoview", lordinfoviewbutton, detect_lordinfoview)


        # lordinfoview.add_connection(lordinfodetails)
        # lordinfoview.add_connection(lordinforanking)
        # lordinfoview.add_connection(lordinfoachivements)
        # lordinfoview.add_connection(lordinfolordskills)
        # lordinfoview.add_connection(lordinfoequip)
        # lordinfoview.add_connection(lordinfoemblem)

        def detect_workshopview():
            detect_workshopview.cxlist = [0.635, 0.3575, 0.97125, 0.91625, 0.13375, 0.73875, 0.11875, 0.78875, 0.20875]
            detect_workshopview.cylist = [0.03515625, 0.0296875, 0.04296875, 0.0203125, 0.590625, 0.15703125, 0.203125,
                                          0.6046875, 0.95546875]
            detect_workshopview.clist = [C.Color(115, 30, 24), C.Color(107, 26, 22), C.Color(3, 61, 68),
                                         C.Color(149, 150, 137), C.Color(22, 24, 25), C.Color(26, 92, 142),
                                         C.Color(17, 47, 73), C.Color(24, 40, 43), C.Color(24, 24, 17)]
            return all(
                map(MN.color_comp, detect_workshopview.cxlist, detect_workshopview.cylist, detect_workshopview.clist))

        workshopview = Context("workshopview", None, detect_workshopview)





        def detect_accountviewbutton():
            return MN.color_comp(0.0275, 0.1046875, C.Color(28, 19, 3))

        def click_accountviewbutton():
            MN.click_screen_area(0.0425, 0.03671875, 0.1225, 0.08125)

        accountviewbutton = B.Button(detect_accountviewbutton, click_accountviewbutton)

        def detect_accountview():
            detect_accountview.cxlist = [0.38875, 0.6325, 0.71375, 0.715, 0.49625, 0.49125, 0.48875, 0.86375, 0.07875,
                                         0.39]
            detect_accountview.cylist = [0.02734375, 0.03359375, 0.62890625, 0.759375, 0.74609375, 0.61015625,
                                         0.6671875, 0.2546875, 0.103125, 0.03359375]
            detect_accountview.clist = [C.Color(138, 34, 25), C.Color(117, 30, 24), C.Color(210, 185, 142),
                                        C.Color(210, 185, 143), C.Color(211, 186, 143), C.Color(208, 183, 140),
                                        C.Color(209, 184, 142), C.Color(204, 179, 134), C.Color(201, 176, 134),
                                        C.Color(140, 33, 25)]
            return all(
                map(MN.color_comp, detect_accountview.cxlist, detect_accountview.cylist, detect_accountview.clist))

        accountview = Context("accountview", accountviewbutton, detect_accountview)

        accountview.add_connection(accountaccountview)




        def detect_vipviewbutton():
            return MN.color_comp(0.615, 0.05625, C.Color(217, 39, 42)) and \
                   MN.color_comp(0.51, 0.06171875, C.Color(191, 26, 26)) and \
                   MN.color_comp(0.57125, 0.05625, C.Color(242, 209, 115))

        def click_vipviewbutton():
            MN.click_screen_area(0.51625, 0.0515625, 0.61875, 0.06484375)

        vipviewbutton = B.Button(detect_vipviewbutton, click_vipviewbutton)

        def detect_vipview():
            return MN.color_comp(0.215, 0.0328125, C.Color(15, 15, 15)) and \
                   MN.color_comp(0.3875, 0.02890625, C.Color(138, 34, 24)) and \
                   MN.color_comp(0.38125, 0.31328125, C.Color(3, 61, 61)) and \
                   MN.color_comp(0.21375, 0.3296875, C.Color(210, 183, 141)) and \
                   MN.color_comp(0.6, 0.36953125, C.Color(49, 41, 32))

        vipview = Context("vipview", vipviewbutton, detect_vipview)



        def detect_purchaseviewbutton():
            return MN.color_comp(0.80375, 0.0703125, C.Color(0, 33, 47)) and \
                   MN.color_comp(0.9475, 0.0625, C.Color(242, 209, 245))

        def click_purchaseviewbutton():
            MN.click_screen_area(0.80625, 0.06171875, 0.955, 0.078125)

        purchaseviewbutton = B.Button(detect_purchaseviewbutton, click_purchaseviewbutton)

        def detect_purchaseview():
            return MN.color_comp(0.885, 0.03671875, C.Color(0, 34, 51)) and \
                   MN.color_comp(0.9375, 0.0265625, C.Color(254, 200, 241)) and \
                   MN.color_comp(0.94125, 0.109375, C.Color(133, 67, 9)) and \
                   MN.color_comp(0.61125, 0.0296875, C.Color(137, 33, 24)) and \
                   MN.color_comp(0.4, 0.0296875, C.Color(138, 33, 24))

        purchaseview = Context("purchaseview", purchaseviewbutton, detect_purchaseview)



        def click_harvestreturnviewbutton():
            MN.click_screen_area(0.17625, 0.77421875, 0.81625, 0.8671875)

        harvestreturnviewbutton = B.Button(None, click_harvestreturnviewbutton)



        # 2nd view (after pressing harvest button)
        def detect_harvestskillharvestviewbutton():
            detect_harvestskillharvestviewbutton.cxlist = [0.41875, 0.5725]
            detect_harvestskillharvestviewbutton.cylist = [0.953125, 0.95703125]
            detect_harvestskillharvestviewbutton.clist = [C.Color(68, 101, 2), C.Color(84, 109, 2)]
            return all(map(MN.color_comp, detect_harvestskillharvestviewbutton.cxlist,
                           detect_harvestskillharvestviewbutton.cylist, detect_harvestskillharvestviewbutton.clist))

        def click_harvestskillharvestviewbutton():
            MN.click_screen_area(0.3425, 0.94453125, 0.65125, 0.9734375)


        harvestskillharvestviewbutton = B.Button(detect_harvestskillharvestviewbutton,
                                                 click_harvestskillharvestviewbutton)

        def detect_harvestskillharvestview():
            detect_harvestskillharvestview.cxlist = [0.6625, 0.33125, 0.22375, 0.75625]
            detect_harvestskillharvestview.cylist = [0.28515625, 0.2828125, 0.31171875, 0.40703125]
            detect_harvestskillharvestview.clist = [C.Color(81, 0, 0), C.Color(94, 4, 4), C.Color(211, 186, 143),
                                                    C.Color(166, 134, 84)]
            return all(map(MN.color_comp, detect_harvestskillharvestview.cxlist, detect_harvestskillharvestview.cylist,
                           detect_harvestskillharvestview.clist))

        harvestskillharvestview = Context("harvestskillharvestview", harvestskillharvestviewbutton,
                                          detect_harvestskillharvestview)


        # 1st view (before pressing harvest button)
        def detect_harvestskillaccessviewbutton():
            detect_harvestskillaccessviewbutton.cxlist = [0.18125, 0.15375]
            detect_harvestskillaccessviewbutton.cylist = [0.62734375, 0.62421875]
            detect_harvestskillaccessviewbutton.clist = [C.Color(30, 204, 17), C.Color(31, 16, 4)]
            return all(map(MN.color_comp, detect_harvestskillaccessviewbutton.cxlist,
                           detect_harvestskillaccessviewbutton.cylist, detect_harvestskillaccessviewbutton.clist))

        def click_harvestskillaccessviewbutton():
            MN.click_screen_area(0.135, 0.63203125, 0.22375, 0.67109375)

        harvestskillaccessviewbutton = B.Button(detect_harvestskillaccessviewbutton,
                                                click_harvestskillaccessviewbutton)

        def detect_harvestskillaccessview():
            detect_harvestskillaccessview.cxlist = [0.59, 0.38875, 0.1725, 0.1725, 0.59, 0.41625]
            detect_harvestskillaccessview.cylist = [0.9578125, 0.95625, 0.8046875, 0.8578125, 0.77578125, 0.775]
            detect_harvestskillaccessview.clist = [C.Color(72, 104, 0), C.Color(62, 95, 0), C.Color(34, 204, 17),
                                                   C.Color(47, 12, 2), C.Color(99, 48, 21), C.Color(109, 52, 22)]
            return all(map(MN.color_comp, detect_harvestskillaccessview.cxlist, detect_harvestskillaccessview.cylist,
                           detect_harvestskillaccessview.clist))

        harvestskillaccessview = Context("harvestskillaccessview", harvestskillaccessviewbutton,
                                         detect_harvestskillaccessview)
        harvestskillaccessview.add_connection(harvestskillharvestview)

        def detect_harvestskillcooldownviewbutton():
            detect_harvestskillcooldownviewbutton.cxlist = [0.1825, 0.155]
            detect_harvestskillcooldownviewbutton.cylist = [0.628125, 0.62578125]
            detect_harvestskillcooldownviewbutton.clist = [C.Color(34, 206, 17), C.Color(34, 17, 4)]
            return all(map(MN.color_comp, detect_harvestskillcooldownviewbutton.cxlist,
                           detect_harvestskillcooldownviewbutton.cylist, detect_harvestskillcooldownviewbutton.clist))

        def click_harvestskillcooldownviewbutton():
            MN.click_screen_area(0.13625, 0.63046875, 0.235, 0.6703125)
            harvestskillview.click_and_wait()

        harvestskillcooldownviewbutton = B.Button(detect_harvestskillcooldownviewbutton,
                                                  click_harvestskillcooldownviewbutton)


        #NEED A CONDITIONAL DATA STRUCT
        def detect_harvestskillcooldownview():
            detect_harvestskillcooldownview.cxlist = [0.415, 0.59125, 0.17125, 0.18625, 0.42125, 0.56625]
            detect_harvestskillcooldownview.cylist = [0.9515625, 0.95234375, 0.8015625, 0.8546875, 0.77109375,
                                                      0.77421875]
            detect_harvestskillcooldownview.clist = [C.Color(80, 80, 80), C.Color(84, 84, 84), C.Color(17, 204, 17),
                                                     C.Color(21, 8, 4), C.Color(103, 49, 22), C.Color(112, 52, 21)]
            return all(
                map(MN.color_comp, detect_harvestskillcooldownview.cxlist, detect_harvestskillcooldownview.cylist,
                    detect_harvestskillcooldownview.clist))

        harvestskillcooldownview = Context("harvestskillcooldownview", harvestskillcooldownviewbutton,
                                           detect_harvestskillcooldownview)

        def detect_harvestskillviewbutton():
            return detect_harvestskillaccessviewbutton()

        def click_harvestskillviewbutton():
            click_harvestskillaccessviewbutton()
            harvestskillview = Context.waitformultiload([harvestskillaccessview, harvestskillcooldownview])
            if (harvestskillview.name == 'harvestskillaccessview'):
                print('collecting harvest')
                harvestskillharvestview.click_and_wait()
                click_dailyrewardreceiptviewbutton()
            elif (harvestskillview.name == 'harvestskillcooldownview'):
                print('harvest already collected')
                harvestskillcooldownview.waitforload()
                click_harvestskillharvestviewbutton()

        harvestskillviewbutton = B.Button(detect_harvestskillviewbutton, click_harvestskillviewbutton)

        def detect_tipsladyviewbutton():
            detect_tipsladyviewbutton.cxlist = [0.105, 0.07125]
            detect_tipsladyviewbutton.cylist = [0.65625, 0.646875]
            detect_tipsladyviewbutton.clist = [C.Color(28, 12, 8), C.Color(255, 238, 229)]
            return all(map(MN.color_comp, detect_tipsladyviewbutton.cxlist, detect_tipsladyviewbutton.cylist,
                           detect_tipsladyviewbutton.clist))

        def click_tipsladyviewbutton():
            MN.click_screen_area(0.03125, 0.65, 0.1, 0.68203125)

        tipsladyviewbutton = B.Button(detect_tipsladyviewbutton, click_tipsladyviewbutton)

        def detect_tipsladyview():
            detect_tipsladyview.cxlist = [0.165, 0.215, 0.15875, 0.10375, 0.17375, 0.1775, 0.35, 0.87125]
            detect_tipsladyview.cylist = [0.1171875, 0.140625, 0.18671875, 0.13984375, 0.103125, 0.13515625, 0.1671875,
                                          0.17109375]
            detect_tipsladyview.clist = [C.Color(255, 251, 238), C.Color(25, 9, 3), C.Color(255, 253, 238),
                                         C.Color(22, 8, 4), C.Color(255, 243, 212), C.Color(255, 238, 221),
                                         C.Color(180, 139, 92), C.Color(179, 138, 84)]
            return all(
                map(MN.color_comp, detect_tipsladyview.cxlist, detect_tipsladyview.cylist, detect_tipsladyview.clist))

        tipsladyview = Context("tipsladyview", tipsladyviewbutton, detect_tipsladyview)

        def detect_removablebuildingdetailview():
            detect_removablebuildingdetailview.cxlist = [0.0925, 0.365, 0.62375, 0.10375, 0.12375, 0.51875, 0.2925,
                                                         0.705, 0.8675]
            detect_removablebuildingdetailview.cylist = [0.0140625, 0.0296875, 0.03203125, 0.62734375, 0.82890625,
                                                         0.92890625, 0.93203125, 0.9359375, 0.9421875]
            detect_removablebuildingdetailview.clist = [C.Color(147, 133, 100), C.Color(113, 30, 24),
                                                        C.Color(134, 32, 24), C.Color(18, 17, 12), C.Color(17, 16, 14),
                                                        C.Color(24, 23, 21), C.Color(7, 67, 75), C.Color(87, 15, 1),
                                                        C.Color(112, 14, 0)]
            return all(
                map(MN.color_comp, detect_removablebuildingdetailview.cxlist, detect_removablebuildingdetailview.cylist,
                    detect_removablebuildingdetailview.clist))

        removablebuildingdetailview = Context("removablebuildingdetailview", None, detect_removablebuildingdetailview)

        def detect_unremovablebuildingdetailview():
            detect_unremovablebuildingdetailview.cxlist = [0.82875, 0.6425, 0.87375, 0.22875, 0.41, 0.59, 0.14125, 0.89125]
            detect_unremovablebuildingdetailview.cylist = [0.03671875, 0.03125, 0.659375, 0.63515625, 0.9328125, 0.9375,
                                                     0.93359375, 0.9265625]
            detect_unremovablebuildingdetailview.clist = [C.Color(33, 32, 28), C.Color(111, 28, 22), C.Color(15, 14, 10),
                                                    C.Color(14, 12, 10), C.Color(2, 68, 68), C.Color(1, 62, 70),
                                                    C.Color(26, 25, 23), C.Color(22, 21, 17)]
            return all(map(MN.color_comp, detect_unremovablebuildingdetailview.cxlist, detect_unremovablebuildingdetailview.cylist,
                           detect_unremovablebuildingdetailview.clist))

        unremovablebuildingdetailview = Context("unremovablebuildingdetailview", None, detect_unremovablebuildingdetailview)

        def click_skillactivatecityviewbutton():
            MN.click_screen_area(0.3175, 0.22265625, 0.72875, 0.615625)

        skillactivatecityviewbutton = B.Button(None, click_skillactivatecityviewbutton)


        def detect_skillactivateviewbutton():
            return MN.color_comp(0.92875, 0.671875, C.Color(255, 255, 255)) and \
                   MN.color_comp(0.96875, 0.671875, C.Color(227, 18, 0)) and \
                   MN.color_comp(0.93, 0.6578125, C.Color(77, 66, 66))

        def click_skillactivateviewbutton():
            MN.click_screen_area(0.895, 0.66484375, 0.955, 0.6890625)

        skillactivateviewbutton = B.Button(detect_skillactivateviewbutton, click_skillactivateviewbutton)

        def detect_skillactivateview():
            return MN.color_comp(0.18125, 0.26484375, C.Color(16, 16, 16)) and \
                   MN.color_comp(0.135, 0.29453125, C.Color(178, 178, 178)) and \
                   MN.color_comp(0.175, 0.32578125, C.Color(131, 131, 131)) and \
                   MN.color_comp(0.9, 0.49453125, C.Color(15, 15, 15)) and \
                   MN.color_comp(0.87375, 0.55234375, C.Color(85, 85, 85))

        skillactivateview = Context("skillactivateview", skillactivateviewbutton, detect_skillactivateview)


        def detect_newachievementview():
            detect_newachievementview.cxlist = [0.82625, 0.735, 0.245, 0.18, 0.6325, 0.3575, 0.40125, 0.6325, 0.36875]
            detect_newachievementview.cylist = [0.5453125, 0.4921875, 0.4984375, 0.54140625, 0.63125, 0.63203125,
                                                0.640625, 0.38515625, 0.38515625]
            detect_newachievementview.clist = [C.Color(224, 170, 46), C.Color(190, 110, 8), C.Color(190, 110, 8),
                                               C.Color(217, 160, 44), C.Color(56, 81, 1), C.Color(49, 74, 1),
                                               C.Color(33, 69, 134), C.Color(24, 17, 8), C.Color(57, 50, 40)]
            return all(map(MN.color_comp, detect_newachievementview.cxlist, detect_newachievementview.cylist,
                           detect_newachievementview.clist))

        newachievementview = Context("newachievementview", None, detect_newachievementview)





        def detect_cityviewbutton():
            return MN.color_comp(0.15125, 0.92109375, C.Color(85, 88, 90)) and \
                   MN.color_comp(0.11, 0.93046875, C.Color(143, 143, 122)) and \
                   MN.color_comp(0.12, 0.9578125, C.Color(161, 93, 40)) and \
                   MN.color_comp(0.07625, 0.9296875, C.Color(136, 101, 74)) and \
                   MN.color_comp(0.0575, 0.928125, C.Color(56, 61, 64)) and \
                   MN.color_comp(0.06875, 0.94296875, C.Color(225, 218, 186)) and \
                   MN.color_comp(0.09375, 0.978125, C.Color(105, 105, 80))

        def click_cityviewbutton():
            MN.click_screen_area(0.05875, 0.92265625, 0.155, 0.9625)

        cityviewbutton = B.Button(detect_cityviewbutton, click_cityviewbutton)





        cityview = Context("cityview", cityviewbutton, detect_cityview)


        cityview.add_connection(questview)
        cityview.add_connection(packview)
        cityview.add_connection(mailview)
        cityview.add_connection(allianceview)
        cityview.add_connection(lordinfoview)
        cityview.add_connection(accountview)
        cityview.add_connection(vipview)
        cityview.add_connection(purchaseview)
        cityview.add_connection(skillactivateview)
        cityview.add_connection(workshopview)
        cityview.add_connection(newachievementview)

        def go_lowerright():
            MN.drag_southeast()

        # DEBUG
        def detect_lowerright(debug=False):
            scanpath = 'images/results/lowerright.png'
            im = MN.full_screen_shot()
            im.save(scanpath, 'PNG')
            if (debug):
                return len(IM.match_template_debug(scanpath, ['images/templates/lowerright.png'], 'lowerright', threshold = 0.65))>0
            return len(IM.match_template(scanpath, ['images/templates/lowerright.png'], threshold = 0.65))>0

        lowerrightbutton = B.Button(None, go_lowerright)

        lowerright = Context("lowerright", lowerrightbutton, detect_lowerright)

        cityview.add_connection(lowerright)

        def detect_lowermiddle(debug=False):
            scanpath = 'images/results/lowermiddle.png'
            im = MN.full_screen_shot()
            im.save(scanpath, 'PNG')
            if (debug):
                return len(IM.match_template_debug(scanpath, ['images/templates/lowermiddle.png', 'images/templates/castlepiece.png'], 'lowermiddle', threshold = 0.5))>0
            return len(IM.match_template(scanpath, ['images/templates/lowermiddle.png', 'images/templates/castlepiece.png'], threshold = 0.5))> 0

        def go_lowermiddle():
            MN.drag_west_south_west()

        lowermiddlebutton = B.Button(None, go_lowermiddle)

        lowermiddle = Context("lowermiddle", lowermiddlebutton, detect_lowermiddle)
        lowerright.add_connection(lowermiddle)


        def find_stonequarryview(debug=False):
            scanpath = 'images/results/stonequarryview.png'
            im = MN.full_screen_shot()

            im.save(scanpath, 'PNG')
            if(debug):
                return IM.match_template_debug(scanpath,
                                        ['images/templates/stonequarry1.png', 'images/templates/stonequarry2.png'],
                                        'stonequarry_find',
                                        threshold = 0.7)
            return IM.match_template(scanpath,
                                     ['images/templates/stonequarry1.png', 'images/templates/stonequarry2.png'],
                                     threshold = 0.7)


        stonequarryview = ImageContext("stonequarryview", None, find_stonequarryview)

        def find_ironmineview(debug=False):
            scanpath = 'images/results/ironmineview.png'
            im = MN.full_screen_shot()

            im.save(scanpath, 'PNG')
            if(debug):
                return IM.match_template_debug(scanpath,
                                        ['images/templates/ironmine2.png', 'images/templates/ironmine1.png',
                                         'images/templates/ironmineedge1.png', 'images/templates/ironmineedge2.png'],
                                        'ironmine_find',
                                        threshold = 0.7)
            return IM.match_template(scanpath,
                                     ['images/templates/ironmine2.png', 'images/templates/ironmine1.png',
                                      'images/templates/ironmineedge1.png', 'images/templates/ironmineedge2.png'],
                                     threshold = 0.7)


        ironmineview = ImageContext("ironmineview", None, find_ironmineview)

        def find_foodfarmview(debug=False):
            scanpath = 'images/results/foodfarmview.png'
            im = MN.full_screen_shot()

            im.save(scanpath, 'PNG')
            if(debug):
                return IM.match_template_debug(scanpath,
                                        ['images/templates/foodfarm1.png', 'images/templates/foodfarm2.png'],
                                        'foodfarm_find',
                                        threshold = 0.7)
            return IM.match_template(scanpath,
                                     ['images/templates/foodfarm1.png', 'images/templates/foodfarm2.png'],
                                     threshold = 0.7)


        foodfarmview = ImageContext("foodfarmview", None, find_foodfarmview)

        def find_woodyardview(debug=False):
            scanpath = 'images/results/woodyardview.png'
            im = MN.full_screen_shot()

            im.save(scanpath, 'PNG')
            if(debug):
                return IM.match_template_debug(scanpath,
                                        ['images/templates/woodyard1.png', 'images/templates/woodyard2.png'],
                                        'woodyard_find',
                                        threshold = 0.7)
            return IM.match_template(scanpath,
                                     ['images/templates/woodyard1.png', 'images/templates/woodyard2.png'],
                                     threshold = 0.7)



        woodyardview = ImageContext("woodyardview", None, find_woodyardview)



        def find_woodtileview():
            scanpath = 'images/woodtileview.png'
            im = MN.full_screen_shot()
            im.save(scanpath, 'PNG')
            return IM.match_template_debug(scanpath,
                                     ['images/templates/woodtile_brown.png', 'images/templates/woodtile_green.png',
                                      'images/templates/woodtile_yellow.png'], 'woodtileview')




        woodtileview = ImageContext("woodtileview", None, find_woodtileview)

        def detect_goldenhammerreturnview():
            detect_goldenhammerreturnview.cxlist = [0.375]
            detect_goldenhammerreturnview.cylist = [0.06640625]
            detect_goldenhammerreturnview.clist = [C.Color(62, 8, 6)]
            return all(map(MN.color_comp, detect_goldenhammerreturnview.cxlist, detect_goldenhammerreturnview.cylist,
                           detect_goldenhammerreturnview.clist))

        def click_goldenhammerreturnview():
            MN.click_screen_area(0.0225, 0.01484375, 0.96875, 0.18125)

        goldenhammerreturnviewbutton = B.Button(detect_goldenhammerreturnview, click_goldenhammerreturnview)

        def detect_goldenhammerviewbutton():
            detect_goldenhammerviewbutton.cxlist = [0.09375, 0.085]
            detect_goldenhammerviewbutton.cylist = [0.2859375, 0.2609375]
            detect_goldenhammerviewbutton.clist = [C.Color(36, 15, 8), C.Color(142, 115, 7)]
            return all(map(MN.color_comp, detect_goldenhammerviewbutton.cxlist, detect_goldenhammerviewbutton.cylist,
                           detect_goldenhammerviewbutton.clist))

        def click_goldenhammerviewbutton():
            MN.click_screen_area(0.035, 0.25390625, 0.09375, 0.290625)

        goldenhammerviewbutton = B.Button(detect_goldenhammerviewbutton, click_goldenhammerviewbutton)

        def detect_goldenhammerview():
            detect_goldenhammerview.cxlist = [0.63875, 0.34125, 0.38125, 0.19875, 0.1925, 0.18625, 0.6425, 0.57375,
                                              0.42125, 0.38375, 0.33375]
            detect_goldenhammerview.cylist = [0.4515625, 0.459375, 0.4375, 0.27421875, 0.32578125, 0.3328125,
                                              0.81484375, 0.81796875, 0.78828125, 0.8296875, 0.80390625]
            detect_goldenhammerview.clist = [C.Color(56, 81, 0), C.Color(51, 76, 4), C.Color(254, 204, 237),
                                             C.Color(255, 249, 225), C.Color(133, 101, 30), C.Color(3, 101, 51),
                                             C.Color(2, 68, 76), C.Color(0, 80, 89), C.Color(185, 151, 86),
                                             C.Color(139, 18, 20), C.Color(0, 48, 48)]
            return all(map(MN.color_comp, detect_goldenhammerview.cxlist, detect_goldenhammerview.cylist,
                           detect_goldenhammerview.clist))

        goldenhammerview = Context("goldenhammerview", goldenhammerviewbutton, detect_goldenhammerview)

        def detect_guardcrownviewbutton():
            detect_guardcrownviewbutton.cxlist = [0.865, 0.8675, 0.9675, 0.97]
            detect_guardcrownviewbutton.cylist = [0.34921875, 0.3125, 0.31015625, 0.33203125]
            detect_guardcrownviewbutton.clist = [C.Color(217, 217, 217), C.Color(66, 66, 65), C.Color(23, 23, 23),
                                                 C.Color(233, 232, 232)]
            return all(map(MN.color_comp, detect_guardcrownviewbutton.cxlist, detect_guardcrownviewbutton.cylist,
                           detect_guardcrownviewbutton.clist))

        def click_guardcrownviewbutton():
            MN.click_screen_area(0.87, 0.31328125, 0.955, 0.3515625)

        guardcrownviewbutton = B.Button(detect_guardcrownviewbutton, click_guardcrownviewbutton)

        def detect_guardcrownview():
            detect_guardcrownview.cxlist = [0.325, 0.7475, 0.84625, 0.7, 0.515, 0.33125, 0.1975, 0.33875, 0.10375,
                                            0.79375]
            detect_guardcrownview.cylist = [0.43984375, 0.43984375, 0.25, 0.234375, 0.2140625, 0.22578125, 0.24453125,
                                            0.15703125, 0.1671875, 0.15]
            detect_guardcrownview.clist = [C.Color(29, 21, 13), C.Color(29, 21, 13), C.Color(196, 154, 139),
                                           C.Color(255, 233, 224), C.Color(229, 187, 171), C.Color(121, 105, 83),
                                           C.Color(164, 164, 164), C.Color(80, 21, 21), C.Color(47, 39, 31),
                                           C.Color(47, 39, 31)]
            return all(map(MN.color_comp, detect_guardcrownview.cxlist, detect_guardcrownview.cylist,
                           detect_guardcrownview.clist))

        guardcrownview = Context("guardcrownview", guardcrownviewbutton, detect_guardcrownview)


        def click_rewardscartreturnviewbutton():
            MN.click_screen_area(0.125, 0.03671875, 0.8575, 0.22734375)

        rewardscartreturnviewbutton = B.Button(None, click_rewardscartreturnviewbutton)


        def find_rewardscartview(debug=True):
            scanpath = 'images/results/rewardscartview.png'
            im = MN.full_screen_shot()
            im.save(scanpath, 'PNG')
            if (debug):
                return IM.match_template_debug(scanpath, ['images/templates/rewardscartwide.png'], 'rewardscartview')
            return IM.match_template(scanpath,
                                     ['images/templates/rewardscartwide.png'])


        def detect_rewardscartreceiptview():
            detect_rewardscartreceiptview.cxlist = [0.19375, 0.3325, 0.67, 0.78, 0.79125, 0.84375]
            detect_rewardscartreceiptview.cylist = [0.30390625, 0.28359375, 0.2828125, 0.290625, 0.4, 0.45]
            detect_rewardscartreceiptview.clist = [C.Color(210, 185, 143), C.Color(87, 0, 0), C.Color(82, 0, 0),
                                            C.Color(197, 172, 130), C.Color(166, 133, 83), C.Color(179, 139, 88)]
            return all(map(MN.color_comp, detect_rewardscartreceiptview.cxlist, detect_rewardscartreceiptview.cylist,
                           detect_rewardscartreceiptview.clist))

        rewardscartview = ImageContext('rewardscartview', None, find_rewardscartview)
        rewardscartreceiptview = Context('rewardscartreceiptview', None, detect_rewardscartreceiptview)
        rewardscartview.add_connection(rewardscartreceiptview)

        def find_alliancequestview(debug=True):
            scanpath = 'images/results/alliancequestview.png'
            im = MN.full_screen_shot()
            im.save(scanpath, 'PNG')
            if (debug):
                return IM.match_template_debug(scanpath, ['images/templates/alliancequestview1.png',
                                                          'images/templates/alliancequestviewwide.png'],
                                               'alliancequestview', threshold=0.65)
            return IM.match_template(scanpath, ['images/templates/alliancequestview1.png',
                                                'images/templates/alliancequestviewwide.png'], threshold=0.65)

        def detect_alliancequestview():
            alliancequestview.cxlist = [0.36875, 0.6625, 0.3475, 0.155, 0.1925, 0.08375, 0.3625, 0.35625, 0.36875,
                                        0.39625, 0.21625]
            alliancequestview.cylist = [0.0375, 0.040625, 0.25390625, 0.284375, 0.27890625, 0.2875, 0.48203125,
                                        0.6109375, 0.70625, 0.953125, 0.953125]
            alliancequestview.clist = [C.Color(103, 27, 22), C.Color(89, 23, 21), C.Color(206, 181, 123),
                                       C.Color(68, 167, 43), C.Color(38, 18, 14), C.Color(23, 7, 1),
                                       C.Color(207, 182, 117), C.Color(27, 27, 19), C.Color(208, 183, 123),
                                       C.Color(63, 91, 6), C.Color(16, 13, 9)]
            return all(map(MN.color_comp, alliancequestview.cxlist, alliancequestview.cylist, alliancequestview.clist))

        alliancequestview = ImageContext("alliancequestview", detect_alliancequestview, find_alliancequestview)

        def detect_alliancequestcollectview():
            detect_alliancequestcollectview.cxlist = [0.40625, 0.60375]
            detect_alliancequestcollectview.cylist = [0.9546875, 0.95546875]
            detect_alliancequestcollectview.clist = [C.Color(56, 87, 0), C.Color(58, 83, 5)]
            return all(map(MN.color_comp, detect_alliancequestcollectview.cxlist, detect_alliancequestcollectview.cylist,
                           detect_alliancequestcollectview.clist))

        def click_alliancequestcollectview():
            MN.click_screen_area(0.37, 0.934375, 0.62625, 0.971875)

        alliancequestcollectviewbutton = B.Button(detect_alliancequestcollectview, click_alliancequestcollectview)


        alliancequestcollectview = Context('alliancequestcollectview', alliancequestcollectviewbutton, detect_dailyrewardreceiptview)
        alliancequestreturnview = Context('alliancequestreturnview', returnbutton, detect_alliancequestview)
        alliancequestcollectview.add_connection(alliancequestreturnview)
        alliancequestview.add_connection(alliancequestcollectview)
        alliancequestcollectview.add_connection(alliancequestreturnview)




        def detect_fooddepotspentviewbutton():
            detect_fooddepotspentviewbutton.cxlist = [0.29, 0.255, 0.225]
            detect_fooddepotspentviewbutton.cylist = [0.496875, 0.49453125, 0.50234375]
            detect_fooddepotspentviewbutton.clist = [C.Color(191, 143, 87), C.Color(4, 11, 11), C.Color(222, 197, 116)]
            return all(
                map(MN.color_comp, detect_fooddepotspentviewbutton.cxlist, detect_fooddepotspentviewbutton.cylist,
                    detect_fooddepotspentviewbutton.clist))

        def click_fooddepotspentviewbutton():
            MN.click_screen_area(0.11125, 0.446875, 0.39375, 0.5765625)

        fooddepotspentviewbutton = B.Button(detect_fooddepotspentviewbutton, click_fooddepotspentviewbutton)

        def detect_fooddepotspentview():
            detect_fooddepotspentview.cxlist = [0.285, 0.24625, 0.22625, 0.19625]
            detect_fooddepotspentview.cylist = [0.4890625, 0.48671875, 0.5015625, 0.6125]
            detect_fooddepotspentview.clist = [C.Color(221, 189, 121), C.Color(2, 8, 8), C.Color(202, 160, 87),
                                          C.Color(254, 201, 242)]
            return all(map(MN.color_comp, detect_fooddepotspentview.cxlist, detect_fooddepotspentview.cylist,
                           detect_fooddepotspentview.clist))

        fooddepotspentview = Context("fooddepotspentview", fooddepotspentviewbutton, detect_fooddepotspentview)

        def detect_fooddepotview():
            detect_fooddepotview.cxlist = [0.28125, 0.2275, 0.1725, 0.20375]
            detect_fooddepotview.cylist = [0.48984375, 0.5046875, 0.51171875, 0.6203125]
            detect_fooddepotview.clist = [C.Color(165, 128, 60), C.Color(177, 136, 66), C.Color(9, 30, 37),
                                          C.Color(50, 47, 43)]
            return all(map(MN.color_comp, detect_fooddepotview.cxlist, detect_fooddepotview.cylist,
                           detect_fooddepotview.clist))

        fooddepotview = Context("fooddepotview", None, detect_fooddepotview)


        def detect_wooddepotspentviewbutton():
            detect_wooddepotspentviewbutton.cxlist = [0.7275, 0.76375, 0.845]
            detect_wooddepotspentviewbutton.cylist = [0.51953125, 0.49921875, 0.5]
            detect_wooddepotspentviewbutton.clist = [C.Color(181, 147, 79), C.Color(175, 158, 90), C.Color(7, 10, 14)]
            return all(
                map(MN.color_comp, detect_wooddepotspentviewbutton.cxlist, detect_wooddepotspentviewbutton.cylist,
                    detect_wooddepotspentviewbutton.clist))

        def click_wooddepotspentviewbutton():
            MN.click_screen_area(0.62125, 0.44765625, 0.88375, 0.57109375)

        wooddepotspentviewbutton = B.Button(detect_wooddepotspentviewbutton, click_wooddepotspentviewbutton)

        def detect_wooddepotspentview():
            detect_wooddepotspentview.cxlist = [0.74625, 0.73, 0.68625, 0.69375]
            detect_wooddepotspentview.cylist = [0.49453125, 0.5171875, 0.54765625, 0.61171875]
            detect_wooddepotspentview.clist = [C.Color(194, 170, 104), C.Color(181, 148, 74), C.Color(3, 20, 27),
                                          C.Color(255, 194, 242)]
            return all(map(MN.color_comp, detect_wooddepotspentview.cxlist, detect_wooddepotspentview.cylist,
                           detect_wooddepotspentview.clist))

        wooddepotspentview = Context("wooddepotspentview", wooddepotspentviewbutton, detect_wooddepotspentview)

        def detect_wooddepotview():
            detect_wooddepotview.cxlist = [0.75375, 0.73125, 0.69375, 0.705]
            detect_wooddepotview.cylist = [0.496875, 0.5171875, 0.54609375, 0.61953125]
            detect_wooddepotview.clist = [C.Color(202, 185, 111), C.Color(182, 149, 75), C.Color(6, 26, 32),
                                          C.Color(45, 44, 40)]
            return all(map(MN.color_comp, detect_wooddepotview.cxlist, detect_wooddepotview.cylist,
                           detect_wooddepotview.clist))

        wooddepotview = Context("wooddepotview", None, detect_wooddepotview)


        def detect_irondepotspentviewbutton():
            detect_irondepotspentviewbutton.cxlist = [0.79375, 0.70375, 0.66]
            detect_irondepotspentviewbutton.cylist = [0.7984375, 0.81171875, 0.8171875]
            detect_irondepotspentviewbutton.clist = [C.Color(146, 146, 154), C.Color(103, 103, 111),
                                                     C.Color(29, 55, 69)]
            return all(
                map(MN.color_comp, detect_irondepotspentviewbutton.cxlist, detect_irondepotspentviewbutton.cylist,
                    detect_irondepotspentviewbutton.clist))

        def click_irondepotspentviewbutton():
            MN.click_screen_area(0.61875, 0.74375, 0.89375, 0.87578125)

        irondepotspentviewbutton = B.Button(detect_irondepotspentviewbutton, click_irondepotspentviewbutton)

        def detect_irondepotspentview():
            detect_irondepotspentview.cxlist = [0.7225, 0.78, 0.6975, 0.69625]
            detect_irondepotspentview.cylist = [0.775, 0.80390625, 0.8015625, 0.9140625]
            detect_irondepotspentview.clist = [C.Color(160, 160, 169), C.Color(139, 139, 146), C.Color(108, 108, 116),
                                          C.Color(254, 234, 249)]
            return all(map(MN.color_comp, detect_irondepotspentview.cxlist, detect_irondepotspentview.cylist,
                           detect_irondepotspentview.clist))

        irondepotspentview = Context("irondepotspentview", irondepotspentviewbutton, detect_irondepotspentview)

        def detect_irondepotview():
            detect_irondepotview.cxlist = [0.7925, 0.7025, 0.82875, 0.7]
            detect_irondepotview.cylist = [0.79765625, 0.80078125, 0.77421875, 0.915625]
            detect_irondepotview.clist = [C.Color(140, 140, 148), C.Color(116, 116, 124), C.Color(10, 17, 17),
                                          C.Color(59, 53, 47)]
            return all(map(MN.color_comp, detect_irondepotview.cxlist, detect_irondepotview.cylist,
                           detect_irondepotview.clist))

        irondepotview = Context("irondepotview", None, detect_irondepotview)

        def detect_stonedepotview():
            detect_stonedepotview.cxlist = [0.265, 0.355, 0.12375, 0.19875]
            detect_stonedepotview.cylist = [0.803125, 0.81875, 0.75390625, 0.91875]
            detect_stonedepotview.clist = [C.Color(204, 217, 219), C.Color(14, 39, 60), C.Color(7, 26, 37),
                                           C.Color(51, 51, 45)]
            return all(map(MN.color_comp, detect_stonedepotview.cxlist, detect_stonedepotview.cylist,
                           detect_stonedepotview.clist))

        stonedepotview = Context("stonedepotview", None, detect_stonedepotview)

        def detect_stonedepotspentviewbutton():
            detect_stonedepotspentviewbutton.cxlist = [0.2675, 0.24625]
            detect_stonedepotspentviewbutton.cylist = [0.79921875, 0.815625]
            detect_stonedepotspentviewbutton.clist = [C.Color(184, 209, 212), C.Color(51, 59, 68)]
            return all(map(MN.color_comp, detect_stonedepotspentviewbutton.cxlist, detect_stonedepotspentviewbutton.cylist,
                           detect_stonedepotspentviewbutton.clist))

        def click_stonedepotspentviewbutton():
            MN.click_screen_area(0.12, 0.7375, 0.3925, 0.87109375)

        stonedepotspentviewbutton = B.Button(detect_stonedepotspentviewbutton, click_stonedepotspentviewbutton)

        def detect_stonedepotspentview():
            detect_stonedepotspentview.cxlist = [0.20125, 0.30375, 0.1175]
            detect_stonedepotspentview.cylist = [0.9140625, 0.92109375, 0.92734375]
            detect_stonedepotspentview.clist = [C.Color(254, 227, 244), C.Color(53, 48, 46), C.Color(48, 46, 41)]
            return all(
                map(MN.color_comp, detect_stonedepotspentview.cxlist, detect_stonedepotspentview.cylist, detect_stonedepotspentview.clist))


        stonedepotspentview = Context("stonedepotspentview", stonedepotspentviewbutton, detect_stonedepotspentview)


        def find_depotview(debug=True):
            scanpath = 'images/results/depotview.png'
            im = MN.full_screen_shot()
            im.save(scanpath, 'PNG')
            if (debug):
                return IM.match_template_debug(scanpath, ['images/templates/depotviewwide.png',
                                                          'images/templates/depotviewicon.png'], 'depotview')
            return IM.match_template(scanpath, ['images/templates/depotviewwide.png',
                                                'images/templates/depotviewicon.png'])

        def detect_depotview():
            detect_depotview.cxlist = [0.16875, 0.3575, 0.62875, 0.88, 0.77125, 0.20125, 0.2525, 0.04375, 0.02125,
                                       0.24375, 0.19125, 0.4775, 0.495, 0.5025]
            detect_depotview.cylist = [0.02890625, 0.02890625, 0.0375, 0.0390625, 0.18046875, 0.1515625, 0.16484375,
                                       0.115625, 0.19375, 0.23046875, 0.24296875, 0.23515625, 0.45546875, 0.77890625]
            detect_depotview.clist = [C.Color(46, 46, 46), C.Color(107, 26, 22), C.Color(122, 29, 24),
                                      C.Color(0, 34, 51), C.Color(207, 183, 173), C.Color(204, 171, 97),
                                      C.Color(147, 106, 65), C.Color(18, 18, 68), C.Color(13, 13, 62),
                                      C.Color(35, 43, 101), C.Color(119, 119, 127), C.Color(102, 77, 77),
                                      C.Color(34, 30, 21), C.Color(22, 17, 12)]
            return all(map(MN.color_comp, detect_depotview.cxlist, detect_depotview.cylist, detect_depotview.clist))

        depotview = ImageContext("depotview", detect_depotview, find_depotview)

        def detect_constructionview():
            detect_constructionview.cxlist = [0.3575, 0.61875, 0.94625, 0.83125, 0.80875, 0.08375, 0.53]
            detect_constructionview.cylist = [0.03046875, 0.028125, 0.1, 0.08828125, 0.10546875, 0.10078125, 0.11796875]
            detect_constructionview.clist = [C.Color(109, 27, 22), C.Color(134, 34, 24), C.Color(20, 98, 131),
                                             C.Color(37, 145, 175), C.Color(16, 82, 111), C.Color(171, 138, 96),
                                             C.Color(30, 26, 24)]
            return all(map(MN.color_comp, detect_constructionview.cxlist, detect_constructionview.cylist,
                           detect_constructionview.clist))

        constructionview = Context("constructionview", None, detect_constructionview)

        def find_dailyrewardsview(debug=False):
            scanpath = 'images/results/dailyrewardsview.png'
            im = MN.full_screen_shot()
            im.save(scanpath, 'PNG')
            if (debug):
                return IM.match_template_debug(scanpath, ['images/templates/dailyrewardview1.png',
                                                          'images/templates/dailyrewardview2.png'], 'dailyrewardsview')
            return IM.match_template(scanpath,
                                     ['images/templates/dailyrewardview1.png', 'images/templates/dailyrewardview2.png'])

        def detect_dailyrewardsview():
            detect_dailyrewardsview.cxlist = []
            detect_dailyrewardsview.cylist = []
            detect_dailyrewardsview.clist = []
            return all(map(MN.color_comp, detect_dailyrewardsview.cxlist, detect_dailyrewardsview.cylist,
                           detect_dailyrewardsview.clist))

        dailyrewardsview = ImageContext("dailyrewardsview", detect_dailyrewardsview, find_dailyrewardsview)


        def find_alliancehelpbirdview(debug=True):
            scanpath = 'images/results/alliancehelpbirdview.png'
            im = MN.full_screen_shot()
            im.save(scanpath, 'PNG')
            if (debug):
                return IM.match_template_debug(scanpath, ['images/templates/alliancehelpbird.png',
                                                          'images/templates/alliancehelpbirdwide.png'],
                                               'alliancehelpbirdview', threshold=0.65)
            return IM.match_template(scanpath, ['images/templates/alliancehelpbird.png',
                                                'images/templates/alliancehelpbirdwide.png'],threshold=0.65)


        alliancehelpbirdview = ImageContext("alliancehelpbirdview", None,
                                            find_alliancehelpbirdview)

        cityview.add_connection(stonequarryview)
        cityview.add_connection(ironmineview)
        cityview.add_connection(foodfarmview)
        cityview.add_connection(woodyardview)
        cityview.add_connection(rewardscartview)
        cityview.add_connection(alliancehelpbirdview)
        cityview.add_connection(alliancequestview)
        cityview.add_connection(constructionview)
        cityview.add_connection(goldenhammerview)
        cityview.add_connection(guardcrownview)
        cityview.add_connection(depotview)
        cityview.add_connection(removablebuildingdetailview)
        cityview.add_connection(unremovablebuildingdetailview)
        cityview.add_connection(tipsladyview)

#--------------------------------------------special buttons-------------------------------------------------------

        def detect_mapviewbutton():
            return MN.color_comp(0.07, 0.96171875, C.Color(185, 185, 67)) and \
                   MN.color_comp(0.1125, 0.95234375, C.Color(173, 178, 39)) and \
                   MN.color_comp(0.11625, 0.92109375, C.Color(126, 132, 129)) and \
                   MN.color_comp(0.0575, 0.92265625, C.Color(78, 82, 84)) and \
                   MN.color_comp(0.14875, 0.921875, C.Color(79, 82, 85)) and \
                   MN.color_comp(0.12, 0.98125, C.Color(39, 23, 0))

        def click_mapviewbutton():
            MN.click_screen_area(0.055, 0.925, 0.1625, 0.97265625)

        mapviewbutton = B.Button(detect_mapviewbutton, click_mapviewbutton)


        mapview = Context("mapview",mapviewbutton,detect_mapview)

        def detect_returnmapbutton():
            return MN.color_comp(0.08875, 0.01484375, C.Color(140, 124, 91)) and \
                   MN.color_comp(0.0475, 0.0234375, C.Color(73, 60, 40)) and \
                   MN.color_comp(0.03625, 0.0359375, C.Color(147, 131, 98))

        def click_returnmapbutton():
            MN.click_screen_area(0.02, 0.0125, 0.095, 0.04375)
            button_mapview = Context.waitformultiload([cityview, mapview])
            if button_mapview is None:
                return
            if button_mapview.name == 'cityview':
                cityview.get_connection('mapview').click_and_wait()


        returnmapbutton = B.Button(detect_returnmapbutton, click_returnmapbutton)

        def detect_returncitybutton():
            return MN.color_comp(0.08875, 0.01484375, C.Color(140, 124, 91)) and \
                   MN.color_comp(0.0475, 0.0234375, C.Color(73, 60, 40)) and \
                   MN.color_comp(0.03625, 0.0359375, C.Color(147, 131, 98))

        def click_returncitybutton():
            MN.click_screen_area(0.02, 0.0125, 0.095, 0.04375)
            button_cityview = Context.waitformultiload([cityview,mapview])
            if button_cityview is None:
                return
            if button_cityview.name == 'mapview':
                mapview.get_connection('cityview').click_and_wait()


        returncitybutton = B.Button(detect_returncitybutton, click_returncitybutton)

        def detect_adorrewardviewbutton():
            return MN.color_comp(0.2825, 0.52734375, C.Color(45, 48, 49)) and \
                   MN.color_comp(0.34625, 0.5609375, C.Color(196, 73, 19)) and \
                   MN.color_comp(0.28625, 0.53671875, C.Color(233, 210, 179)) and \
                   MN.color_comp(0.2825, 0.5703125, C.Color(22, 22, 23))

        def click_appicon():
            MN.click_screen_area(0.28625, 0.53046875, 0.3525, 0.56875)

        def process_blockers():
            button_adorrewardview = Context.waitformultiload(
                [adview, altadview, altaltadview, dailyrewardview, cityview], timeout=20)
            if button_adorrewardview is None:
                cityview.return_context()

            loadreturn = button_adorrewardview
            if loadreturn is None:
                cityview.return_context()
                loadreturn = Context.waitformultiload([adview, altadview, altaltadview, dailyrewardview, cityview]).name
            else:
                loadreturn = loadreturn.name
            if (loadreturn == 'adview' or loadreturn == 'altadview' or loadreturn == 'altaltadview'):
                print('detected adview')
                click_adexitviewbutton()
                button_rewardorcityview = Context.waitformultiload([dailyrewardview, cityview])
                if (button_rewardorcityview == None):
                    cityview.reset_context()
                elif (button_rewardorcityview.name == 'dailyrewardview'):
                    print('detected dailyrewardview')
                    dailyrewardreceiptview.click_and_wait()
                    dailyrewardreceiptview.get_connection('cityview').click_and_wait()
            elif (loadreturn == 'dailyrewardview'):
                print('detected dailyrewardview')
                dailyrewardreceiptview.click_and_wait()
                dailyrewardreceiptview.get_connection('cityview').click_and_wait()

        def click_adorrewardviewbutton():
            click_appicon()
            process_blockers()


        adorrewardviewbutton = B.Button(detect_adorrewardviewbutton, click_adorrewardviewbutton)

        def detect_alliancedonateallviewbutton():
            detect_alliancedonateallviewbutton.cxlist = [0.4]
            detect_alliancedonateallviewbutton.cylist = [0.6546875]
            detect_alliancedonateallviewbutton.clist = [C.Color(5, 72, 86)]
            return all(
                map(MN.color_comp, detect_alliancedonateallviewbutton.cxlist, detect_alliancedonateallviewbutton.cylist,
                    detect_alliancedonateallviewbutton.clist))

        def click_alliancedonateallviewbutton():
            MN.click_screen_area_fast(0.165, 0.640625, 0.41625, 0.66875, 9)
            MN.robot_sleep(3000)
            alliancedonatepostview = Context.waitformultiload([alliancedonateallview, alliancedonateresetview, alliancedonateview])
            if (alliancedonatepostview.name == 'alliancedonateallview'):
                alliancedonateallreturnviewbutton.click()
            elif (alliancedonatepostview.name == 'alliancedonateresetview'):
                alliancedonateresetreturnviewbutton.click()

        alliancedonateallviewbutton = B.Button(detect_alliancedonateallviewbutton, click_alliancedonateallviewbutton)

        alliancedonatepostview = copy.copy(alliancedonateview)
        alliancedonatepostview.setbutton(alliancedonateallviewbutton)
        alliancedonateview.add_connection(alliancedonatepostview)

        harvestskillview = copy.copy(skillactivateview)
        harvestskillview.setbutton(harvestskillviewbutton)
        harvestskillview.add_option(harvestskillcooldownview)
        harvestskillview.add_option(harvestskillaccessview)
        skillactivateview.add_connection(harvestskillview)

        mapview.add_connection(woodtileview)
        mapview.add_connection(skillactivateview)
        mapview.add_connection(accountview)
        mapview.add_connection(vipview)
        mapview.add_connection(purchaseview)
        mapview.add_connection(questview)
        mapview.add_connection(packview)
        mapview.add_connection(mailview)
        mapview.add_connection(allianceview)
        mapview.add_connection(lordinfoview)
        # mapview.add_connection(bookmarksview)
        # mapview.add_connection(globalmapview)
        # mapview.add_connection(mapsearchview)
        # mapview.add_connection(allycityview)
        # mapview.add_connection(enemycityview)
        # mapview.add_connection(emptylandview)
        # mapview.add_connection(monsterview)
        # mapview.add_connection(tileview)
        # mapview.add_connection(alliancebuildingview)
        mapview.add_connection(newachievementview)
        mapview.add_connection(coordinputview)

        marchsetoutview = copy.copy(mapview)
        marchsetoutview.setbutton(marchsetoutbutton)
        battlerebelssuppressview.add_connection(marchsetoutview)
        rallyrebelsview.add_connection(marchsetoutview)



        mapview.add_connection(cityview)
        cityview.add_connection(mapview)

        returnmapview = copy.copy(mapview)
        returnmapview.setbutton(returnmapbutton)
        questview.add_connection(returnmapview)
        packview.add_connection(returnmapview)
        mailview.add_connection(returnmapview)
        allianceview.add_connection(returnmapview)
        lordinfoview.add_connection(returnmapview)
        accountview.add_connection(returnmapview)
        vipview.add_connection(returnmapview)
        purchaseview.add_connection(returnmapview)
        harvestskillview.add_connection(returnmapview)
        skillactivateview.add_connection(returnmapview)
        newachievementview.add_connection(returnmapview)



        returncityview = copy.copy(cityview)
        returncityview.setbutton(returncitybutton)
        questview.add_connection(returncityview)
        packview.add_connection(returncityview)
        mailview.add_connection(returncityview)
        allianceview.add_connection(returncityview)
        lordinfoview.add_connection(returncityview)
        accountview.add_connection(returncityview)
        vipview.add_connection(returncityview)
        purchaseview.add_connection(returncityview)
        workshopview.add_connection(returncityview)
        constructionview.add_connection(returncityview)
        alliancequestview.add_connection(returncityview)
        depotview.add_connection(returncityview)
        removablebuildingdetailview.add_connection(returncityview)
        newachievementview.add_connection(returncityview)
        tipsladyview.add_connection(returncityview)
        guardcrownview.add_connection(returncityview)
        harvestskillview.add_connection(returncityview)
        skillactivateview.add_connection(returncityview)

        alliancereturnview = copy.copy(allianceview)
        alliancereturnview.setbutton(returnbutton)
        alliancetechview.add_connection(alliancereturnview)
        alliancebattleview.add_connection(alliancereturnview)

        returnaccountview = copy.copy(accountview)
        returnaccountview.setbutton(returnbutton)
        accountaccountview.add_connection(returnaccountview)

        googleplayfailreturnview = copy.copy(cityview)
        googleplayfailreturnview.setbutton(googleplayfailreturnbutton)
        googleplayfailreturnview.add_connection(googleplayfailreturnview)

        goldenhammerreturnview = copy.copy(cityview)
        goldenhammerreturnview.setbutton(goldenhammerreturnviewbutton)
        goldenhammerview.add_connection(goldenhammerreturnview)





        alliancetechreturnview = copy.copy(alliancetechview)
        alliancetechreturnview.setbutton(alliancetechreturnviewbutton)
        alliancedonateview.add_connection(alliancetechreturnview)



        rewardcityview = copy.copy(cityview)
        rewardcityview.setbutton(dailyrewardcityviewbutton)
        dailyrewardreceiptview.add_connection(rewardcityview)

        rewardscartreturnview = copy.copy(cityview)
        rewardscartreturnview.setbutton(rewardscartreturnviewbutton)
        rewardscartreceiptview.add_connection(rewardscartreturnview)

        optionaldailyrewardview = ConditionalContext('optionaldailyrewardview', adorrewardviewbutton)
        optionaldailyrewardview.setbutton(adexitviewbutton)
        optionaldailyrewardview.add_option(dailyrewardview)
        optionaldailyrewardview.add_option(cityview)
        adview.add_connection(optionaldailyrewardview)
        altadview.add_connection(optionaldailyrewardview)
        altaltadview.add_connection(optionaldailyrewardview)

        phonetocityview = copy.copy(cityview)
        phonetocityview.setbutton(adorrewardviewbutton)

        farmswitchtocityview = copy.copy(cityview)
        farmswitchtocityview.setbutton(farmswitchconfirmbutton)
        farm0pos.add_connection(farmswitchtocityview)
        farm1pos.add_connection(farmswitchtocityview)

        phonehomescreen.add_connection(phonetocityview)
        phonehomescreen.add_option(adview)
        phonehomescreen.add_option(altadview)
        phonehomescreen.add_option(altaltadview)
        phonehomescreen.add_option(dailyrewardview)
        phonehomescreen.add_option(optionaldailyrewardview)



        return phonehomescreen

class ImageContext(Context):
    def __init__(self, name, detector, find):
        Context.__init__(self, name, None, detector)
        self.find = find
        self.coordlist = []
        self.buttonlist = []
        self.buttonindex = 0

    @staticmethod
    def create_clickfunc(x, y):
        def clickfunc():
            MN.click_screen_loc(x, y)
        return clickfunc
    @staticmethod
    def create_fastclickfunc(x, y):
        def clickfunc():
            MN.click_screen_loc_fast(x, y)
        return clickfunc

    def create_buttons(self, debug=False):
        self.coordlist = self.find()
        coordlistlen = len(self.coordlist)
        if(coordlistlen>0):
            self.buttonlist = []
            for coord in self.coordlist:
                if(debug):
                    print(str(coord[0]) + ', ' + str(coord[1]))
                    click_selfbutton = self.create_fastclickfunc(coord[0], coord[1])
                else:
                    click_selfbutton = self.create_clickfunc(coord[0],coord[1])
                if(click_selfbutton == None):
                    print('declaration failed!')
                b = B.Button(default_waitfunc, click_selfbutton)
                self.buttonlist.append(b)
            self.buttonindex = 0
            self.button = self.buttonlist[0]
            print('found ' + str(len(self.buttonlist)) + ' ' + self.name +'\'s')
            return coordlistlen
        else:
            print('no ' + self.name +'\'s found!')
            self.button = None
            return 0

    def next_button(self):
        self.buttonindex += 1
        self.button = self.buttonlist[self.buttonindex]
    def next(self):
        return self.next_button()

    def has_next(self):
        return self.buttonindex < len(self.buttonlist)-1

    def hasnextbutton(self):
        return self.has_next()

    def get_coordlist(self):
        return self.coordlist

    def get_coord(self):
        return self.coordlist[self.buttonindex]

    def get_relative_context(self, name):
        context = self.get_connection(name)
        current_coord = self.get_coord()
        context.add_coord(current_coord)

    def click_button(self):
        if(self.button == None):
            print('no ' + self.name + '\'s found!')
        else:
            Context.click_button(self)

    def click_all(self, homecontext = None, debug = False):
        nbuttons = self.create_buttons(debug=debug)
        while (self.hasnextbutton()):
            self.click_button()
            self.next_button()
        if(homecontext != None):
            if (not homecontext.detect()):
                homecontext.waitforload(timeout=1)
        return nbuttons



class RelativeContext(Context):
    def __init__(self, name, relative_button, detector):
        Context.__init__(self, name, relative_button, detector)
        self.coord = None

    def add_coord(self,coord):
        self.coord = coord

    def click_button(self):
        if(self.coord == None):
            print('Context not initialized!')
        else:
            self.button(self.coord[0],self.coord[1])
            self.coord = None

class ConditionalContext(Context):
    def __init__(self, name, button):
        Context.__init__(self, name, button, None)
        self.currentoption = None

    def add_option(self,context):
        self.optionlist.append(context)

    def add_options(self, contextlist):
        self.optionlist.extend(contextlist)

    def get_option(self, optionname):
        for option in self.optionlist:
            if(option.name == optionname):
                return option
        print('option ' + optionname + ' not found!')
        return None

    def choose(self):
        for option in self.optionlist:
            if option.detect():
                self.optionname = option.name
                self.button = option.button
                self.detector = option.detector
                return True
        return False

    def detect_all(self):
        detected = False
        for option in self.optionlist:
            # print('testing for: ' + option.name + ': ' + str(option.detect()))
            detected = detected or option.detect()
            # print('detected: ' + str(detected))
        return detected

    def waitforload(self, timeout = 5, ontimeout = None):
        while(not self.choose()):
            if (Context.detect_camelloadingscreen()):
                print('detected camelloadingscreen')
                MN.robot_sleep(4000)
            elif (Context.detect_waoserverfetch()):
                print('detected waoserverfetch')
                MN.robot_sleep(4000)
            elif (Context.detect_waoclientsideload()):
                print('detected waoclientsideload')
                MN.robot_sleep(4000)
            else:
                if(timeout > 0):
                    MN.robot_sleep(350)
                    timeout -= 0.5
                    if (timeout % 1 == 0):
                        print('waiting for ' + self.getname() + ' load... ' + str(timeout))
                else:
                    print(self.getname() + ' timed out!')
                    if (ontimeout == None):
                        self.return_context()
                        return self.waitforload()
                    else:
                        return ontimeout()
        return self
    #this could be a recursion problem
    def detect(self):
        detected = False
        for option in self.optionlist:
            if(option.detect != None):
                detected = detected or option.detect()
        return detected

    def return_context(self):
        print('returning to context: '+self.name)
        if(Context.detect_waocrash()):
            MN.close_memu()
            MN.open_memu()
        else:
            firstcontextlist = []
            found = False
            for option in self.optionlist:
                print('testing option: ' + option.name)
                found = option.cycle_contexts()
                if found is not None:
                    return found
            print('unable to find context')
        return self.reset_context()


    def tunnel_context(self, findname):
        for option in self.optionlist:
            checkresult = option.check_tunnel_context(findname)
            if checkresult is not None:
                return checkresult
        return None
