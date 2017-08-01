# -*- coding: utf-8 -*-
import pythoncom
import pyHook
import pyautogui

def onMouseEvent(event):
    print "Position:", event.Position
    im = pyautogui.screenshot()
    print "RGB:",im.getpixel(event.Position)
    print "---"

    return True


def main():
    hm = pyHook.HookManager()
    hm.MouseAll = onMouseEvent
    hm.HookMouse()
    pythoncom.PumpMessages()


if __name__ == "__main__":
    main()
