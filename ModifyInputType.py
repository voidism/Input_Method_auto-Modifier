import pythoncom
import pyHook
from pymouse import *
from pykeyboard import *
import ctypes
import pyautogui
import json
import os
import requests


def IsZhInput(words):
    bpmf = [49, 113, 97, 122, 50, 119, 115, 120, 101,\
     100, 99, 114, 102, 118, 53, 116, 103, 98, 121, 104, 110]
    iwu = [117, 106, 109]
    aouh = [56, 105, 107, 44, 57, 111, 108, 46, 48, 112, 59, 47]
    tone = [32, 54, 51, 52, 55]
    if len(words) == 2:
        if words[0] in [53, 116, 103, 98, 121, 104, 110, 117, \
                        106, 109, 56, 105, 107, 44, 57, 111, \
                        108, 46, 48, 112, 59, 45]:
            if words[1] in tone:
                return True
    if len(words) == 3:
        if (words[0] in bpmf) and (words[1] in iwu + aouh) and (words[2] in tone):
            return True
    if len(words) == 3:
        if (words[0] in iwu) and (words[1] in aouh) and (words[2] in tone):
            return True
    if len(words) == 4:
        if (words[0] in bpmf) and (words[1] in iwu) and (words[2] in aouh) and (words[3] in tone):
            return True
    return False


def IsZhInputs(alist):
    # type: (list) -> int
    if len(alist) >= 8:
        if IsZhInput(alist[-4:]) and IsZhInput(alist[-8:-4]):
            return 8
    if len(alist) >= 7:
        if IsZhInput(alist[-3:]) and IsZhInput(alist[-7:-3]):
            return 7
        elif IsZhInput(alist[-4:]) and IsZhInput(alist[-7:-4]):
            return 7
    if len(alist) >= 6:
        if IsZhInput(alist[-2:]) and IsZhInput(alist[-6:-2]):
            return 6
        elif IsZhInput(alist[-3:]) and IsZhInput(alist[-6:-3]):
            return 6
        elif IsZhInput(alist[-4:]) and IsZhInput(alist[-6:-4]):
            return 6
    if len(alist) >= 5:
        if IsZhInput(alist[-2:]) and IsZhInput(alist[-5:-2]):
            return 5
        elif IsZhInput(alist[-3:]) and IsZhInput(alist[-5:-3]):
            return 5
    if len(alist) >= 4:
        if IsZhInput(alist[-2:]) and IsZhInput(alist[-4:-2]):
            return 4

    return 0


if not os.path.exists('./EnWordBase.json'):
    web = requests.get(
        "https://raw.githubusercontent.com/voidism/Modify-Input-Type-Automatically/master/EnWordBase.json")
    dic = web.json()
    for i in range(len(dic['words'])):
        if not dic['words'][i].islower():
            dic['words'][i] = dic['words'][i].lower()
    with open('EnWordBase.json', 'w') as file1:
        json.dump(dic, file1)
    file1.close()
    #print 'Dictionary Loaded!'

with open('EnWordBase.json', 'r') as file2:
    ewb = json.load(file2)
file2.close()
ewords = ewb['words']


'''
def IsZhSingle(alist):
    # type: (list) -> int
    if len(alist) >= 4:
        if IsZhInput(alist[-2:]):
            return True
        elif IsZhInput(alist[-3:]):
            return True
        elif IsZhInput(alist[-4:]):
            return True
    if len(alist) >= 3:
        if IsZhInput(alist[-2:]):
            return True
        elif IsZhInput(alist[-3:]):
            return True
    if len(alist) >= 2:
        if IsZhInput(alist[-2:]):
            return True

    return False


def extZh(alist):
    if len(alist) >= 6:
        if not (IsZhSingle(alist[:-1]) or IsZhSingle(alist[:-2]) or IsZhSingle(alist[:-3])):
            return False
    return True
'''

def extEn(sus):
    if sus in ewords:
        return True
    else:
        return False


def OnKeyboardEvent(event):
    global InputType, ProgramPress, cur_words, cur_keys, susword, wn, shift_pressed#, alt_pressed
    if event.MessageName=='key up':# and not (event.KeyID in [161, 160]):event.Ascii != 0:
        if  (event.KeyID in [161, 160]):
            shift_pressed=0
            return True
        #elif (event.KeyID in [164, 165]):
            #alt_pressed=0
        else:
            return True

    bpmf = [49, 113, 97, 122, 50, 119, 115, 120, 101, 100, 99, 114, 102, 118, 116, 103, 98, 121, 104, 110]
    iwu = [117, 106, 109]
    aouh = [56, 105, 107, 44, 57, 111, 108, 46, 48, 112, 59, 47]
    tone = [32, 54, 51, 52, 55]
    pixel=(1683, 1063)
    if wn!=event.WindowName:
        wn=event.WindowName
        cur_words = []
        cur_keys = []
        susword = ""
    # Input is human
    if (ProgramPress == 0):
        #if (event.KeyID in [164, 165]):
            #alt_pressed = 1
            #return True
        if (event.KeyID in [161, 160]):
            shift_pressed=1
        if (event.KeyID in [161, 160]) and len(susword) > 2:
            #print 'Shift!'
            im = pyautogui.screenshot()
            if im.getpixel(pixel)[1]>=200:
                InputType = 1
            else:
                InputType = 0
            if InputType == 1:
                #print susword,'add to base!'
                ewb['words'].append(susword)
                with open('EnWordBase.json', 'w') as file1:
                    json.dump(ewb, file1)
                file1.close()
            #print event.Key
            cur_words = []
            cur_keys = []
            susword=""
            return True
        elif (event.Ascii == 8) and len(cur_words) > 0:
            del cur_keys[-1]
            del cur_words[-1]
            susword=susword[:-1]
        elif (event.Ascii == 8) and len(cur_words) == 0:
            #print event.Key
            return True
        elif (event.Ascii in [13, 0, 9]):
            #print event.Key
            cur_words = []
            cur_keys = []
            susword = ""
            return True
        else:
            cur_words.append(event.Ascii)
            cur_keys.append(chr(event.Ascii))
            susword=''.join([susword,chr(event.Ascii)])
            if (event.KeyID in [32]):
                susword = ""
        #print event, event.Ascii, cur_words
        #print susword, cur_keys

        im = pyautogui.screenshot()
        if im.getpixel(pixel)[1]>=200:
            InputType = 1
        else:
            InputType = 0

        # Input is En
        if (InputType == 0):
            if len(cur_keys) > 0:
                for i in range(len(susword)):
                    if extEn(susword[i:]):
                        cur_words = []
                        cur_keys = []
                        susword = ""
            if (cur_words == [122, 120, 99, 118]):
                ctypes.windll.user32.PostQuitMessage(0)

            temp=IsZhInputs(cur_words)
            if temp>0:
                #print('Shift to Zh')
                ProgramPress = (temp * 2)
                k.tap_key(k.shift_key)
                for i in range(temp - 1):
                    k.tap_key('\b')
                for i in cur_keys[-temp:]:
                    k.tap_key(i)
                cur_keys = []
                cur_words = []
                susword = ""
                return False
            else:
                return True
        # Input is Zh
        elif (InputType == 1):
            EnKey=[114, 102, 118, 98, 103, 116, 121, \
            104, 110, 109, 106, 117, 105, 107, 108, 111, 112, \
            122, 97, 113, 119, 115, 120, 99, 100, 101]
            #NumKey=[48, 57, 56, 55, 54, 53, 52, 51, 50, 49]
            if shift_pressed == 1:
                cur_keys=[]
                if event.Ascii not in EnKey:
                    susword=''
            '''
            if alt_pressed==1 and event.Ascii in NumKey:
                ProgramPress = 6
                alt_pressed = 0
                k.release_key(k.alt_key)
                k.tap_key(k.shift_key)
                k.tap_key(chr(event.Ascii))
                k.tap_key(k.shift_key)
                k.press_key(k.alt_key)
                alt_pressed = 1
            '''
            if (cur_words == [122, 120, 99, 118]):
                ctypes.windll.user32.PostQuitMessage(0)
            if len(cur_keys) > 0:
                for i in range(len(cur_words)):
                    if IsZhInput(cur_words[i:]):
                        cur_words = []
                        cur_keys = []
                        susword = ""
            '''         [114, 102, 118, 98, 103, 116, 121, \
            104, 110, 109, 106, 117, 105, 107, 108, 111, 112, \ 
            122, 97, 113, 119, 115, 120, 99, 100, 101]  
            if IsZhInputs(cur_words)>0:
                susword = ""
                cur_keys = []
                cur_words = []
            '''
            if extEn(susword):
                #print susword,
                #print 'Shift to En'
                ProgramPress = (len(cur_keys)+2)
                k.tap_key(k.escape_key)
                k.tap_key(k.shift_key)
                #pyautogui.typewrite(susword)
                for i in cur_keys:
                    k.tap_key(i)
                cur_keys = []
                cur_words = []
                susword = ""
                return False

            return True

    #Input is computer
    else:
        ProgramPress -= 1
        #print "computer",
        #print event.Ascii, cur_words
        #print cur_keys
        return True


if __name__ == "__main__":
    global k, InputType, ProgramPress, cur_words, cur_keys, susword, wn, shift_pressed#, alt_pressed
    InputType = 0
    ProgramPress = 0
    cur_words = []
    cur_keys = []
    susword=''
    wn=''
    shift_pressed=0
    #alt_pressed=0

    # m = PyMouse()
    k = PyKeyboard()

    # create a hook manager
    hm = pyHook.HookManager()
    # watch for all mouse events
    hm.KeyDown = OnKeyboardEvent
    hm.KeyUp = OnKeyboardEvent
    # set the hook
    hm.HookKeyboard()
    # wait forever
    pythoncom.PumpMessages()
