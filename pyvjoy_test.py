from vjoy import vj, setJoy
import numpy as np
import time

print("vj opening", flush=True)
vj.open()

time.sleep(1)


print("sending axes", flush=True)




def setJoy_throttle(valueX, valueY=0, scale = 16384):
    valueX = valueX+1
    xPos = int(valueX*scale)
    #yPos = int(valueY*scale)
    #print (xPos, valueX*scale )
    joystickPosition = vj.generateJoystickPosition(wAxisZRot = xPos)
    vj.update(joystickPosition)

def setJoy_steering(valueX, valueY=0, scale=16384):
    valueX = valueX+1
    xPos = int(valueX*scale)
    #yPos = int(valueY*scale)
    joystickPosition = vj.generateJoystickPosition(wAxisX = xPos, wAxisY = int(scale/2))
    vj.update(joystickPosition)

def setJoy_Steer_Throttle (value_steerX, value_throttleX, button_state,scale = 16384):
    value_steerX = value_steerX +1
    value_throttleX = value_throttleX +1
    xPos_steering = int(value_steerX*scale)
    xPos_throttle = int(value_throttleX*scale)
    joystickPosition = vj.generateJoystickPosition(wAxisX = xPos_steering, wAxisY = int(scale/2), wAxisZRot = xPos_throttle, lButtons = button_state)
    vj.update(joystickPosition)


def setJoy_Steer_Throttle_Brake (value_steerX, value_throttleX, brake_state,scale = 16384):
    value_steerX = value_steerX +1
    value_throttleX = value_throttleX +1
    xPos_steering = int(value_steerX*scale)
    xPos_throttle = int(value_throttleX*scale)
    joystickPosition = vj.generateJoystickPosition(wAxisX = xPos_steering, wAxisY = int(scale/2), wAxisZRot = xPos_throttle, lButtons = brake_state)
    vj.update(joystickPosition)


#for  i in range(10000):
#    xPos_steer = -1
#    setJoy_steering(xPos_steer)
predicted_steer = 0
predicted_throttle = -1

setJoy_Steer_Throttle(predicted_steer, predicted_throttle, 0)

#for i in range (2000):
#    xPos = -1 + i/1000
#    setJoy_steering(xPos)
#    time.sleep(0.001)


print("vj closing", flush=True)
vj.close()