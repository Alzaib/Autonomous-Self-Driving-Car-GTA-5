import numpy as np
from grabscreen import grab_screen
import cv2
import time
from directkeys import PressKey,ReleaseKey, W, A, S, D
import keras
from keras.models import load_model
from getkeys import key_check




from vjoy import vj, setJoy
#for steering and throttle control
def setJoy_Steer_Throttle (value_steerX, value_throttleX, scale = 16384):
    value_steerX = value_steerX +1
    value_throttleX = value_throttleX +1
    xPos_steering = int(value_steerX*scale)
    xPos_throttle = int(value_throttleX*scale)
    joystickPosition = vj.generateJoystickPosition(wAxisX = xPos_steering, wAxisY = int(scale/2), wAxisZRot = xPos_throttle)
    vj.update(joystickPosition)

#for steering, throttle and brake control
def setJoy_Steer_Throttle_Brake (value_steerX, value_throttleX, brake_state,scale = 16384):
    value_steerX = value_steerX +1
    value_throttleX = value_throttleX +1
    xPos_steering = int(value_steerX*scale)
    xPos_throttle = int(value_throttleX*scale)
    joystickPosition = vj.generateJoystickPosition(wAxisX = xPos_steering, wAxisY = int(scale/2), wAxisZRot = xPos_throttle, lButtons = brake_state)
    vj.update(joystickPosition)
    

def main():
    last_time = time.time()
    vj.open()
    time.sleep(1)

    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)
    model_name = 'steer_augmentation.h5'
    model = load_model(model_name)
    
    # Load Yolo
    net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
    classes = []
    with open("coco.names.txt", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()

    confidence_threshold = 0.6
    
    paused = False
    
    while(True):
        if not paused:
            '''-------------Screenshot for YOLO and CNN------------------------'''
            screen = grab_screen(region=(0,40,800,640)) # take screen shot of the screen
            img = screen #make a copy for YOLOv3
            window_width = 800
            img = img [:, round(window_width/4):round(window_width*3/4)]
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, channels = img.shape
            #window_width = width
            
            print ("FPS: ", 1/(time.time()-last_time)) #print FPS
            last_time = time.time()
            '''-------------------resize and reshape the input image for CNN----------------'''
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (160,120))

            prediction = model.predict([screen.reshape(-1,160,120,1)])[0]
            print (prediction)
            steering_angle = prediction [0]
            
            #if steering_angle > 0.20 or steering_angle <-0.20:
                #steering_angle = steering_angle*1.5
            
            throttle = prediction [1]
            brake = 0
            if throttle>=0:
                throttle = throttle/2
            else:
                throttle = -0.25
        
            #-----------------YOLO IMPLEMENTATION---------------------------------
            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(output_layers)
        
            #
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > confidence_threshold:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            for i in range(len(boxes)):
                if i in indexes:
                    if (classes[class_ids[i]] == 'car' or 
                            classes[class_ids[i]] == 'truck' or 
                            classes[class_ids[i]] == 'person' or 
                            classes[class_ids[i]] == 'motorbike' or
                            classes[class_ids[i]] == 'bus' or
                            classes[class_ids[i]] == 'train'or
                            classes[class_ids[i]] == 'stop sign'): # person bicycle car motorbike bus train stop sign
                        #PressKey(S)
                        x, y, w, h = boxes[i]
                        diag_len = np.sqrt((w*w)+(h*h))
                        #print (diag_len)
                        if diag_len >= 150: # Detected object is too close so STOP
                            print("STOP")
                            throttle = -1
                            steering_angle = 0
                            brake = 1
                        elif diag_len>=50 and diag_len<150: # Detected object is near by so SLOW DOWN
                            print("SLOW")
                            if throttle>=0:
                                throttle = throttle/2
                            else:
                                throttle = throttle-((1+throttle)/2)
                        else: #Detected object is far 
                            print("JUST DRIVE")
                            if throttle>=0:
                                throttle = throttle/2
                            else:
                                throttle = throttle-((1+throttle)/2)
                            
            setJoy_Steer_Throttle_Brake(steering_angle,throttle, brake)
            time.sleep(0.0001)


        keys = key_check()
        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                steering_angle = 0
                throttle = -1
                brake = 0
            
                setJoy_Steer_Throttle_Brake(steering_angle,throttle, brake)
                time.sleep(1)
main()

