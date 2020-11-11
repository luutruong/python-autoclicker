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
        NSLog(u"%@", event)
        print ('keycode: ' + str(event.keyCode()))

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

# the clicker
def clicker():
    global flag
    print('Clicker started...')

    while(flag):
        ourEvent = CGEventCreate(None)
        currentpos = CGEventGetLocation(ourEvent) # Save current mouse position
        mouseclick(int(currentpos.x),int(currentpos.y))

        print('Continuing after 5 seconds...')
        sleep(5)
    
#main function
def main():
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()
    
if __name__ == '__main__':
    _thread.start_new_thread(clicker,())
    main()
