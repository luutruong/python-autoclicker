#!/usr/bin/python
# -*- coding: utf-8 -*-
  
from Quartz.CoreGraphics import *
from time import sleep
from AppKit import NSApplication, NSApp
from Foundation import NSObject, NSLog
from Cocoa import NSEvent, NSKeyDownMask
from PyObjCTools import AppHelper
import _thread
import sys

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

    # print('\nClicked at position x=' + str(posx) + ' y=' + str(posy))

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
    time_eslapsed = 0
    currentpos = False

    while(flag):
        if ((limit > 0) and (clicked_total >= limit)):
            print("\nReached maximum clicks...")
            print("\nPress Z to auto click again OR ESC to stop...")

            flag = False
            break

        if (time_eslapsed - sleep_interval) == 1:
            ourEvent = CGEventCreate(None)
            currentpos = CGEventGetLocation(ourEvent) # Save current mouse position
            mouseclick(int(currentpos.x),int(currentpos.y))

            time_eslapsed = 0
            clicked_total = clicked_total + 1

        sys.stdout.write("\r")
        message = "Clicked at position x={0} y={1}. Total clicks {2}/{3}. Continuing {4} seconds...".format(
                int(currentpos.x) if currentpos else 0,
                int(currentpos.y) if currentpos else 0,
                clicked_total,
                limit,
                sleep_interval - time_eslapsed
            )
        sys.stdout.write(message)
        sys.stdout.flush()
        
        time_eslapsed = time_eslapsed + 1
        sleep(1)
    
#main function
def main():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()
    
if __name__ == '__main__':
    _thread.start_new_thread(clicker,())
    main()
