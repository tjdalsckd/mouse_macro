from PIL import ImageGrab
import time
import cv2
import sys
import re
import threading
from easy_ocr import ocr_image

import keyboard

import mouse

import numpy as np
start = 0
value = 99999
print("Input checkvalue:")
check_value =int(input())
print("Input move1 x:")
move1_x =int(input())
print("Input move1 y:")
move1_y =int(input())
print("Input move2 x:")
move2_x =int(input())
print("Input move2 y:")
move2_y =int(input())

allstop = 0
ROI_SET = False
def move():
    global value
    global start

    global allstop
    while 1:
        if start == 1:
           start = 2
        if start>1:
           print(value)
           if value < check_value:
               print("move1")
               mouse.move(move1_x, move1_y, absolute=True, duration=0.25)
               mouse.click()
           elif value==99999:
               time.sleep(5)
           else:
               print("move2")
               mouse.move(move2_x, move2_y, absolute=True, duration=0.25)
               mouse.click()
               
           time.sleep(5)
           if allstop ==1:
                break;
 

def set_roi():
    global ROI_SET, x1, y1, x2, y2
    global start
    
    ROI_SET = False
    print("Select your ROI using mouse drag.")
    while(mouse.is_pressed() == False):

        x1, y1 = mouse.get_position()

        while(mouse.is_pressed() == True):

            x2, y2 = mouse.get_position()

            while(mouse.is_pressed() == False):

                print("Your ROI : {0}, {1}, {2}, {3}".format(x1, y1, x2, y2))

                ROI_SET = True
                
                return x1,y1,x2,y2


    
def stop():
   global allstop
   allstop = 1
 
def capture():
   global x1
   global x2
   global y1
   global y2
   global allstop
   global start
   global value
   global ROI_SET
   x1,y1,x2,y2 = set_roi()
   while True:
    if allstop ==1:
          break;
    if ROI_SET == True:
        image = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2))), cv2.COLOR_BGR2RGB)
        cv2.imwrite('image.png',image)
        start = 1
        try:
            value1=ocr_image('image.png',service='qq')
            value2 = re.findall("\d+",value1[0])
            value = float(value2[0])
        except:
            value = 40


        cv2.imshow("image", image)

        key = cv2.waitKey(10)

        if key == ord("q"):

            print("Quit")
            allstop = 1
            break

   cv2.destroyAllWindows()

th1 = threading.Thread(target=move)
th2 = threading.Thread(target=capture)
th1.start()
th2.start()

while 1:
    if allstop ==1:
        break;
    print("stopcommand : ",allstop,"\t read_value : ",value)
    time.sleep(1)

