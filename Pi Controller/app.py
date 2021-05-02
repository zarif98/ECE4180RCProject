#!/usr/bin/env python
# coding: Latin-1
# The code

# Load library functions we want
import time
import pygame
import serial

# Axis config for controller
leftThumbUpLeftRight = 0                #Joystick Axis Left Thumb
leftThumbUpDown = 1                     
leftTrig = 4                            #Joystick Axis Left Trigger
rightTrig = 5                           #Joystick Axis Right Trigger
aButton = 0                             #Joystick A Button
bButton = 1                             #Joystick B Button
interval = .1                          #Time between keyboard updates in seconds, smaller responds faster but uses more processor time

# Setup pygame and key states
global hadEvent
global moveQuit
global leftLeftRightVal 
global leftUpDownVal
global lTrigVal
global rTrigVal
global aVal
global bVal
leftLeftRightVal = 0
leftUpDownVal = 0
lTrigVal = -1
rTrigVal = -1
aVal = 0
bVal = 0
hadEvent = True
moveQuit = False
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
screen = pygame.display.set_mode([300,300])
pygame.display.set_caption("JoyBorg - Press [ESC] to quit")

# Function to handle pygame events
def PygameHandler(events):
    # Variables accessible outside this function
    global hadEvent
    global moveQuit
    global leftLeftRightVal 
    global leftUpDownVal
    global lTrigVal
    global rTrigVal
    global aVal
    global bVal
    # Handle each event individually
    for event in events:
        if event.type == pygame.QUIT:
            # User exit
            hadEvent = True
            moveQuit = True
        elif event.type == pygame.KEYDOWN:
            # A key has been pressed, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_ESCAPE:
                moveQuit = True
        elif event.type == pygame.KEYUP:
            # A key has been released, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_ESCAPE:
                moveQuit = False
        elif event.type == pygame.JOYAXISMOTION:
            # A joystick has been moved, read axis positions (-1 to +1)
            hadEvent = True
            leftLeftRightVal = joystick.get_axis(leftThumbUpLeftRight)
            leftUpDownVal = joystick.get_axis(leftThumbUpDown)
            lTrigVal = joystick.get_axis(leftTrig)
            rTrigVal = joystick.get_axis(rightTrig)
        elif event.type == pygame.JOYBUTTONDOWN:
            hadEvent = True
            aVal = joystick.get_button(aButton)
            bVal = joystick.get_button(bButton)
            
# Loop indefinitely
# Make Serial connection

print('Press [ESC] to quit')

while True:
    # Get the currently pressed keys on the keyboard
    PygameHandler(pygame.event.get())
    if hadEvent:
        # Keys have changed, generate the command list based on keys
        hadEvent = False
        if moveQuit:
            break
        # Write to Serial Port values:
        # left thumb x-axis, left thumb y-axis, left trigger, right trigger, a button, b button
        values = [leftLeftRightVal, leftUpDownVal, lTrigVal, rTrigVal, aVal, bVal]
        roundedvalues = [0,0,0,0,0,0]
        for i in range(len(values)):
            roundedvalues[i] = round(values[i],2)
        string = ' '.join(str(i) for i in roundedvalues)
        new_string = string.encode()
        print(new_string)
        device = serial.Serial('/dev/ttyACM0')
        device.write(new_string)
        device.close()
    # Wait for the interval period
    time.sleep(interval)

