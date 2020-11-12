#!/usr/bin/python
# -*- coding: utf-8 -*-
  
from Quartz.CoreGraphics import *
from time import sleep
from AppKit import NSApplication, NSApp
from Foundation import NSObject, NSLog
from Cocoa import NSEvent, NSKeyDownMask
from PyObjCTools import AppHelper
import _thread

flag = False

# Keyboard Events
class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        mask = NSKeyDownMask
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(mask, handler)
        
# Where the magic begins
def handler(event):
    global flag

    try:
        # NSLog(u"%@", event)
        # print ('keycode: ' + str(event.keyCode()))

        if (int(event.keyCode()) == 6): # 6 - Z Key
            flag = not(flag)
            status = 'activated' if flag else 'deactivated'
            print('clicker ' + status)

            clicker()
        elif (int(event.keyCode()) == 53): # 53 - ESC Key 
            print('AppHelper.stopEventLoop()')
            AppHelper.stopEventLoop()
    except KeyboardInterrupt:
        print('KeyboardInterrupt -> AppHelper.stopEventLoop()')
        AppHelper.stopEventLoop()
    
# Mouse Events
def mouseEvent(type, posx, posy):  
    theEvent = CGEventCreateMouseEvent(None, type, (posx,posy), kCGMouseButtonLeft)
    result = CGEventPost(kCGHIDEventTap, theEvent)
    return result
    
def mouseclick(posx,posy):  
    up = mouseEvent(kCGEventLeftMouseDown, posx,posy)
    down = mouseEvent(kCGEventLeftMouseUp, posx,posy)

    print('Clicked at position x=' + str(posx) + ' y=' + str(posy))

    return str(up) + ' ' + str(down)

def sanitised_input(prompt, type_=None):
    value = input(prompt)
    if type_ is not None:
        try:
            value = type_(value)
        except ValueError:
            print("Input type must be {0}".format(type_.__name__))
            sanitised_input(prompt, type_)

            return

    return value

# the clicker
def clicker():
    global flag
    
    limit = -1
    sleep_interval = 0

    if flag:
        limit = sanitised_input("Maximum clicks: ", int)
        sleep_interval = sanitised_input("Delay between click (seconds): ", int)
    else:
        print('Clicker started...')
        print('Press Z to start auto click...')
    clicked_total = 0

    while(flag):
        if ((limit > 0) and (clicked_total >= limit)):
            print("Reached maximum clicks...")
            print("Press Z to auto click again OR ESC to stop...")

            flag = False
            break

        ourEvent = CGEventCreate(None)
        currentpos = CGEventGetLocation(ourEvent) # Save current mouse position
        mouseclick(int(currentpos.x),int(currentpos.y))

        print('Continuing after ' + str(sleep_interval) + ' seconds...')
        clicked_total = clicked_total + 1
        sleep(sleep_interval)
    
#main function
def main():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()
    
if __name__ == '__main__':
    _thread.start_new_thread(clicker,())
    main()
